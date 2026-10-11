package handlers

import (
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"video-editor/engine/worker"
)

// WatermarkBlurRequest represents watermark blur API request
type WatermarkBlurRequest struct {
	InputPath    string `json:"inputPath" binding:"required"`
	OutputPath   string `json:"outputPath"`
	X            int    `json:"x" binding:"required"`
	Y            int    `json:"y" binding:"required"`
	W            int    `json:"w" binding:"required"`
	H            int    `json:"h" binding:"required"`
	BlurStrength int    `json:"blurStrength"`
}

// WatermarkBlur handles watermark blur requests
func WatermarkBlur(pool *worker.Pool) gin.HandlerFunc {
	return func(c *gin.Context) {
		var req WatermarkBlurRequest
		if err := c.ShouldBindJSON(&req); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{
				"error": "invalid request body",
				"details": err.Error(),
			})
			return
		}

		// Validate region
		if req.X < 0 || req.Y < 0 {
			c.JSON(http.StatusBadRequest, gin.H{
				"error": "x and y must be >= 0",
			})
			return
		}
		if req.W <= 0 || req.H <= 0 {
			c.JSON(http.StatusBadRequest, gin.H{
				"error": "w and h must be > 0",
			})
			return
		}

		// Default blur strength
		strength := req.BlurStrength
		if strength <= 0 {
			strength = 10
		}

		// Generate output path
		outputPath := req.OutputPath
		if outputPath == "" {
			outputPath = "./output/watermark_" + uuid.New().String()[:8] + ".mp4"
		}

		// Create job
		jobID := uuid.New().String()
		job := worker.Job{
			ID:           jobID,
			Type:         worker.JobTypeWatermarkBlur,
			InputPath:    req.InputPath,
			OutputPath:   outputPath,
			WatermarkRegion: &worker.WatermarkRegion{
				X: req.X,
				Y: req.Y,
				W: req.W,
				H: req.H,
			},
			BlurStrength: strength,
			Status:       worker.StatusQueued,
			CreatedAt:    time.Now(),
		}

		pool.Submit(job)

		c.JSON(http.StatusAccepted, gin.H{
			"job_id":  jobID,
			"status":  "queued",
			"message": "watermark blur job submitted",
		})
	}
}
