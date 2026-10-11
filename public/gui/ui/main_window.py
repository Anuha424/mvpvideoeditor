"""
Main Window — Minimalist Monochrome Video Editor GUI
With QThread for non-blocking operations, event logger, and preview.
"""

import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QProgressBar,
    QDoubleSpinBox, QSpinBox, QListWidget, QListWidgetItem,
    QStatusBar, QMessageBox, QSlider, QTabWidget, QFrame,
    QTextEdit, QSizePolicy
)
from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget

from api_client import EngineClient, HealthCheckThread, SubmitJobThread, PollJobThread


class MainWindow(QMainWindow):
    """Main application window with monochrome design."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("VIDEO EDITOR")
        self.setMinimumSize(1100, 700)
        self.resize(1300, 800)

        # State
        self.engine = EngineClient()
        self.current_job_id = None
        self.video_files = []
        self._duration_connected = False

        # Threads
        self.health_thread = None
        self.submit_thread = None
        self.poll_thread = None

        # Build UI
        self._build_ui()
        self._setup_timers()
        self._log("Application started")

    # ─── UI Construction ─────────────────────────────────────────────────────

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Top bar
        topbar = self._build_topbar()
        root.addWidget(topbar)

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setObjectName("separator")
        root.addWidget(sep)

        # Main content
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Left sidebar
        sidebar = self._build_sidebar()
        sidebar.setFixedWidth(360)
        content_layout.addWidget(sidebar)

        # Vertical separator
        vsep = QFrame()
        vsep.setFrameShape(QFrame.VLine)
        vsep.setObjectName("separator")
        vsep.setFixedWidth(1)
        content_layout.addWidget(vsep)

        # Right area (preview + logger)
        right_panel = self._build_right_panel()
        content_layout.addWidget(right_panel, 1)

        root.addWidget(content, 1)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("ready")

    def _build_topbar(self) -> QWidget:
        topbar = QWidget()
        topbar.setFixedHeight(52)
        layout = QHBoxLayout(topbar)
        layout.setContentsMargins(20, 0, 20, 0)

        # Title
        title = QLabel("VIDEO EDITOR")
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        layout.addStretch()

        # Connection indicator
        self.conn_dot = QLabel("●")
        self.conn_dot.setStyleSheet("color: #333333; font-size: 12px;")
        layout.addWidget(self.conn_dot)

        self.conn_label = QLabel("disconnected")
        self.conn_label.setObjectName("statusLabel")
        layout.addWidget(self.conn_label)

        return topbar

    def _build_sidebar(self) -> QWidget:
        sidebar = QWidget()
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        # ── Files Section ────────────────────────────────────────────────
        section_files = QLabel("FILES")
        section_files.setObjectName("sectionLabel")
        layout.addWidget(section_files)

        self.file_list = QListWidget()
        self.file_list.setMaximumHeight(150)
        layout.addWidget(self.file_list)

        file_btns = QHBoxLayout()
        
        self.btn_add = QPushButton("+ ADD FILES")
        self.btn_add.setToolTip("Select video files from your computer")
        self.btn_add.clicked.connect(self._add_files)
        file_btns.addWidget(self.btn_add)

        self.btn_remove = QPushButton("− REMOVE")
        self.btn_remove.setToolTip("Remove selected file from list")
        self.btn_remove.clicked.connect(self._remove_selected)
        file_btns.addWidget(self.btn_remove)
        
        layout.addLayout(file_btns)

        # ── Separator ────────────────────────────────────────────────────
        sep1 = QFrame()
        sep1.setFrameShape(QFrame.HLine)
        sep1.setObjectName("separator")
        layout.addWidget(sep1)

        # ── Tabs ─────────────────────────────────────────────────────────
        self.tabs = QTabWidget()
        self.tabs.addTab(self._build_trim_tab(), "TRIM")
        self.tabs.addTab(self._build_merge_tab(), "MERGE")
        self.tabs.addTab(self._build_watermark_tab(), "WATERMARK")
        layout.addWidget(self.tabs)

        layout.addStretch()

        # ── Render Button ────────────────────────────────────────────────
        self.btn_render = QPushButton("▶ RENDER")
        self.btn_render.setObjectName("primaryButton")
        self.btn_render.setToolTip("Start rendering process")
        self.btn_render.clicked.connect(self._start_render)
        layout.addWidget(self.btn_render)

        # ── Progress ─────────────────────────────────────────────────────
        progress_group = QGroupBox("PROGRESS")
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)

        self.progress_label = QLabel("IDLE")
        self.progress_label.setObjectName("statusLabel")
        self.progress_label.setAlignment(Qt.AlignCenter)
        progress_layout.addWidget(self.progress_label)

        layout.addWidget(progress_group)

        return sidebar

    def _build_trim_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(12, 16, 12, 12)
        layout.setSpacing(12)

        desc = QLabel("Cut video by timecodes")
        desc.setObjectName("statusLabel")
        layout.addWidget(desc)

        # Start time
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("START"))
        self.start_time = QDoubleSpinBox()
        self.start_time.setRange(0, 99999)
        self.start_time.setDecimals(2)
        self.start_time.setSuffix("s")
        self.start_time.setSingleStep(0.5)
        self.start_time.setToolTip("Start time in seconds")
        row1.addWidget(self.start_time)
        layout.addLayout(row1)

        # End time
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("END"))
        self.end_time = QDoubleSpinBox()
        self.end_time.setRange(0, 99999)
        self.end_time.setDecimals(2)
        self.end_time.setSuffix("s")
        self.end_time.setValue(10.0)
        self.end_time.setSingleStep(0.5)
        self.end_time.setToolTip("End time in seconds")
        row2.addWidget(self.end_time)
        layout.addLayout(row2)

        layout.addStretch()
        return widget

    def _build_merge_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(12, 16, 12, 12)

        desc = QLabel("Add 2+ files to concatenate them in order")
        desc.setObjectName("statusLabel")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        layout.addStretch()
        return widget

    def _build_watermark_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(12, 16, 12, 12)
        layout.setSpacing(10)

        desc = QLabel("Blur/hide watermark region")
        desc.setObjectName("statusLabel")
        layout.addWidget(desc)

        # X, Y coordinates
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("X"))
        self.wm_x = QSpinBox()
        self.wm_x.setRange(0, 9999)
        self.wm_x.setSuffix("px")
        self.wm_x.setToolTip("X coordinate (left edge)")
        row1.addWidget(self.wm_x)
        row1.addWidget(QLabel("Y"))
        self.wm_y = QSpinBox()
        self.wm_y.setRange(0, 9999)
        self.wm_y.setSuffix("px")
        self.wm_y.setToolTip("Y coordinate (top edge)")
        row1.addWidget(self.wm_y)
        layout.addLayout(row1)

        # W, H dimensions
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("W"))
        self.wm_w = QSpinBox()
        self.wm_w.setRange(1, 9999)
        self.wm_w.setValue(200)
        self.wm_w.setSuffix("px")
        self.wm_w.setToolTip("Width of watermark region")
        row2.addWidget(self.wm_w)
        row2.addWidget(QLabel("H"))
        self.wm_h = QSpinBox()
        self.wm_h.setRange(1, 9999)
        self.wm_h.setValue(60)
        self.wm_h.setSuffix("px")
        self.wm_h.setToolTip("Height of watermark region")
        row2.addWidget(self.wm_h)
        layout.addLayout(row2)

        # Blur strength
        row3 = QHBoxLayout()
        row3.addWidget(QLabel("BLUR"))
        self.wm_blur = QSpinBox()
        self.wm_blur.setRange(1, 50)
        self.wm_blur.setValue(10)
        self.wm_blur.setToolTip("Blur strength (1-50)")
        row3.addWidget(self.wm_blur)
        layout.addLayout(row3)

        # Strength slider
        self.blur_slider = QSlider(Qt.Horizontal)
        self.blur_slider.setRange(1, 50)
        self.blur_slider.setValue(10)
        self.blur_slider.setToolTip("Adjust blur strength")
        self.blur_slider.valueChanged.connect(lambda v: self.wm_blur.setValue(v))
        self.wm_blur.valueChanged.connect(lambda v: self.blur_slider.setValue(v))
        layout.addWidget(self.blur_slider)

        layout.addStretch()
        return widget

    def _build_right_panel(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Video preview
        self.video_widget = QVideoWidget()
        self.video_widget.setMinimumHeight(350)
        self.video_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.video_widget, 1)

        # Playback controls
        controls = QWidget()
        controls.setFixedHeight(48)
        controls.setStyleSheet("background-color: #050505;")
        ctrl_layout = QHBoxLayout(controls)
        ctrl_layout.setContentsMargins(16, 0, 16, 0)

        self.btn_play = QPushButton("▶")
        self.btn_play.setFixedSize(36, 36)
        self.btn_play.setToolTip("Play/Pause video")
        self.btn_play.clicked.connect(self._toggle_playback)
        ctrl_layout.addWidget(self.btn_play)

        self.btn_stop = QPushButton("■")
        self.btn_stop.setFixedSize(36, 36)
        self.btn_stop.setToolTip("Stop playback")
        self.btn_stop.clicked.connect(self._stop_playback)
        ctrl_layout.addWidget(self.btn_stop)

        # Position slider
        self.pos_slider = QSlider(Qt.Horizontal)
        self.pos_slider.setRange(0, 0)
        self.pos_slider.setToolTip("Seek through video")
        self.pos_slider.sliderMoved.connect(self._on_seek)
        ctrl_layout.addWidget(self.pos_slider)

        # Time display
        self.time_label = QLabel("00:00 / 00:00")
        self.time_label.setObjectName("statusLabel")
        self.time_label.setMinimumWidth(110)
        self.time_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        ctrl_layout.addWidget(self.time_label)

        layout.addWidget(controls)

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setObjectName("separator")
        layout.addWidget(sep)

        # Event logger
        logger_group = QWidget()
        logger_group.setFixedHeight(120)
        logger_layout = QVBoxLayout(logger_group)
        logger_layout.setContentsMargins(12, 8, 12, 8)

        logger_title = QLabel("EVENT LOG")
        logger_title.setObjectName("sectionLabel")
        logger_layout.addWidget(logger_title)

        self.logger = QTextEdit()
        self.logger.setObjectName("logger")
        self.logger.setReadOnly(True)
        self.logger.setMaximumHeight(80)
        logger_layout.addWidget(self.logger)

        layout.addWidget(logger_group)

        # Media player
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.positionChanged.connect(self._on_position_changed)

        return widget

    # ─── Event Logger ────────────────────────────────────────────────────────

    def _log(self, message: str):
        """Add message to event logger."""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.logger.append(f"[{timestamp}] {message}")
        # Auto-scroll to bottom
        scrollbar = self.logger.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    # ─── Timers ──────────────────────────────────────────────────────────────

    def _setup_timers(self):
        # Health check
        self.health_timer = QTimer()
        self.health_timer.timeout.connect(self._check_connection)
        self.health_timer.start(3000)

        # Progress polling
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self._poll_progress)

        # Initial check
        self._check_connection()

    # ─── Connection ──────────────────────────────────────────────────────────

    def _check_connection(self):
        """Check connection in background thread."""
        if self.health_thread and self.health_thread.isRunning():
            return
        
        self.health_thread = HealthCheckThread(self.engine)
        self.health_thread.finished.connect(self._on_health_check)
        self.health_thread.start()

    def _on_health_check(self, result: dict):
        """Handle health check result."""
        if result.get("status") == "running":
            self.conn_dot.setStyleSheet("color: #ffffff; font-size: 12px;")
            self.conn_label.setText("connected")
        else:
            self.conn_dot.setStyleSheet("color: #333333; font-size: 12px;")
            self.conn_label.setText("disconnected")

    # ─── File Management ─────────────────────────────────────────────────────

    def _add_files(self):
        """Open file dialog to add video files."""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Video Files",
            os.path.expanduser("~"),
            "Video Files (*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm *.ts *.m4v);;All Files (*)"
        )
        
        for file_path in files:
            if file_path not in self.video_files:
                self.video_files.append(file_path)
                item = QListWidgetItem(os.path.basename(file_path))
                item.setData(Qt.UserRole, file_path)
                item.setToolTip(file_path)
                self.file_list.addItem(item)

        # Load first file in preview
        if self.video_files:
            self._load_preview(self.video_files[0])

        count = len(self.video_files)
        self._log(f"Loaded {count} file{'s' if count != 1 else ''}")
        self.status_bar.showMessage(f"{count} file{'s' if count != 1 else ''} loaded")

    def _remove_selected(self):
        """Remove selected file from list."""
        row = self.file_list.currentRow()
        if 0 <= row < len(self.video_files):
            self.file_list.takeItem(row)
            self.video_files.pop(row)
            self._log("File removed")

    def _load_preview(self, file_path: str):
        """Load video file into preview player."""
        url = QUrl.fromLocalFile(file_path)
        self.media_player.setSource(url)
        self.media_player.pause()
        self._log(f"Preview: {os.path.basename(file_path)}")

        # Connect duration signal only once
        if not self._duration_connected:
            self.media_player.durationChanged.connect(self._on_duration_changed)
            self._duration_connected = True

    # ─── Playback ────────────────────────────────────────────────────────────

    def _on_duration_changed(self, duration_ms: int):
        """Handle video duration change."""
        duration_sec = duration_ms / 1000.0
        self.end_time.setValue(duration_sec)
        self.pos_slider.setRange(0, max(1, duration_ms))
        self._update_time_display(0, duration_ms)

    def _on_position_changed(self, position_ms: int):
        """Handle position change during playback."""
        self.pos_slider.setValue(position_ms)
        duration_ms = self.media_player.duration()
        self._update_time_display(position_ms, duration_ms)

    def _on_seek(self, position_ms: int):
        """Handle seek slider."""
        self.media_player.setPosition(position_ms)

    def _update_time_display(self, current_ms: int, total_ms: int):
        """Update time display label."""
        current_s = current_ms // 1000
        total_s = total_ms // 1000
        self.time_label.setText(
            f"{current_s // 60:02d}:{current_s % 60:02d} / {total_s // 60:02d}:{total_s % 60:02d}"
        )

    def _toggle_playback(self):
        """Toggle play/pause."""
        if self.media_player.playbackState() == QMediaPlayer.PlayingState:
            self.media_player.pause()
            self.btn_play.setText("▶")
        else:
            self.media_player.play()
            self.btn_play.setText("⏸")

    def _stop_playback(self):
        """Stop playback."""
        self.media_player.stop()
        self.btn_play.setText("▶")

    # ─── Rendering ───────────────────────────────────────────────────────────

    def _start_render(self):
        """Start rendering process in background thread."""
        if not self.video_files:
            QMessageBox.warning(self, "No Files", "Add video files first.")
            return

        current_tab = self.tabs.currentIndex()
        endpoint = ""
        payload = {}

        if current_tab == 0:
            # TRIM
            endpoint = "/api/trim"
            payload = {
                "inputPath": self.video_files[0],
                "startTime": self.start_time.value(),
                "endTime": self.end_time.value(),
            }
            self._log(f"Submitting trim job: {payload['startTime']}s - {payload['endTime']}s")
        elif current_tab == 1:
            # MERGE
            if len(self.video_files) < 2:
                QMessageBox.warning(self, "Not Enough Files", "Add at least 2 files for merge.")
                return
            endpoint = "/api/merge"
            payload = {"inputPaths": self.video_files}
            self._log(f"Submitting merge job: {len(self.video_files)} files")
        elif current_tab == 2:
            # WATERMARK BLUR
            endpoint = "/api/watermark-blur"
            payload = {
                "inputPath": self.video_files[0],
                "x": self.wm_x.value(),
                "y": self.wm_y.value(),
                "w": self.wm_w.value(),
                "h": self.wm_h.value(),
                "blurStrength": self.wm_blur.value(),
            }
            self._log(f"Submitting watermark blur: ({payload['x']},{payload['y']}) {payload['w']}x{payload['h']}")

        # Submit in background thread
        self.submit_thread = SubmitJobThread(self.engine, endpoint, payload)
        self.submit_thread.finished.connect(self._on_job_submitted)
        self.submit_thread.error.connect(self._on_submit_error)
        self.submit_thread.start()

        self.btn_render.setEnabled(False)
        self.progress_bar.setValue(0)
        self.progress_label.setText("SUBMITTING...")

    def _on_job_submitted(self, result: dict):
        """Handle job submission result."""
        if "error" in result:
            QMessageBox.critical(self, "Error", f"Failed to submit job:\n{result['error']}")
            self._log(f"Error: {result['error']}")
            self.btn_render.setEnabled(True)
            self.progress_label.setText("IDLE")
            return

        self.current_job_id = result.get("job_id")
        self.progress_label.setText("QUEUED")
        self._log(f"Job submitted: {self.current_job_id}")

        # Start polling
        self.progress_timer.start(800)

    def _on_submit_error(self, error: str):
        """Handle submission error."""
        QMessageBox.critical(self, "Error", f"Submission failed:\n{error}")
        self._log(f"Error: {error}")
        self.btn_render.setEnabled(True)
        self.progress_label.setText("IDLE")

    def _poll_progress(self):
        """Poll job progress in background thread."""
        if not self.current_job_id:
            return

        if self.poll_thread and self.poll_thread.isRunning():
            return

        self.poll_thread = PollJobThread(self.engine, self.current_job_id)
        self.poll_thread.finished.connect(self._on_progress_update)
        self.poll_thread.start()

    def _on_progress_update(self, status):
        """Handle progress update."""
        pct = int(status.progress)
        self.progress_bar.setValue(pct)

        if status.status == "queued":
            self.progress_label.setText("QUEUED")
        elif status.status == "processing":
            self.progress_label.setText(f"RENDERING {pct}%")
            if pct % 10 == 0:  # Log every 10%
                self._log(f"Processing {pct}%...")
        elif status.status == "completed":
            self.progress_timer.stop()
            self.btn_render.setEnabled(True)
            self.progress_label.setText("DONE")
            self._log("✓ Rendering complete!")
            self.status_bar.showMessage("Render completed successfully!")
            QMessageBox.information(
                self, "Complete",
                f"Rendering finished!\n\nOutput:\n{status.output}"
            )
            self.current_job_id = None
        elif status.status == "failed":
            self.progress_timer.stop()
            self.btn_render.setEnabled(True)
            self.progress_label.setText("FAILED")
            self._log(f"✗ Failed: {status.error}")
            QMessageBox.critical(self, "Render Failed", f"Error:\n{status.error}")
            self.current_job_id = None
        elif status.status == "error":
            self.progress_timer.stop()
            self.btn_render.setEnabled(True)
            self.progress_label.setText("ERROR")
            self._log(f"✗ Error: {status.error}")
            self.current_job_id = None
