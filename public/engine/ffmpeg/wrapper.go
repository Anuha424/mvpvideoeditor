package ffmpeg

import (
	"bufio"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"
)

// Errors
var (
	ErrInvalidPath    = fmt.Errorf("invalid file path")
	ErrFileNotFound   = fmt.Errorf("file not found")
	ErrNotAFile       = fmt.Errorf("path is not a file")
	ErrInvalidRange   = fmt.Errorf("invalid time range")
	ErrInvalidRegion  = fmt.Errorf("invalid watermark region")
	ErrTooFewFiles    = fmt.Errorf("at least 2 files required")
	ErrFFmpegNotFound = fmt.Errorf("ffmpeg not found in PATH")
)

// validateFile checks if a file exists and is accessible
func validateFile(path string) error {
	if path == "" {
		return ErrInvalidPath
	}
	absPath, err := filepath.Abs(path)
	if err != nil {
		return fmt.Errorf("%w: %v", ErrInvalidPath, err)
	}
	info, err := os.Stat(absPath)
	if err != nil {
		if os.IsNotExist(err) {
			return fmt.Errorf("%w: %s", ErrFileNotFound, absPath)
		}
		return fmt.Errorf("cannot access %s: %w", absPath, err)
	}
	if info.IsDir() {
		return fmt.Errorf("%w: %s", ErrNotAFile, absPath)
	}
	return nil
}

// ensureDir creates parent directory if needed
func ensureDir(outputPath string) error {
	dir := filepath.Dir(outputPath)
	if dir == "" || dir == "." {
		return nil
	}
	return os.MkdirAll(dir, 0755)
}

// getDuration returns video duration in seconds using ffprobe
func getDuration(inputPath string) (float64, error) {
	absPath, err := filepath.Abs(inputPath)
	if err != nil {
		return 0, err
	}
	cmd := exec.Command("ffprobe",
		"-v", "error",
		"-show_entries", "format=duration",
		"-of", "default=noprint_wrappers=1:nokey=1",
		absPath,
	)
	output, err := cmd.Output()
	if err != nil {
		return 0, fmt.Errorf("ffprobe failed: %w", err)
	}
	dur, err := strconv.ParseFloat(strings.TrimSpace(string(output)), 64)
	if err != nil {
		return 0, fmt.Errorf("cannot parse duration: %w", err)
	}
	return dur, nil
}

// parseProgress extracts progress from FFmpeg stderr
var timeRegex = regexp.MustCompile(`time=(\d+):(\d+):(\d+\.\d+)`)

func parseProgress(line string, duration float64) (float64, bool) {
	m := timeRegex.FindStringSubmatch(line)
	if len(m) != 4 || duration <= 0 {
		return 0, false
	}
	h, _ := strconv.ParseFloat(m[1], 64)
	mi, _ := strconv.ParseFloat(m[2], 64)
	s, _ := strconv.ParseFloat(m[3], 64)
	current := h*3600 + mi*60 + s
	progress := (current / duration) * 100
	if progress > 100 {
		progress = 100
	}
	return progress, true
}

// runFFmpeg executes ffmpeg with progress tracking
func runFFmpeg(args []string, duration float64, progressCb func(float64)) error {
	cmd := exec.Command("ffmpeg", args...)

	stderr, err := cmd.StderrPipe()
	if err != nil {
		return fmt.Errorf("stderr pipe: %w", err)
	}

	if err := cmd.Start(); err != nil {
		return fmt.Errorf("start ffmpeg: %w", err)
	}

	scanner := bufio.NewScanner(stderr)
	scanner.Buffer(make([]byte, 0, 64*1024), 1024*1024)

	for scanner.Scan() {
		if progressCb != nil && duration > 0 {
			if progress, ok := parseProgress(scanner.Text(), duration); ok {
				progressCb(progress)
			}
		}
	}

	if err := cmd.Wait(); err != nil {
		return fmt.Errorf("ffmpeg failed: %w", err)
	}

	if progressCb != nil {
		progressCb(100)
	}
	return nil
}

