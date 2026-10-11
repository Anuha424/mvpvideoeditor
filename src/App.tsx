import { useState } from 'react'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import vscDarkPlus from 'react-syntax-highlighter/dist/esm/styles/prism/vsc-dark-plus'
import {
  Server, Monitor, Container, FileCode, FolderTree,
  Terminal, Zap, Layers, Cpu, Globe, Package, BookOpen,
  Github, Eye, Square, Shield, Activity
} from 'lucide-react'

type TabType = 'overview' | 'architecture' | 'code' | 'setup'

function App() {
  const [activeTab, setActiveTab] = useState<TabType>('overview')
  const [selectedFile, setSelectedFile] = useState('engine/main.go')
  const [os, setOs] = useState<'macos' | 'linux' | 'windows'>('macos')

  return (
    <div className="min-h-screen bg-black text-white antialiased">
      <header className="border-b border-neutral-900 bg-black/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded border border-neutral-700 flex items-center justify-center">
              <Square size={14} className="text-white" />
            </div>
            <div>
              <h1 className="text-sm font-semibold tracking-wider text-white">VIDEO EDITOR</h1>
              <p className="text-[10px] text-neutral-600 tracking-widest uppercase">Go · PySide6 · FFmpeg</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <span className="px-2 py-0.5 text-[10px] tracking-wider uppercase rounded border border-neutral-800 text-neutral-500">v0.3</span>
            <a href="#" className="p-1.5 rounded hover:bg-neutral-900 transition-colors">
              <Github size={16} className="text-neutral-500" />
            </a>
          </div>
        </div>
      </header>

      <nav className="border-b border-neutral-900">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex">
            {([
              { id: 'overview' as const, label: 'OVERVIEW', icon: <BookOpen size={13} /> },
              { id: 'architecture' as const, label: 'ARCHITECTURE', icon: <Layers size={13} /> },
              { id: 'code' as const, label: 'SOURCE', icon: <FileCode size={13} /> },
              { id: 'setup' as const, label: 'SETUP', icon: <Terminal size={13} /> },
            ]).map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-4 py-3 text-[11px] tracking-wider font-medium border-b transition-all ${
                  activeTab === tab.id ? 'border-white text-white' : 'border-transparent text-neutral-600 hover:text-neutral-300'
                }`}
              >
                {tab.icon}{tab.label}
              </button>
            ))}
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-6 py-8">
        {activeTab === 'overview' && <OverviewTab />}
        {activeTab === 'architecture' && <ArchitectureTab />}
        {activeTab === 'code' && <CodeTab selectedFile={selectedFile} setSelectedFile={setSelectedFile} />}
        {activeTab === 'setup' && <SetupTab os={os} setOs={setOs} />}
      </main>

      <footer className="border-t border-neutral-900 mt-16">
        <div className="max-w-7xl mx-auto px-6 py-6 text-center text-neutral-700 text-[10px] tracking-widest uppercase">
          Video Editor v0.3 — Monochrome Build
        </div>
      </footer>
    </div>
  )
}

function OverviewTab() {
  const features = [
    { icon: <Zap size={18} />, title: 'FFmpeg Integration', desc: 'CLI wrapper with real-time progress parsing' },
    { icon: <Server size={18} />, title: 'REST API (Gin)', desc: 'High-performance HTTP server with panic recovery' },
    { icon: <Layers size={18} />, title: 'Worker Pool', desc: 'Goroutine-based async queue with graceful shutdown' },
    { icon: <Monitor size={18} />, title: 'Monochrome GUI', desc: 'PySide6 — black, white, gray. Professional aesthetic' },
    { icon: <Eye size={18} />, title: 'Watermark Blur', desc: 'Hide logos with delogo + boxblur filter' },
    { icon: <Shield size={18} />, title: 'Robust Error Handling', desc: 'Validation, panic recovery, QThread for non-blocking UI' },
  ]

  const apiEndpoints = [
    { method: 'GET', path: '/api/health', desc: 'Server health & FFmpeg status' },
    { method: 'POST', path: '/api/trim', desc: 'Cut video by start/end timecodes' },
    { method: 'POST', path: '/api/merge', desc: 'Concatenate multiple clips' },
    { method: 'POST', path: '/api/watermark-blur', desc: 'Blur/hide watermark region (x,y,w,h)' },
    { method: 'GET', path: '/api/status/:job_id', desc: 'Poll async job progress (0–100%)' },
  ]

  return (
    <div className="space-y-12">
      <div className="py-8">
        <h2 className="text-3xl font-bold text-white tracking-tight mb-3">Cross-Platform Video Editor</h2>
        <p className="text-neutral-500 text-base max-w-2xl leading-relaxed">
          Lightweight desktop video editor. Go backend with graceful shutdown and panic recovery,
          PySide6 GUI with QThread for non-blocking operations. Trim, merge, and hide watermarks.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-px bg-neutral-900 border border-neutral-900 rounded-lg overflow-hidden">
        {[
          { label: 'GO ENGINE', desc: 'Gin HTTP, goroutine pool, FFmpeg CLI, graceful shutdown' },
          { label: 'PYTHON GUI', desc: 'PySide6/Qt, monochrome theme, QThread, event logger' },
          { label: 'DOCKER', desc: 'Alpine multi-stage, CI/CD ready' },
        ].map((item, i) => (
          <div key={i} className="bg-black p-6">
            <p className="text-[10px] tracking-widest text-neutral-600 mb-2">{item.label}</p>
            <p className="text-sm text-neutral-400">{item.desc}</p>
          </div>
        ))}
      </div>

      <div>
        <h3 className="text-[10px] tracking-widest text-neutral-600 mb-4 uppercase">Features</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-px bg-neutral-900 border border-neutral-900 rounded-lg overflow-hidden">
          {features.map((f, i) => (
            <div key={i} className="bg-black p-5 hover:bg-neutral-950 transition-colors">
              <div className="text-neutral-500 mb-3">{f.icon}</div>
              <h4 className="text-sm font-medium text-white mb-1">{f.title}</h4>
              <p className="text-xs text-neutral-600 leading-relaxed">{f.desc}</p>
            </div>
          ))}
        </div>
      </div>

      <div>
        <h3 className="text-[10px] tracking-widest text-neutral-600 mb-4 uppercase">REST API</h3>
        <div className="border border-neutral-900 rounded-lg overflow-hidden">
          <table className="w-full">
            <thead>
              <tr className="bg-neutral-950 border-b border-neutral-900">
                <th className="text-left px-5 py-3 text-[10px] tracking-wider text-neutral-600 font-medium">METHOD</th>
                <th className="text-left px-5 py-3 text-[10px] tracking-wider text-neutral-600 font-medium">ENDPOINT</th>
                <th className="text-left px-5 py-3 text-[10px] tracking-wider text-neutral-600 font-medium">DESCRIPTION</th>
              </tr>
            </thead>
            <tbody>
              {apiEndpoints.map((ep, i) => (
                <tr key={i} className="border-b border-neutral-900/50 hover:bg-neutral-950/50">
                  <td className="px-5 py-3">
                    <span className={`px-1.5 py-0.5 rounded text-[10px] font-mono font-bold tracking-wider ${
                      ep.method === 'GET' ? 'bg-neutral-900 text-neutral-400' : 'bg-neutral-800 text-white'
                    }`}>{ep.method}</span>
                  </td>
                  <td className="px-5 py-3 font-mono text-xs text-neutral-300">{ep.path}</td>
                  <td className="px-5 py-3 text-xs text-neutral-600">{ep.desc}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

function ArchitectureTab() {
  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-xl font-bold text-white mb-1">System Architecture</h2>
        <p className="text-sm text-neutral-600">Component diagram with graceful shutdown and QThread</p>
      </div>

      <div className="rounded-lg border border-neutral-900 bg-neutral-950 p-6 overflow-x-auto">
        <pre className="text-xs text-neutral-400 font-mono leading-relaxed whitespace-pre">
{`┌─────────────────────────────────────────────────────────────────────┐
│              Python GUI (PySide6 — Monochrome + QThread)             │
│                                                                      │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │
│   │  FILES   │  │ PREVIEW  │  │  TRIM /  │  │   EVENT LOG      │   │
│   │  PICKER  │  │  PLAYER  │  │  MERGE / │  │   (QTextEdit)    │   │
│   │          │  │          │  │  WM BLUR │  │                  │   │
│   └──────────┘  └──────────┘  └──────────┘  └──────────────────┘   │
│                                                                      │
│        QThread: HealthCheck | SubmitJob | PollJob (non-blocking)     │
│                        │  HTTP / REST  │                              │
├────────────────────────┼───────────────┼──────────────────────────────┤
│              Go Engine (Gin + Panic Recovery)                        │
│                                                                      │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │
│   │ /health  │  │ /trim    │  │ /merge   │  │ /watermark-blur  │   │
│   └──────────┘  └──────────┘  └──────────┘  └──────────────────┘   │
│                                                                      │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │         Worker Pool (Goroutines + Channels + WaitGroup)      │   │
│   │                                                              │   │
│   │   ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐          │   │
│   │   │Worker 1│  │Worker 2│  │Worker 3│  │Worker 4│          │   │
│   │   └────────┘  └────────┘  └────────┘  └────────┘          │   │
│   └─────────────────────────────────────────────────────────────┘   │
│                          │                                           │
│               ┌──────────┴──────────┐                                │
│               │  FFmpeg CLI Wrapper  │                                │
│               │  (validation+progress)                                │
│               └──────────────────────┘                                │
├──────────────────────────────────────────────────────────────────────┤
│     Graceful Shutdown: signal.NotifyContext → pool.Stop() → exit    │
└──────────────────────────────────────────────────────────────────────┘`}
        </pre>
      </div>

      <div>
        <h3 className="text-[10px] tracking-widest text-neutral-600 mb-4 uppercase">Project Structure</h3>
        <div className="rounded-lg border border-neutral-900 bg-neutral-950 p-6">
          <pre className="text-xs font-mono text-neutral-400 leading-loose">
{`video-editor/
├── engine/                      Go Backend
│   ├── main.go                 Entry point, graceful shutdown
│   ├── server.go               HTTP server wrapper
│   ├── go.mod                  Module dependencies
│   ├── Dockerfile              Multi-stage container
│   ├── handlers/               API endpoints
│   │   ├── health.go           GET  /api/health
│   │   ├── trim.go             POST /api/trim
│   │   ├── merge.go            POST /api/merge
│   │   ├── watermark.go        POST /api/watermark-blur
│   │   └── status.go           GET  /api/status/:job_id
│   ├── worker/
│   │   └── pool.go             Worker pool (goroutines, panic recovery)
│   └── ffmpeg/
│       └── wrapper.go          FFmpeg CLI (trim, merge, delogo/boxblur)
│
├── gui/                         Python Frontend
│   ├── main.py                 PySide6 entry, monochrome stylesheet
│   ├── api_client.py           HTTP client + QThread classes
│   ├── requirements.txt        Python deps
│   └── ui/
│       └── main_window.py      Main window (tabs, logger, preview)
│
├── Makefile                     Build automation
├── README.md                    Documentation
└── SETUP.md                     Detailed setup guide`}
          </pre>
        </div>
      </div>
    </div>
  )
}

function CodeTab({ selectedFile, setSelectedFile }: { selectedFile: string; setSelectedFile: (f: string) => void }) {
  const files: Record<string, { language: string; description: string; code: string }> = {
    'engine/main.go': {
      language: 'go',
      description: 'Entry point with graceful shutdown',
      code: `package main

import (
\t"context"
\t"log"
\t"os"
\t"os/signal"
\t"strconv"
\t"syscall"
\t"time"

\t"github.com/gin-gonic/gin"
\t"video-editor/engine/handlers"
\t"video-editor/engine/worker"
)

func main() {
\tgin.SetMode(gin.ReleaseMode)

\tif err := os.MkdirAll("./output", 0755); err != nil {
\t\tlog.Fatalf("mkdir output: %v", err)
\t}

\tpoolSize := 4
\tif v := os.Getenv("WORKER_POOL_SIZE"); v != "" {
\t\tif n, err := strconv.Atoi(v); err == nil && n > 0 && n <= 32 {
\t\t\tpoolSize = n
\t\t}
\t}

\tpool := worker.NewPool(poolSize)
\tpool.Start()

\tr := gin.New()
\tr.Use(gin.Recovery()) // panic recovery
\tr.Use(corsMiddleware())

\tapi := r.Group("/api")
\tapi.GET("/health", handlers.HealthCheck)
\tapi.POST("/trim", handlers.Trim(pool))
\tapi.POST("/merge", handlers.Merge(pool))
\tapi.POST("/watermark-blur", handlers.WatermarkBlur(pool))
\tapi.GET("/status/:job_id", handlers.Status(pool))

\tr.Static("/output", "./output")

\tport := envStr("PORT", "8080")

\t// Graceful shutdown
\tctx, stop := signal.NotifyContext(context.Background(),
\t\tsyscall.SIGINT, syscall.SIGTERM)
\tdefer stop()

\tsrv := &httpServer{addr: ":" + port, handler: r}
\tgo func() {
\t\tlog.Printf("engine :%s workers=%d", port, poolSize)
\t\tsrv.listenAndServe()
\t}()

\t<-ctx.Done()
\tlog.Println("shutting down...")

\tshutdownCtx, cancel := context.WithTimeout(
\t\tcontext.Background(), 5*time.Second)
\tdefer cancel()

\tsrv.shutdown(shutdownCtx)
\tpool.Stop()
\tlog.Println("bye")
}`
    },
    'engine/worker/pool.go': {
      language: 'go',
      description: 'Worker pool with panic recovery',
      code: `package worker

import (
\t"fmt"
\t"log"
\t"sync"
\t"time"
\t"video-editor/engine/ffmpeg"
)

type JobType string
const (
\tJobTypeTrim          JobType = "trim"
\tJobTypeMerge         JobType = "merge"
\tJobTypeWatermarkBlur JobType = "watermark_blur"
)

type Job struct {
\tID              string
\tType            JobType
\tInputPath       string
\tInputPaths      []string
\tOutputPath      string
\tStartTime       float64
\tEndTime         float64
\tWatermarkRegion *WatermarkRegion
\tBlurStrength    int
\tStatus          JobStatus
\tProgress        float64
\tError           string
\tCreatedAt       time.Time
\tStartedAt       *time.Time
\tFinishedAt      *time.Time
}

type Pool struct {
\tworkers  int
\tjobQueue chan Job
\tjobs     map[string]*Job
\tmu       sync.RWMutex
\tquit     chan struct{}
\twg       sync.WaitGroup
}

func (p *Pool) processJob(wid int, job *Job) {
\tdefer func() {
\t\tif r := recover(); r != nil {
\t\t\tlog.Printf("worker %d panic: %v", wid, r)
\t\t\tp.mu.Lock()
\t\t\tjob.Status = StatusFailed
\t\t\tjob.Error = fmt.Sprintf("internal error: %v", r)
\t\t\tnow := time.Now()
\t\t\tjob.FinishedAt = &now
\t\t\tp.mu.Unlock()
\t\t}
\t}()

\t// Process job...
\tswitch job.Type {
\tcase JobTypeTrim:
\t\terr = ffmpeg.Trim(job.InputPath, job.OutputPath,
\t\t\tjob.StartTime, job.EndTime, p.progressCallback(job))
\tcase JobTypeWatermarkBlur:
\t\terr = ffmpeg.BlurWatermark(
\t\t\tjob.InputPath, job.OutputPath,
\t\t\tjob.WatermarkRegion.X, job.WatermarkRegion.Y,
\t\t\tjob.WatermarkRegion.W, job.WatermarkRegion.H,
\t\t\tjob.BlurStrength, p.progressCallback(job))
\t}
}`
    },
    'gui/api_client.py': {
      language: 'python',
      description: 'HTTP client with QThread support',
      code: `"""HTTP Client with QThread for non-blocking operations."""

import requests
from dataclasses import dataclass
from typing import Optional, Dict, Any
from PySide6.QtCore import QThread, Signal


@dataclass
class JobStatus:
    job_id: str
    status: str
    progress: float
    type: str
    output: str
    error: Optional[str] = None


class EngineClient:
    """HTTP client for Go Video Editor Engine."""

    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def health_check(self) -> Dict[str, Any]:
        try:
            r = self.session.get(f"{self.base_url}/api/health", timeout=5)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.ConnectionError:
            return {"status": "offline", "error": "cannot connect"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def trim_video(self, input_path: str, start_time: float,
                   end_time: float) -> Dict[str, Any]:
        return self._post("/api/trim", {
            "inputPath": input_path,
            "startTime": start_time,
            "endTime": end_time,
        })

    def blur_watermark(self, input_path: str, x: int, y: int,
                       w: int, h: int, blur_strength: int = 10) -> Dict:
        return self._post("/api/watermark-blur", {
            "inputPath": input_path,
            "x": x, "y": y, "w": w, "h": h,
            "blurStrength": blur_strength,
        })

    def get_job_status(self, job_id: str) -> JobStatus:
        try:
            r = self.session.get(
                f"{self.base_url}/api/status/{job_id}", timeout=5)
            r.raise_for_status()
            d = r.json()
            return JobStatus(
                job_id=d.get("job_id", job_id),
                status=d.get("status", "unknown"),
                progress=float(d.get("progress", 0)),
                type=d.get("type", ""),
                output=d.get("output", ""),
                error=d.get("error"),
            )
        except Exception as e:
            return JobStatus(job_id, "error", 0, "", "", str(e))

    def is_connected(self) -> bool:
        return self.health_check().get("status") == "running"

    def _post(self, endpoint: str, payload: Dict) -> Dict:
        try:
            r = self.session.post(
                f"{self.base_url}{endpoint}",
                json=payload, timeout=10)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            return {"error": str(e)}


# QThread Classes for Non-blocking Operations
class HealthCheckThread(QThread):
    finished = Signal(dict)
    def __init__(self, client: EngineClient):
        super().__init__()
        self.client = client
    def run(self):
        self.finished.emit(self.client.health_check())


class SubmitJobThread(QThread):
    finished = Signal(dict)
    error = Signal(str)
    def __init__(self, client: EngineClient, endpoint: str, payload: Dict):
        super().__init__()
        self.client = client
        self.endpoint = endpoint
        self.payload = payload
    def run(self):
        try:
            result = self.client._post(self.endpoint, self.payload)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class PollJobThread(QThread):
    finished = Signal(object)
    def __init__(self, client: EngineClient, job_id: str):
        super().__init__()
        self.client = client
        self.job_id = job_id
    def run(self):
        self.finished.emit(self.client.get_job_status(self.job_id))`
    },
  }

  return (
    <div className="flex gap-4 h-[calc(100vh-220px)]">
      <div className="w-64 shrink-0 rounded-lg border border-neutral-900 bg-neutral-950 overflow-hidden flex flex-col">
        <div className="px-4 py-3 border-b border-neutral-900">
          <p className="text-[10px] tracking-widest text-neutral-600 uppercase">Files</p>
        </div>
        <div className="overflow-y-auto flex-1 p-1.5">
          {Object.entries(files).map(([path, meta]) => (
            <button
              key={path}
              onClick={() => setSelectedFile(path)}
              className={`w-full text-left px-3 py-2 rounded text-xs flex items-center gap-2 transition-all ${
                selectedFile === path ? 'bg-neutral-800 text-white' : 'text-neutral-600 hover:bg-neutral-900 hover:text-neutral-300'
              }`}
            >
              <FileCode size={13} className="text-neutral-700" />
              <div className="min-w-0">
                <div className="font-mono text-[11px] truncate">{path}</div>
                <div className="text-[9px] text-neutral-700 truncate">{meta.description}</div>
              </div>
            </button>
          ))}
        </div>
      </div>

      <div className="flex-1 rounded-lg border border-neutral-900 bg-neutral-950 overflow-hidden flex flex-col">
        <div className="px-4 py-3 border-b border-neutral-900 flex items-center gap-2">
          <FileCode size={13} className="text-neutral-700" />
          <span className="text-xs font-mono text-neutral-400">{selectedFile}</span>
        </div>
        <div className="overflow-auto flex-1">
          <SyntaxHighlighter
            language={files[selectedFile]?.language || 'text'}
            style={vscDarkPlus}
            customStyle={{ margin: 0, padding: '1rem', background: 'transparent', fontSize: '12px', lineHeight: '1.7' }}
            showLineNumbers
            lineNumberStyle={{ color: '#222', minWidth: '2.5em' }}
          >
            {files[selectedFile]?.code || ''}
          </SyntaxHighlighter>
        </div>
      </div>
    </div>
  )
}

function SetupTab({ os, setOs }: { os: 'macos' | 'linux' | 'windows'; setOs: (o: 'macos' | 'linux' | 'windows') => void }) {
  const installCommands: Record<string, string[]> = {
    macos: ['# Homebrew', 'brew install go python ffmpeg', '', '# Проверка', 'go version', 'python3 --version', 'ffmpeg -version'],
    linux: ['# Ubuntu/Debian', 'sudo apt update', 'sudo apt install -y golang python3 ffmpeg', '', '# Проверка', 'go version', 'python3 --version', 'ffmpeg -version'],
    windows: ['# PowerShell (admin)', 'winget install GoLang.Go', 'winget install Python.Python.3.12', 'winget install Gyan.FFmpeg', '', '# Перезапустите PowerShell', 'go version', 'python --version', 'ffmpeg -version'],
  }

  const steps = [
    { title: 'Клонирование', commands: ['git clone https://github.com/YOUR_USERNAME/video-editor.git', 'cd video-editor'] },
    { title: 'Установка зависимостей', commands: installCommands[os] },
    { title: 'Запуск Go-движка', commands: ['cd engine/', 'go mod download', 'go run main.go', '', '# В другом терминале:', 'curl http://localhost:8080/api/health'] },
    { title: 'Настройка Python GUI', commands: os === 'windows' ? ['cd gui', 'python -m venv venv', 'venv\\Scripts\\activate', 'pip install -r requirements.txt'] : ['cd gui/', 'python3 -m venv venv', 'source venv/bin/activate', 'pip install -r requirements.txt'] },
    { title: 'Запуск GUI', commands: ['python main.py'] },
  ]

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-xl font-bold text-white mb-1">Setup Guide</h2>
        <p className="text-sm text-neutral-600">Пошаговая инструкция по установке и запуску</p>
      </div>

      <div className="flex gap-2">
        {(['macos', 'linux', 'windows'] as const).map(item => (
          <button
            key={item}
            onClick={() => setOs(item)}
            className={`px-4 py-2 text-xs tracking-wider rounded transition-all ${
              os === item ? 'bg-white text-black font-medium' : 'bg-neutral-900 text-neutral-500 hover:text-white hover:bg-neutral-800'
            }`}
          >
            {item.toUpperCase()}
          </button>
        ))}
      </div>

      <div className="space-y-px bg-neutral-900 border border-neutral-900 rounded-lg overflow-hidden">
        {steps.map((step, i) => (
          <div key={i} className="bg-black">
            <div className="px-5 py-3 border-b border-neutral-900 flex items-center gap-3">
              <span className="text-[10px] font-mono text-neutral-700">{String(i + 1).padStart(2, '0')}</span>
              <span className="text-xs text-white font-medium">{step.title}</span>
            </div>
            <div className="px-5 py-3 pl-14">
              <pre className="text-xs font-mono leading-relaxed">
                {step.commands.map((line, j) => (
                  <div key={j} className={line.startsWith('#') ? 'text-neutral-700' : line === '' ? '' : 'text-neutral-400'}>
                    {line || '\u00A0'}
                  </div>
                ))}
              </pre>
            </div>
          </div>
        ))}
      </div>

      <div className="rounded-lg border border-neutral-900 bg-neutral-950 p-5">
        <p className="text-[10px] tracking-widest text-neutral-600 mb-3 uppercase">Чеклист</p>
        <div className="space-y-2">
          {['Go 1.21+ установлен', 'Python 3.10+ установлен', 'FFmpeg установлен', 'Engine запущен (:8080)', 'GUI запущен', 'В GUI виден "connected"'].map((item, i) => (
            <div key={i} className="flex items-center gap-3">
              <div className="w-4 h-4 rounded border border-neutral-700 flex items-center justify-center shrink-0">
                <span className="text-[8px] text-neutral-600">{i + 1}</span>
              </div>
              <span className="text-xs text-neutral-500">{item}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default App
