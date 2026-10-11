package worker

import (
	"fmt"
	"log"
	"sync"
	"time"
	"video-editor/engine/ffmpeg"
)

// JobType represents the type of video processing job
type JobType string

const (
	JobTypeTrim          JobType = "trim"
	JobTypeMerge         JobType = "merge"
	JobTypeWatermarkBlur JobType = "watermark_blur"
)

// JobStatus represents the current status of a job
type JobStatus string

const (
	StatusQueued     JobStatus = "queued"
	StatusProcessing JobStatus = "processing"
	StatusCompleted  JobStatus = "completed"
	StatusFailed     JobStatus = "failed"
)

// WatermarkRegion defines the area to blur
type WatermarkRegion struct {
	X int `json:"x"`
	Y int `json:"y"`
	W int `json:"w"`
	H int `json:"h"`
}

// Job represents a video processing task
type Job struct {
	ID              string            `json:"job_id"`
	Type            JobType           `json:"type"`
	InputPath       string            `json:"-"`
	InputPaths      []string          `json:"-"`
	OutputPath      string            `json:"output"`
	StartTime       float64           `json:"-"`
	EndTime         float64           `json:"-"`
	WatermarkRegion *WatermarkRegion  `json:"-"`
	BlurStrength    int               `json:"-"`
	Status          JobStatus         `json:"status"`
	Progress        float64           `json:"progress"`
	Error           string            `json:"error,omitempty"`
	CreatedAt       time.Time         `json:"created_at"`
	StartedAt       *time.Time        `json:"started_at,omitempty"`
	FinishedAt      *time.Time        `json:"finished_at,omitempty"`
}

// Pool manages a pool of worker goroutines
type Pool struct {
	workers  int
	jobQueue chan Job
	jobs     map[string]*Job
	mu       sync.RWMutex
	quit     chan struct{}
	wg       sync.WaitGroup
}

// NewPool creates a new worker pool
func NewPool(workers int) *Pool {
	if workers < 1 {
		workers = 1
	}
	if workers > 32 {
		workers = 32
	}
	return &Pool{
		workers:  workers,
		jobQueue: make(chan Job, 100),
		jobs:     make(map[string]*Job),
		quit:     make(chan struct{}),
	}
}

// Start launches worker goroutines
func (p *Pool) Start() {
	for i := 0; i < p.workers; i++ {
		p.wg.Add(1)
		go p.worker(i)
	}
	log.Printf("pool started: %d workers", p.workers)
}

// Stop gracefully shuts down the pool
func (p *Pool) Stop() {
	close(p.quit)
	p.wg.Wait()
	log.Println("pool stopped")
}

// Submit adds a job to the queue
func (p *Pool) Submit(job Job) {
	p.mu.Lock()
	p.jobs[job.ID] = &job
	p.mu.Unlock()

	select {
	case p.jobQueue <- job:
		log.Printf("job %s queued", job.ID)
	default:
		log.Printf("job queue full, rejecting %s", job.ID)
		p.mu.Lock()
		job.Status = StatusFailed
		job.Error = "queue full"
		p.mu.Unlock()
	}
}

// GetJob returns a job by ID
func (p *Pool) GetJob(id string) (*Job, bool) {
	p.mu.RLock()
	defer p.mu.RUnlock()
	job, exists := p.jobs[id]
	return job, exists
}

// worker processes jobs from the queue
func (p *Pool) worker(id int) {
	defer p.wg.Done()
	for {
		select {
		case job, ok := <-p.jobQueue:
			if !ok {
				return
			}
			p.processJob(id, &job)
		case <-p.quit:
			return
		}
	}
}

// processJob handles the actual video processing with panic recovery
func (p *Pool) processJob(workerID int, job *Job) {
	defer func() {
		if r := recover(); r != nil {
			log.Printf("worker %d panic: %v", workerID, r)
			p.mu.Lock()
			job.Status = StatusFailed
			job.Error = fmt.Sprintf("internal error: %v", r)
			now := time.Now()
			job.FinishedAt = &now
			p.mu.Unlock()
		}
	}()

	log.Printf("worker %d processing %s (%s)", workerID, job.ID, job.Type)

	// Update status to processing
	now := time.Now()
	p.mu.Lock()
	job.Status = StatusProcessing
	job.StartedAt = &now
	job.Progress = 0
	p.mu.Unlock()

	var err error

	switch job.Type {
	case JobTypeTrim:
		err = ffmpeg.Trim(job.InputPath, job.OutputPath, job.StartTime, job.EndTime, p.progressCallback(job))
	case JobTypeMerge:
		err = ffmpeg.Merge(job.InputPaths, job.OutputPath, p.progressCallback(job))
	case JobTypeWatermarkBlur:
		if job.WatermarkRegion == nil {
			err = fmt.Errorf("watermark region required")
		} else {
			strength := job.BlurStrength
			if strength <= 0 {
				strength = 10
			}
			err = ffmpeg.BlurWatermark(
				job.InputPath,
				job.OutputPath,
				job.WatermarkRegion.X,
				job.WatermarkRegion.Y,
				job.WatermarkRegion.W,
				job.WatermarkRegion.H,
				strength,
				p.progressCallback(job),
			)
		}
	default:
		err = fmt.Errorf("unknown job type: %s", job.Type)
	}

	// Update final status
	finished := time.Now()
	p.mu.Lock()
	job.FinishedAt = &finished
	if err != nil {
		job.Status = StatusFailed
		job.Error = err.Error()
		log.Printf("job %s failed: %v", job.ID, err)
	} else {
		job.Status = StatusCompleted
		job.Progress = 100
		log.Printf("job %s completed", job.ID)
	}
	p.mu.Unlock()
}

// progressCallback returns a thread-safe progress update function
func (p *Pool) progressCallback(job *Job) func(float64) {
	return func(progress float64) {
		p.mu.Lock()
		job.Progress = progress
		p.mu.Unlock()
	}
}