// Trim cuts video by timecodes
func Trim(inputPath, outputPath string, startTime, endTime float64, progressCb func(float64)) error {
	if err := validateFile(inputPath); err != nil {
		return err
	}
	if err := ensureDir(outputPath); err != nil {
		return fmt.Errorf("create output dir: %w", err)
	}
	if startTime < 0 || endTime <= startTime {
		return ErrInvalidRange
	}

	absInput, _ := filepath.Abs(inputPath)
	absOutput, _ := filepath.Abs(outputPath)
	duration := endTime - startTime

	args := []string{
		"-y",
		"-ss", fmt.Sprintf("%.3f", startTime),
		"-i", absInput,
		"-t", fmt.Sprintf("%.3f", duration),
		"-c:v", "libx264",
		"-c:a", "aac",
		"-preset", "fast",
		"-movflags", "+faststart",
		absOutput,
	}

	return runFFmpeg(args, duration, progressCb)
}

// Merge concatenates multiple videos
func Merge(inputPaths []string, outputPath string, progressCb func(float64)) error {
	if len(inputPaths) < 2 {
		return ErrTooFewFiles
	}
	for _, p := range inputPaths {
		if err := validateFile(p); err != nil {
			return err
		}
	}
	if err := ensureDir(outputPath); err != nil {
		return fmt.Errorf("create output dir: %w", err)
	}

	// Create concat file
	concatFile := outputPath + ".concat.txt"
	defer os.Remove(concatFile)

	var buf strings.Builder
	for _, p := range inputPaths {
		absPath, _ := filepath.Abs(p)
		escaped := strings.ReplaceAll(absPath, "'", "'\\''")
		buf.WriteString(fmt.Sprintf("file '%s'\n", escaped))
	}
	if err := os.WriteFile(concatFile, []byte(buf.String()), 0644); err != nil {
		return fmt.Errorf("write concat file: %w", err)
	}

	// Calculate total duration
	var totalDur float64
	for _, p := range inputPaths {
		if d, err := getDuration(p); err == nil {
			totalDur += d
		}
	}

	absOutput, _ := filepath.Abs(outputPath)
	args := []string{
		"-y",
		"-f", "concat",
		"-safe", "0",
		"-i", concatFile,
		"-c", "copy",
		"-movflags", "+faststart",
		absOutput,
	}

	return runFFmpeg(args, totalDur, progressCb)
}

// BlurWatermark hides watermark using delogo + boxblur
func BlurWatermark(inputPath, outputPath string, x, y, w, h, strength int, progressCb func(float64)) error {
	if err := validateFile(inputPath); err != nil {
		return err
	}
	if err := ensureDir(outputPath); err != nil {
		return fmt.Errorf("create output dir: %w", err)
	}
	if x < 0 || y < 0 || w <= 0 || h <= 0 {
		return ErrInvalidRegion
	}
	if strength < 1 {
		strength = 1
	}
	if strength > 50 {
		strength = 50
	}

	absInput, _ := filepath.Abs(inputPath)
	absOutput, _ := filepath.Abs(outputPath)

	dur, _ := getDuration(inputPath)

	// Build filter
	var filter string
	if strength <= 5 {
		// Simple delogo
		filter = fmt.Sprintf("delogo=x=%d:y=%d:w=%d:h=%d", x, y, w, h)
	} else {
		// Delogo + boxblur on region
		filter = fmt.Sprintf(
			"[0:v]split[main][blur];"+
				"[blur]crop=%d:%d:%d:%d,"+
				"boxblur=luma_radius=%d:chroma_radius=%d[blurred];"+
				"[main][blurred]overlay=%d:%d",
			w, h, x, y, strength, strength, x, y,
		)
	}

	args := []string{
		"-y",
		"-i", absInput,
		"-vf", filter,
		"-c:v", "libx264",
		"-preset", "fast",
		"-crf", "23",
		"-c:a", "copy",
		"-movflags", "+faststart",
		absOutput,
	}

	return runFFmpeg(args, dur, progressCb)
}
