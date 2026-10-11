# Multi-stage build for Video Editor Engine
FROM golang:1.21-alpine AS builder

RUN apk add --no-cache ffmpeg
WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux \
    go build -ldflags="-w -s" -o /video-engine .

# --- Runtime stage ---
FROM alpine:3.19

RUN apk add --no-cache \
    ffmpeg \
    ca-certificates \
    && mkdir -p /app/output

WORKDIR /app
COPY --from=builder /video-engine .

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD wget -qO- http://localhost:8080/api/health || exit 1

CMD ["./video-engine"]
