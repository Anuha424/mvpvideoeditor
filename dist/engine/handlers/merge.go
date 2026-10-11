package handlers

import (
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"video-editor/engine/worker"
)

// MergeRequest represents merge API request
type MergeRequest struct {
	InputPaths []string `json:"inputPaths" binding:"required"`
	OutputPath string   `json:"outputPath"`
}

// Merge handles video merge requests
func Merge(pool *worker.Pool) gin.HandlerFunc {
	return func(c *gin.Context) {
		var req MergeRequest
		if err := c.ShouldBindJSON(&req); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{
				"error": "invalid request body",
				"details": err.Error(),
			})
			return
		}

		// Validate input count
		if len(req.InputPaths) < 2 {
			c.JSON(http.StatusBadRequest, gin.H{
				"error": "at least 2 input files required",
			})
			return
		}

		// Validate each path is non-empty
		for i, p := range req.InputPaths {
			if p == "" {
				c.JSON(http.StatusBadRequest, gin.H{
					"error": "input path at index is empty",
					"index": i,
				})
				return
			}
		}

		// Generate output path
		outputPath := req.OutputPath
		if outputPath == "" {
			outputPath = "./output/merge_" + uuid.New().String()[:8] + ".mp4"
		}

		// Create job
		jobID := uuid.New().String()
		job := worker.Job{
			ID:         jobID,
			Type:       worker.JobTypeMerge,
			InputPaths: req.InputPaths,
			OutputPath: outputPath,
			Status:     worker.StatusQueued,
			CreatedAt:  time.Now(),
		}

		pool.Submit(job)

		c.JSON(http.StatusAccepted, gin.H{
			"job_id":  jobID,
			"status":  "queued",
			"message": "merge job submitted",
		})
	}
}
