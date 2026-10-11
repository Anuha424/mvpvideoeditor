# 📖 Подробная инструкция по запуску Video Editor MVP

> Полное руководство по установке, настройке и запуску проекта на любой операционной системе.

---

## 📋 Содержание

1. [Системные требования](#1-системные-требования)
2. [Установка зависимостей](#2-установка-зависимостей)
3. [Клонирование и структура проекта](#3-клонирование-и-структура-проекта)
4. [Запуск Go-движка (локально)](#4-запуск-go-движка-локально)
5. [Запуск Go-движка (Docker)](#5-запуск-go-движка-docker)
6. [Настройка Python GUI](#6-настройка-python-gui)
7. [Запуск GUI](#7-запуск-gui)
8. [Тестирование API](#8-тестирование-api)
9. [Полный запуск (все в одном)](#9-полный-запуск-все-в-одном)
10. [Решение проблем](#10-решение-проблем)
11. [Разработка и отладка](#11-разработка-и-отладка)

---

## 1. Системные требования

### Минимальные

| Компонент | Версия | Примечание |
|-----------|--------|------------|
| **ОС** | Windows 10+, macOS 11+, Ubuntu 20.04+ | 64-bit |
| **Go** | 1.21+ | [go.dev/dl](https://go.dev/dl/) |
| **Python** | 3.10+ | [python.org](https://www.python.org/downloads/) |
| **FFmpeg** | 5.0+ | [ffmpeg.org](https://ffmpeg.org/download.html) |
| **RAM** | 4 GB+ | Для рендеринга видео |
| **Диск** | 1 GB свободного места | + место для видео |

### Рекомендуемые

| Компонент | Версия |
|-----------|--------|
| **Go** | 1.22+ |
| **Python** | 3.12+ |
| **FFmpeg** | 6.0+ |
| **RAM** | 8 GB+ |
| **Docker** | 24.0+ (опционально) |

---

## 2. Установка зависимостей

### 🍎 macOS

```bash
# Homebrew (если не установлен)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Go
brew install go

# Python
brew install python

# FFmpeg
brew install ffmpeg

# Docker (опционально)
brew install --cask docker

# Проверка версий
go version          # Должно быть: go version go1.21+ darwin/arm64
python3 --version   # Должно быть: Python 3.10+
ffmpeg -version     # Должно быть: ffmpeg version 5.0+
```

### 🐧 Linux (Ubuntu/Debian)

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Go
wget https://go.dev/dl/go1.22.0.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.22.0.linux-amd64.tar.gz
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
source ~/.bashrc

# Python (обычно предустановлен)
sudo apt install -y python3 python3-pip python3-venv

# FFmpeg
sudo apt install -y ffmpeg

# Docker (опционально)
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
# Перелогиньтесь после добавления в группу docker

# Проверка версий
go version
python3 --version
ffmpeg -version
```

### 🪟 Windows

#### Вариант A: Через winget (рекомендуется)

```powershell
# Откройте PowerShell от имени администратора

# Go
winget install GoLang.Go

# Python
winget install Python.Python.3.12

# FFmpeg
winget install Gyan.FFmpeg

# Docker Desktop (опционально)
winget install Docker.DockerDesktop
```

#### Вариант B: Ручная установка

1. **Go**: Скачайте с [go.dev/dl](https://go.dev/dl/) → установщик `.msi`
2. **Python**: Скачайте с [python.org](https://www.python.org/downloads/) → ✅ отметьте "Add to PATH"
3. **FFmpeg**: 
   - Скачайте с [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) (release build)
   - Распакуйте в `C:\ffmpeg`
   - Добавьте `C:\ffmpeg\bin` в PATH:
     ```
     Параметры системы → Переменные среды → Path → Создать → C:\ffmpeg\bin
     ```

#### Проверка (PowerShell)

```powershell
go version
python --version
ffmpeg -version
```

---

## 3. Клонирование и структура проекта

```bash
# Клонируйте репозиторий
git clone https://github.com/YOUR_USERNAME/video-editor.git
cd video-editor

# Или создайте структуру вручную:
mkdir -p video-editor/{engine,gui}
cd video-editor
```

### Ожидаемая структура

```
video-editor/
├── engine/                     # Go бэкенд
│   ├── main.go                # Точка входа
│   ├── go.mod                 # Go модуль
│   ├── Dockerfile             # Контейнер
│   ├── handlers/              # API обработчики
│   │   ├── health.go
│   │   ├── trim.go
│   │   ├── merge.go
│   │   ├── watermark.go
│   │   └── status.go
│   ├── worker/                # Пул воркеров
│   │   └── pool.go
│   └── ffmpeg/                # Обёртка FFmpeg
│       └── wrapper.go
├── gui/                        # Python фронтенд
│   ├── main.py                # Точка входа
│   ├── api_client.py          # HTTP клиент
│   ├── requirements.txt       # Зависимости
│   └── ui/
│       ├── __init__.py
│       └── main_window.py     # Главное окно
├── Makefile                    # Команды сборки
├── README.md
└── SETUP.md                   # Эта инструкция
```

---

## 4. Запуск Go-движка (локально)

### Шаг 1: Перейдите в директорию engine

```bash
cd engine/
```

### Шаг 2: Скачайте зависимости

```bash
go mod download
```

Это загрузит:
- `github.com/gin-gonic/gin` — HTTP фреймворк
- `github.com/google/uuid` — генерация UUID

### Шаг 3: Запустите сервер

```bash
go run main.go
```

Вы должны увидеть:

```
[GIN-debug] Listening and serving HTTP on :8080
🎬 Engine starting on :8080 (workers: 4)
🔧 Worker pool started: 4 workers
```

### Шаг 4: Проверьте работоспособность

Откройте другой терминал:

```bash
curl http://localhost:8080/api/health
```

Ожидаемый ответ:

```json
{
  "ffmpeg_available": true,
  "ffmpeg_version": "ffmpeg version 6.0 ...",
  "go_version": "go1.22.0",
  "goroutines": 8,
  "status": "running"
}
```

### Сборка бинарника (опционально)

```bash
# Создать бинарник
go build -o ../bin/video-engine .

# Запустить бинарник
../bin/video-engine
```

### Переменные окружения

| Переменная | Значение по умолчанию | Описание |
|------------|----------------------|----------|
| `PORT` | `8080` | Порт HTTP сервера |
| `WORKER_POOL_SIZE` | `4` | Количество воркеров |

```bash
# Пример: запустить на порту 9090 с 8 воркерами
PORT=9090 WORKER_POOL_SIZE=8 go run main.go
```

---

## 5. Запуск Go-движка (Docker)

### Шаг 1: Соберите Docker-образ

```bash
cd engine/
docker build -t video-editor-engine .
```

Это создаст образ на базе Alpine Linux с Go-бинарником и FFmpeg.

### Шаг 2: Запустите контейнер

```bash
docker run -d \
  --name video-engine \
  -p 8080:8080 \
  -v $(pwd)/output:/app/output \
  video-editor-engine
```

**Параметры:**
- `-d` — фоновый режим
- `--name video-engine` — имя контейнера
- `-p 8080:8080` — проброс порта
- `-v $(pwd)/output:/app/output` — монтирование директории для результатов

### Шаг 3: Проверьте

```bash
# Логи контейнера
docker logs -f video-engine

# Health check
curl http://localhost:8080/api/health
```

### Управление контейнером

```bash
# Остановить
docker stop video-engine

# Удалить
docker rm video-engine

# Перезапустить
docker restart video-engine

# Посмотреть все контейнеры
docker ps -a
```

### Windows (PowerShell)

```powershell
# Используйте %cd% вместо $(pwd)
docker run -d --name video-engine -p 8080:8080 -v ${PWD}\output:/app/output video-editor-engine
```

---

## 6. Настройка Python GUI

### Шаг 1: Перейдите в директорию gui

```bash
cd gui/
```

### Шаг 2: Создайте виртуальное окружение

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**

```powershell
python -m venv venv
venv\Scripts\activate
```

После активации в начале строки появится `(venv)`.

### Шаг 3: Установите зависимости

```bash
pip install -r requirements.txt
```

Установятся:
- `PySide6` — Qt для Python (GUI фреймворк)
- `requests` — HTTP клиент

### Шаг 4: Проверьте установку

```bash
python -c "import PySide6; print('PySide6 OK:', PySide6.__version__)"
python -c "import requests; print('requests OK:', requests.__version__)"
```

### Решение проблем с PySide6

**Linux — отсутствуют системные библиотеки:**

```bash
# Ubuntu/Debian
sudo apt install -y libxcb-xinerama0 libxcb-cursor0 libegl1

# Fedora
sudo dnf install -y libxcb xcb-util-cursor mesa-libEGL
```

**macOS — проблемы с Qt:**

```bash
# Если не запускается, попробуйте:
pip install --force-reinstall PySide6
```

**Windows — DLL ошибки:**

```powershell
# Установите Visual C++ Redistributable:
# https://aka.ms/vs/17/release/vc_redist.x64.exe
```

---

## 7. Запуск GUI

### Предварительные условия

✅ Go-движок запущен (порт 8080)  
✅ Python виртуальное окружение активировано  
✅ Зависимости установлены

### Запуск

```bash
# Убедитесь, что вы в директории gui/ и venv активирован
python main.py
```

### Что произойдёт

1. Откроется окно приложения с тёмной монохромной темой
2. В верхнем правом углу появится индикатор подключения:
   - `● connected` (белый) — движок доступен
   - `● disconnected` (серый) — движок не запущен
3. Интерфейс готов к работе

### Использование GUI

#### Обрезка видео (TRIM)

1. Нажмите **"+ ADD"** → выберите видеофайл
2. Файл появится в списке и загрузится в предпросмотр
3. Нажмите **▶** для воспроизведения
4. Перейдите к нужному моменту, запишите время
5. Во вкладке **TRIM** укажите START и END (в секундах)
6. Нажмите **"RENDER"**
7. Прогресс отобразится внизу окна

#### Склейка видео (MERGE)

1. Нажмите **"+ ADD"** → выберите 2+ видеофайлов
2. Перейдите во вкладку **MERGE**
3. Нажмите **"RENDER"**
4. Файлы будут склеены в порядке списка

#### Размытие водяного знака (WATERMARK)

1. Добавьте видеофайл
2. Перейдите во вкладку **WATERMARK**
3. Укажите координаты области:
   - **X, Y** — позиция левого верхнего угла (в пикселях)
   - **W, H** — ширина и высота области
   - **BLUR** — сила размытия (1–50)
4. Нажмите **"RENDER"**

### Выход из GUI

- Закройте окно (кнопка ✕)
- Или нажмите `Ctrl+Q` / `Cmd+Q`

---

## 8. Тестирование API

### Health Check

```bash
curl http://localhost:8080/api/health | jq .
```

### Trim (обрезка)

```bash
curl -X POST http://localhost:8080/api/trim \
  -H "Content-Type: application/json" \
  -d '{
    "inputPath": "/path/to/video.mp4",
    "startTime": 5.0,
    "endTime": 15.0
  }'
```

Ответ:

```json
{
  "job_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "message": "Trim job submitted successfully",
  "status": "queued"
}
```

### Merge (склейка)

```bash
curl -X POST http://localhost:8080/api/merge \
  -H "Content-Type: application/json" \
  -d '{
    "inputPaths": [
      "/path/to/clip1.mp4",
      "/path/to/clip2.mp4",
      "/path/to/clip3.mp4"
    ]
  }'
```

### Watermark Blur (размытие водяного знака)

```bash
curl -X POST http://localhost:8080/api/watermark-blur \
  -H "Content-Type: application/json" \
  -d '{
    "inputPath": "/path/to/video.mp4",
    "x": 10,
    "y": 10,
    "w": 200,
    "h": 60,
    "blurStrength": 15
  }'
```

### Status (прогресс задачи)

```bash
# Замените {job_id} на реальный ID из ответа
curl http://localhost:8080/api/status/a1b2c3d4-e5f6-7890-abcd-ef1234567890 | jq .
```

Ответ:

```json
{
  "created_at": "2024-01-15T10:30:00Z",
  "error": "",
  "finished_at": null,
  "job_id": "a1b2c3d4-...",
  "output": "./output/trim_a1b2c3d4.mp4",
  "progress": 45.5,
  "started_at": "2024-01-15T10:30:01Z",
  "status": "processing",
  "type": "trim"
}
```

### Автоматический polling прогресса

```bash
# Бесконечный опрос каждые 2 секунды
JOB_ID="ваш-job-id"
while true; do
  curl -s http://localhost:8080/api/status/$JOB_ID | jq '{status, progress}'
  sleep 2
done
```

---

## 9. Полный запуск (все в одном)

### Вариант A: Два терминала

**Терминал 1 — Движок:**

```bash
cd engine/
go run main.go
```

**Терминал 2 — GUI:**

```bash
cd gui/
source venv/bin/activate  # или venv\Scripts\activate на Windows
python main.py
```

### Вариант B: Через Makefile

```bash
# Терминал 1
make engine-run

# Терминал 2
make gui-run
```

### Вариант C: Docker + GUI

```bash
# Терминал 1
make docker-run

# Терминал 2
make gui-run
```

### Вариант D: Скрипт запуска (создайте `start.sh`)

```bash
#!/bin/bash
# start.sh — Запуск всего проекта

echo "🎬 Starting Video Editor..."

# Запуск Go engine в фоне
cd engine/
go run main.go &
ENGINE_PID=$!
cd ..

# Ожидание запуска движка
echo "⏳ Waiting for engine..."
sleep 3

# Проверка здоровья
if curl -s http://localhost:8080/api/health | grep -q "running"; then
    echo "✅ Engine is running"
else
    echo "❌ Engine failed to start"
    kill $ENGINE_PID
    exit 1
fi

# Запуск GUI
cd gui/
source venv/bin/activate
python main.py

# Остановка engine при выходе из GUI
kill $ENGINE_PID
echo "👋 Shutdown complete"
```

```bash
chmod +x start.sh
./start.sh
```

---

## 10. Решение проблем

### ❌ "Cannot connect to engine"

**Причина:** Go-движок не запущен.

**Решение:**

```bash
# Проверьте, что движок запущен
curl http://localhost:8080/api/health

# Если не отвечает — запустите:
cd engine && go run main.go
```

### ❌ "ffmpeg: command not found"

**Причина:** FFmpeg не установлен или не в PATH.

**Решение:**

```bash
# Проверка
which ffmpeg  # Linux/macOS
where ffmpeg  # Windows

# Установка
# macOS: brew install ffmpeg
# Ubuntu: sudo apt install ffmpeg
# Windows: winget install Gyan.FFmpeg + перезапуск терминала
```

### ❌ "module not found: PySide6"

**Причина:** Не установлено или venv не активирован.

**Решение:**

```bash
# Активируйте venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Переустановите
pip install --force-reinstall PySide6
```

### ❌ "Permission denied: ./output/"

**Причина:** Нет прав на запись в директорию output.

**Решение:**

```bash
# Создайте директорию вручную
mkdir -p engine/output
chmod 755 engine/output
```

### ❌ Docker: "port is already allocated"

**Причина:** Порт 8080 занят.

**Решение:**

```bash
# Найдите процесс
lsof -i :8080  # Linux/macOS
netstat -ano | findstr :8080  # Windows

# Или используйте другой порт
docker run -d -p 9090:8080 video-editor-engine
# GUI: измените base_url в api_client.py
```

### ❌ Видео не воспроизводится в превью

**Причина:** Неподдерживаемый кодек.

**Решение:**

```bash
# Конвертируйте в H.264/AAC
ffmpeg -i input.avi -c:v libx264 -c:a aac output.mp4
```

### ❌ "go: command not found"

**Причина:** Go не установлен или не в PATH.

**Решение:**

```bash
# Linux: добавьте в ~/.bashrc
export PATH=$PATH:/usr/local/go/bin
source ~/.bashrc

# Windows: перезапустите PowerShell после установки
```

### ❌ GUI не открывается (Linux)

**Причина:** Отсутствуют Qt-библиотеки.

**Решение:**

```bash
sudo apt install -y \
    libxcb-xinerama0 \
    libxcb-cursor0 \
    libegl1 \
    libxkbcommon0 \
    libfontconfig1
```

### ❌ Рендер зависает на 0%

**Причина:** FFmpeg не может прочитать файл.

**Решение:**

```bash
# Проверьте файл напрямую
ffmpeg -i /path/to/video.mp4

# Проверьте логи движка (терминал где запущен engine)
# Ошибка будет видна в выводе
```

---

## 11. Разработка и отладка

### Запуск в режиме разработки

```bash
# Engine с автоперезагрузкой (установите air)
go install github.com/cosmtrek/air@latest
cd engine && air

# GUI с подробными логами
cd gui && python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from main import main
main()
"
```

### Тестирование API с тестовым видео

```bash
# Создайте тестовое видео (10 секунд, цветные полосы)
ffmpeg -f lavfi -i testsrc=duration=10:size=1280x720:rate=30 \
  -f lavfi -i sine=frequency=1000:duration=10 \
  -c:v libx264 -c:a aac -shortest test_video.mp4

# Используйте его для тестов
curl -X POST http://localhost:8080/api/trim \
  -H "Content-Type: application/json" \
  -d '{"inputPath":"./test_video.mp4","startTime":2.0,"endTime":8.0}'
```

### Отладка Go

```bash
# Установите delve
go install github.com/go-delve/delve/cmd/dlv@latest

# Запуск с отладчиком
cd engine
dlv debug main.go
```

### Отладка Python

```bash
# Запуск с отладчиком (установите debugpy)
pip install debugpy
python -m debugpy --listen 5678 --wait-for-client main.py

# Подключитесь из VS Code
```

### Логи

**Engine логи** — выводятся в терминал где запущен `go run main.go`

**FFmpeg логи** — видны в engine логах при ошибках

**GUI логи** — выводятся в терминал где запущен `python main.py`

### Полезные команды

```bash
# Проверить все зависимости Go
cd engine && go mod verify

# Форматирование кода Go
cd engine && go fmt ./...

# Проверка Python кода
pip install flake8
cd gui && flake8 .

# Очистка артефактов
make clean

# Запуск тестов (если есть)
make test
```

---

## 📞 Поддержка

Если столкнулись с проблемой, которой нет в этом руководстве:

1. Проверьте логи (engine и GUI)
2. Убедитесь, что все зависимости установлены правильных версий
3. Попробуйте пересобрать: `make clean && make all`
4. Проверьте, что FFmpeg доступен: `ffmpeg -version`

---

## ✅ Чеклист перед запуском

- [ ] Go 1.21+ установлен (`go version`)
- [ ] Python 3.10+ установлен (`python --version`)
- [ ] FFmpeg установлен (`ffmpeg -version`)
- [ ] Проект клонирован/скопирован
- [ ] Go зависимости скачаны (`go mod download`)
- [ ] Python venv создан и активирован
- [ ] Python зависимости установлены (`pip install -r requirements.txt`)
- [ ] Engine запущен (`go run main.go`)
- [ ] Health check проходит (`curl localhost:8080/api/health`)
- [ ] GUI запущен (`python main.py`)
- [ ] В GUI виден индикатор "connected"

**Всё готово! 🎬**
