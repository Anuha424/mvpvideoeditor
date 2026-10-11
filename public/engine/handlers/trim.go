package handlers

import (
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"video-editor/engine/worker"
)

// TrimRequest represents trim API request
type TrimRequest struct {
	InputPath  string  `json:"inputPath" binding:"required"`
	OutputPath string  `json:"outputPath"`
	StartTime  float64 `json:"startTime" binding:"required"`
	EndTime    float64 `json:"endTime" binding:"required"`
}

// Trim handles video trim requests
func Trim(pool *worker.Pool) gin.HandlerFunc {
	return func(c *gin.Context) {
		var req TrimRequest
		if err := c.ShouldBindJSON(&req); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{
				"error": "invalid request body",
				"details": err.Error(),
			})
			return
		}

		// Validate time range
		if req.StartTime < 0 {
			c.JSON(http.StatusBadRequest, gin.H{
				"error": "startTime must be >= 0",
			})
			return
		}
		if req.EndTime <= req.StartTime {
			c.JSON(http.StatusBadRequest, gin.H{
				"error": "endTime must be greater than startTime",
			})
			return
		}

		// Generate output path
		outputPath := req.OutputPath
		if outputPath == "" {
			outputPath = "./output/trim_" + uuid.New().String()[:8] + ".mp4"
		}

		// Create job
		jobID := uuid.New().String()
		job := worker.Job{
			ID:         jobID,
			Type:       worker.JobTypeTrim,
			InputPath:  req.InputPath,
			OutputPath: outputPath,
			StartTime:  req.StartTime,
			EndTime:    req.EndTime,
			Status:     worker.StatusQueued,
			CreatedAt:  time.Now(),
		}

		pool.Submit(job)

		c.JSON(http.StatusAccepted, gin.H{
			"job_id":  jobID,
			"status":  "queued",
			"message": "trim job submitted",
		})
	}
}
