# 🎬 Video Editor v0.3

> Lightweight cross-platform desktop video editor with monochrome UI

## ✨ Что нового в v0.3

### Go-бэкенд
- **Graceful shutdown** — обработка SIGINT/SIGTERM с корректным завершением воркеров
- **Panic recovery** — middleware `gin.Recovery()` + defer/recover в воркерах
- **Валидация путей** — проверка существования файлов перед FFmpeg
- **Чистые JSON-ошибки** — понятные сообщения при невалидных запросах
- **Оптимизация** — убраны лишние импорты, компактный код

### Python GUI
- **QThread** — неблокирующие HTTP-запросы (health check, submit job, poll progress)
- **Event logger** — QTextEdit внизу окна с временными метками
- **Tooltips** — подсказки на всех кнопках и полях ввода
- **Монохромный стиль** — строго чёрный, белый, серый
- **Крупные кнопки** — интуитивный UX для новичков
- **Превью кадров** — QMediaPlayer с таймлайном

### Функционал
- **TRIM** — обрезка видео по таймкодам
- **MERGE** — склейка нескольких клипов
- **WATERMARK BLUR** — размытие водяных знаков (delogo + boxblur)
- **Прогресс-бар** — реаль-time обновление через polling

## 🏗️ Архитектура

```
┌─────────────────────────────────────────────────────────────┐
│         Python GUI (PySide6 + QThread + Event Logger)        │
│   Files │ Preview │ Trim/Merge/Watermark │ Progress │ Log    │
│                         │ HTTP/REST │                        │
├─────────────────────────┼───────────┼────────────────────────┤
│      Go Engine (Gin + Panic Recovery + Graceful Shutdown)    │
│   /health │ /trim │ /merge │ /watermark-blur │ /status/:id   │
│                    │ Worker Pool (WaitGroup) │               │
│                    │    FFmpeg CLI Wrapper    │               │
├────────────────────┴────────────────────────┴────────────────┤
│                    FFmpeg / Docker (Alpine)                   │
└──────────────────────────────────────────────────────────────┘
```

## 🚀 Быстрый старт

### 1. Запуск Go-движка
```bash
cd engine/
go mod download
go run main.go
# Engine listens on http://localhost:8080
```

### 2. Запуск Python GUI
```bash
cd gui/
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### 3. Docker (альтернатива)
```bash
cd engine/
docker build -t video-editor-engine .
docker run -d -p 8080:8080 -v $(pwd)/output:/app/output video-editor-engine
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Server health & FFmpeg status |
| POST | `/api/trim` | Cut video by timecodes |
| POST | `/api/merge` | Concatenate multiple clips |
| POST | `/api/watermark-blur` | Blur/hide watermark region |
| GET | `/api/status/:job_id` | Poll job progress (0–100%) |

### Примеры запросов

**Trim:**
```bash
curl -X POST http://localhost:8080/api/trim \
  -H "Content-Type: application/json" \
  -d '{"inputPath":"/path/video.mp4","startTime":5.0,"endTime":15.0}'
```

**Watermark Blur:**
```bash
curl -X POST http://localhost:8080/api/watermark-blur \
  -H "Content-Type: application/json" \
  -d '{"inputPath":"/path/video.mp4","x":10,"y":10,"w":200,"h":60,"blurStrength":15}'
```

## 📁 Структура проекта

```
video-editor/
├── engine/                 # Go backend
│   ├── main.go            # Entry point, graceful shutdown
│   ├── server.go          # HTTP server wrapper
│   ├── go.mod             # Dependencies
│   ├── Dockerfile         # Container build
│   ├── handlers/          # API handlers
│   │   ├── health.go
│   │   ├── trim.go
│   │   ├── merge.go
│   │   ├── watermark.go
│   │   └── status.go
│   ├── worker/
│   │   └── pool.go        # Worker pool (panic recovery)
│   └── ffmpeg/
│       └── wrapper.go     # FFmpeg CLI (validation + progress)
├── gui/                   # Python frontend
│   ├── main.py            # PySide6 entry, monochrome stylesheet
│   ├── api_client.py      # HTTP client + QThread classes
│   ├── requirements.txt
│   └── ui/
│       └── main_window.py # Main window (tabs, logger, preview)
├── Makefile
├── README.md
└── SETUP.md               # Detailed setup guide
```

## 🎨 Дизайн

**Строгий монохромный стиль:**
- Чёрный фон (#000000)
- Белый текст (#ffffff)
- Оттенки серого (#1a1a1a, #333333, #666666, #999999)
- Никаких цветных акцентов
- Профессиональная типографика (SF Mono, JetBrains Mono)

## 🔧 Оптимизация

- **Минимальное потребление RAM** — ~100-150 MB
- **QThread** — UI не зависает при HTTP-запросах
- **Goroutine pool** — параллельная обработка задач
- **Graceful shutdown** — корректное завершение без утечек
- **Panic recovery** — стабильность при ошибках

## 🛠️ Разработка

```bash
# Форматирование Go
cd engine && go fmt ./...

# Проверка Python
cd gui && python -m flake8 .

# Очистка
make clean

# Тесты
make test
```

## 📋 Системные требования

- Go 1.21+
- Python 3.10+
- FFmpeg 5.0+
- RAM 4 GB+

## 📖 Документация

- [SETUP.md](SETUP.md) — подробная инструкция по установке
- [README.md](README.md) — этот файл

## 🐛 Решение проблем

**Cannot connect to engine**
→ Убедитесь что движок запущен: `cd engine && go run main.go`

**ffmpeg: command not found**
→ Установите FFmpeg и перезапустите терминал

**GUI не открывается (Linux)**
→ `sudo apt install libxcb-xinerama0 libxcb-cursor0 libegl1`

## 📝 Лицензия

MIT

---

**Video Editor v0.3** — Monochrome Build  
Go + PySide6 + FFmpeg
