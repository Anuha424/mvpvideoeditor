package handlers

import (
	"net/http"
	"os/exec"
	"runtime"
	"strings"

	"github.com/gin-gonic/gin"
)

// HealthCheck returns server status
func HealthCheck(c *gin.Context) {
	ffmpegAvailable := false
	ffmpegVersion := "not found"

	if out, err := exec.Command("ffmpeg", "-version").Output(); err == nil {
		ffmpegAvailable = true
		if lines := strings.Split(string(out), "\n"); len(lines) > 0 {
			ffmpegVersion = strings.TrimSpace(lines[0])
		}
	}

	c.JSON(http.StatusOK, gin.H{
		"status":           "running",
		"ffmpeg_available": ffmpegAvailable,
		"ffmpeg_version":   ffmpegVersion,
		"go_version":       runtime.Version(),
		"goroutines":       runtime.NumGoroutine(),
	})
}
