package handlers

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"video-editor/engine/worker"
)

// Status returns job status
func Status(pool *worker.Pool) gin.HandlerFunc {
	return func(c *gin.Context) {
		jobID := c.Param("job_id")

		job, exists := pool.GetJob(jobID)
		if !exists {
			c.JSON(http.StatusNotFound, gin.H{
				"error": "job not found",
				"job_id": jobID,
			})
			return
		}

		c.JSON(http.StatusOK, gin.H{
			"job_id":      job.ID,
			"status":      job.Status,
			"progress":    job.Progress,
			"type":        job.Type,
			"output":      job.OutputPath,
			"error":       job.Error,
			"created_at":  job.CreatedAt,
			"started_at":  job.StartedAt,
			"finished_at": job.FinishedAt,
		})
	}
}
