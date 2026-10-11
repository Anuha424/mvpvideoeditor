# Video Editor MVP — Makefile
# ================================

.PHONY: all engine gui docker run clean help

# Default target
all: engine gui

# ================================
# Go Engine
# ================================

engine:
	@echo "Building Go Engine..."
	cd engine && go build -o ../bin/video-engine .
	@echo "Engine built: bin/video-engine"

engine-run:
	@echo "Starting Go Engine on :8080..."
	cd engine && go run main.go

# ================================
# Python GUI
# ================================

gui:
	@echo "Setting up Python GUI..."
	cd gui && pip install -r requirements.txt
	@echo "GUI dependencies installed"

gui-run:
	@echo "Launching Python GUI..."
	cd gui && python main.py

# ================================
# Docker
# ================================

docker-build:
	@echo "Building Docker image..."
	cd engine && docker build -t video-editor-engine .
	@echo "Docker image built: video-editor-engine"

docker-run:
	@echo "Starting Docker container..."
	docker run -d \
		--name video-engine \
		-p 8080:8080 \
		-v $(PWD)/output:/app/output \
		video-editor-engine
	@echo "Container running on http://localhost:8080"

docker-stop:
	@echo "Stopping Docker container..."
	docker stop video-engine && docker rm video-engine

# ================================
# Full Stack
# ================================

run: engine docker-run gui-run
	@echo "Full stack running!"

# ================================
# Utilities
# ================================

clean:
	@echo "Cleaning build artifacts..."
	rm -rf bin/
	rm -rf engine/output/
	rm -rf gui/__pycache__/
	rm -rf gui/ui/__pycache__/
	@echo "Clean"

test:
	@echo "Running tests..."
	cd engine && go test ./...
	@echo "Tests passed"

help:
	@echo ""
	@echo "Video Editor MVP — Available Commands"
	@echo "========================================="
	@echo "  make engine       — Build Go engine binary"
	@echo "  make engine-run   — Run Go engine locally"
	@echo "  make gui          — Install Python dependencies"
	@echo "  make gui-run      — Launch Python GUI"
	@echo "  make docker-build — Build Docker image"
	@echo "  make docker-run   — Run engine in Docker"
	@echo "  make docker-stop  — Stop Docker container"
	@echo "  make run          — Start full stack"
	@echo "  make clean        — Remove build artifacts"
	@echo "  make test         — Run tests"
	@echo ""
