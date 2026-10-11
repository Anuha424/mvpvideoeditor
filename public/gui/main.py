"""
Video Editor GUI — Minimalist Monochrome Interface
Strictly black, white, and gray. Professional developer tool aesthetic.
"""

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from ui.main_window import MainWindow


def main():
    """Launch the Video Editor GUI application."""
    app = QApplication(sys.argv)
    app.setApplicationName("Video Editor")
    app.setApplicationVersion("0.3.0")
    app.setOrganizationName("VideoEditor")

    # Apply monochrome stylesheet
    app.setStyleSheet(MONOCHROME_STYLESHEET)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


# ─── Monochrome Stylesheet ────────────────────────────────────────────────────

MONOCHROME_STYLESHEET = """
/* ── Base ─────────────────────────────────────────── */
QMainWindow {
    background-color: #000000;
}

QWidget {
    background-color: #000000;
    color: #e0e0e0;
    font-family: 'SF Mono', 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
    font-size: 12px;
}

/* ── Labels ───────────────────────────────────────── */
QLabel {
    color: #b0b0b0;
    background: transparent;
}

QLabel#titleLabel {
    color: #ffffff;
    font-size: 16px;
    font-weight: 600;
    letter-spacing: 1px;
}

QLabel#sectionLabel {
    color: #666666;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-weight: 500;
}

QLabel#statusLabel {
    color: #666666;
    font-size: 11px;
}

QLabel#valueLabel {
    color: #ffffff;
    font-size: 12px;
    font-weight: 500;
}

/* ── Buttons ──────────────────────────────────────── */
QPushButton {
    background-color: #1a1a1a;
    border: 1px solid #333333;
    border-radius: 4px;
    padding: 8px 16px;
    color: #cccccc;
    font-size: 11px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #2a2a2a;
    border-color: #444444;
    color: #ffffff;
}

QPushButton:pressed {
    background-color: #333333;
}

QPushButton:disabled {
    background-color: #0a0a0a;
    color: #333333;
    border-color: #1a1a1a;
}

QPushButton#primaryButton {
    background-color: #ffffff;
    color: #000000;
    border: none;
    font-weight: 600;
    padding: 12px 24px;
    font-size: 13px;
}

QPushButton#primaryButton:hover {
    background-color: #e0e0e0;
}

QPushButton#primaryButton:pressed {
    background-color: #cccccc;
}

QPushButton#primaryButton:disabled {
    background-color: #333333;
    color: #666666;
}

QPushButton#actionButton {
    background-color: #1a1a1a;
    border: 1px solid #444444;
    color: #ffffff;
    font-weight: 500;
    padding: 10px 20px;
    font-size: 12px;
}

QPushButton#actionButton:hover {
    background-color: #2a2a2a;
    border-color: #555555;
}

/* ── Inputs ───────────────────────────────────────── */
QLineEdit, QSpinBox, QDoubleSpinBox {
    background-color: #0a0a0a;
    border: 1px solid #333333;
    border-radius: 3px;
    padding: 6px 10px;
    color: #ffffff;
    font-size: 12px;
}

QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
    border-color: #555555;
}

QSpinBox::up-button, QDoubleSpinBox::up-button,
QSpinBox::down-button, QDoubleSpinBox::down-button {
    background-color: #1a1a1a;
    border: none;
    width: 16px;
}

QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {
    background-color: #2a2a2a;
}

/* ── Progress Bar ─────────────────────────────────── */
QProgressBar {
    background-color: #0a0a0a;
    border: 1px solid #1a1a1a;
    border-radius: 2px;
    text-align: center;
    color: #666666;
    height: 22px;
    font-size: 10px;
}

QProgressBar::chunk {
    background-color: #ffffff;
    border-radius: 1px;
}

/* ── Group Box ────────────────────────────────────── */
QGroupBox {
    border: 1px solid #1a1a1a;
    border-radius: 6px;
    margin-top: 8px;
    padding: 16px 12px 12px 12px;
    background-color: #050505;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 8px;
    color: #666666;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

/* ── List Widget ──────────────────────────────────── */
QListWidget {
    background-color: #050505;
    border: 1px solid #1a1a1a;
    border-radius: 4px;
    padding: 2px;
    outline: none;
}

QListWidget::item {
    padding: 8px 10px;
    border-radius: 3px;
    color: #999999;
    font-size: 11px;
}

QListWidget::item:hover {
    background-color: #1a1a1a;
    color: #ffffff;
}

QListWidget::item:selected {
    background-color: #2a2a2a;
    color: #ffffff;
}

/* ── Slider ───────────────────────────────────────── */
QSlider::groove:horizontal {
    border: none;
    height: 3px;
    background: #333333;
    border-radius: 2px;
}

QSlider::handle:horizontal {
    background: #ffffff;
    border: none;
    width: 14px;
    height: 14px;
    margin: -6px 0;
    border-radius: 7px;
}

QSlider::handle:horizontal:hover {
    background: #cccccc;
}

QSlider::sub-page:horizontal {
    background: #555555;
    border-radius: 2px;
}

/* ── Scrollbar ────────────────────────────────────── */
QScrollBar:vertical {
    background: transparent;
    width: 8px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #333333;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: #555555;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    background: transparent;
    height: 8px;
    margin: 0;
}

QScrollBar::handle:horizontal {
    background: #333333;
    border-radius: 4px;
    min-width: 30px;
}

/* ── Status Bar ───────────────────────────────────── */
QStatusBar {
    background-color: #000000;
    color: #555555;
    border-top: 1px solid #1a1a1a;
    font-size: 10px;
}

/* ── Separator ────────────────────────────────────── */
QFrame#separator {
    background-color: #1a1a1a;
    max-height: 1px;
}

/* ── Tab Widget ───────────────────────────────────── */
QTabWidget::pane {
    border: 1px solid #1a1a1a;
    border-radius: 4px;
    background-color: #050505;
}

QTabBar::tab {
    background-color: #000000;
    border: 1px solid #1a1a1a;
    border-bottom: none;
    padding: 10px 20px;
    color: #666666;
    font-size: 11px;
    margin-right: 1px;
}

QTabBar::tab:selected {
    background-color: #050505;
    color: #ffffff;
    border-bottom: 2px solid #ffffff;
}

QTabBar::tab:hover {
    color: #aaaaaa;
}

/* ── Text Edit (Logger) ──────────────────────────── */
QTextEdit#logger {
    background-color: #050505;
    border: 1px solid #1a1a1a;
    border-radius: 4px;
    color: #888888;
    font-family: 'SF Mono', 'JetBrains Mono', monospace;
    font-size: 10px;
    padding: 8px;
}
"""


if __name__ == "__main__":
    main()
