package main

import (
	"context"
	"log"
	"os"
	"os/signal"
	"strconv"
	"syscall"
	"time"

	"github.com/gin-gonic/gin"
	"video-editor/engine/handlers"
	"video-editor/engine/worker"
)

func main() {
	// Quiet Gin logs
	gin.SetMode(gin.ReleaseMode)

	// Ensure output directory
	if err := os.MkdirAll("./output", 0755); err != nil {
		log.Fatalf("mkdir output: %v", err)
	}

	// Worker pool
	poolSize := 4
	if v := os.Getenv("WORKER_POOL_SIZE"); v != "" {
		if n, err := strconv.Atoi(v); err == nil && n > 0 && n <= 32 {
			poolSize = n
		}
	}

	pool := worker.NewPool(poolSize)
	pool.Start()

	// Router
	r := gin.New()
	r.Use(gin.Recovery()) // panic recovery
	r.Use(corsMiddleware())

	// Routes
	api := r.Group("/api")
	api.GET("/health", handlers.HealthCheck)
	api.POST("/trim", handlers.Trim(pool))
	api.POST("/merge", handlers.Merge(pool))
	api.POST("/watermark-blur", handlers.WatermarkBlur(pool))
	api.GET("/status/:job_id", handlers.Status(pool))

	r.Static("/output", "./output")

	port := envStr("PORT", "8080")

	// Graceful shutdown
	ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)
	defer stop()

	srv := &httpServer{addr: ":" + port, handler: r}
	go func() {
		log.Printf("engine :%s workers=%d", port, poolSize)
		if err := srv.listenAndServe(); err != nil {
			log.Printf("server: %v", err)
		}
	}()

	<-ctx.Done()
	log.Println("shutting down...")

	shutdownCtx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	srv.shutdown(shutdownCtx)
	pool.Stop()
	log.Println("bye")
}

func corsMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Header("Access-Control-Allow-Origin", "*")
		c.Header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
		c.Header("Access-Control-Allow-Headers", "Content-Type")
		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			return
		}
		c.Next()
	}
}

func envStr(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}
