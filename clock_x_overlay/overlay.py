import time
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication
from PyQt6.QtCore import Qt, QTimer, QPoint, QRect
from PyQt6.QtGui import QFont, QColor, QPainter, QPainterPath, QFontMetrics


class ClockOverlay(QWidget):
    def __init__(self, cfg: dict):
        super().__init__()
        self.cfg = cfg
        self._drag_pos = None

        self._init_window()
        self._init_ui()
        self._apply_config()

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(200)
        self._tick()

    def _init_window(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
            | Qt.WindowType.BypassWindowManagerHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def _init_ui(self):
        self._label = QLabel("00:00:00", self)
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._label)
        self.setLayout(layout)

    def _apply_config(self):
        cfg = self.cfg
        font = QFont(cfg["font_family"], cfg["font_size"])
        font.setBold(cfg["font_bold"])
        font.setItalic(cfg["font_italic"])
        self._label.setFont(font)

        text_color = QColor(cfg["text_color"])
        text_color.setAlpha(cfg["text_opacity"])

        self._label.setStyleSheet(
            f"color: rgba({text_color.red()},{text_color.green()},{text_color.blue()},{text_color.alpha()});"
            f"background: transparent;"
            f"padding: {cfg['padding_v']}px {cfg['padding_h']}px;"
        )

        self._update_click_through()
        self._reposition()
        self.update()

    def _update_click_through(self):
        if self.cfg.get("click_through", True):
            self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        else:
            self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)

    def _reposition(self):
        cfg = self.cfg
        screens = QApplication.screens()
        idx = min(cfg["screen_index"], len(screens) - 1)
        screen_geo: QRect = screens[idx].geometry()

        self.adjustSize()
        w = self.sizeHint().width()
        h = self.sizeHint().height()

        x = screen_geo.x() + int((screen_geo.width() - w) * cfg["pos_x"] / 100)
        y = screen_geo.y() + int((screen_geo.height() - h) * cfg["pos_y"] / 100)
        self.move(x, y)

    def paintEvent(self, event):
        cfg = self.cfg
        if not cfg["bg_enabled"]:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        bg = QColor(cfg["bg_color"])
        bg.setAlpha(cfg["bg_opacity"])
        painter.setBrush(bg)
        painter.setPen(Qt.PenStyle.NoPen)

        radius = cfg["border_radius"]
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), radius, radius)
        painter.drawPath(path)

    def _tick(self):
        fmt = self.cfg["time_format"]
        self._label.setText(time.strftime(fmt))
        self.adjustSize()

    def update_config(self, cfg: dict):
        self.cfg = cfg
        self._apply_config()
        self._tick()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._drag_pos is not None and event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
        self._save_position()

    def _save_position(self):
        screens = QApplication.screens()
        idx = min(self.cfg["screen_index"], len(screens) - 1)
        screen_geo: QRect = screens[idx].geometry()
        pos = self.pos()
        w, h = self.width(), self.height()
        rx = (pos.x() - screen_geo.x()) / max(screen_geo.width() - w, 1) * 100
        ry = (pos.y() - screen_geo.y()) / max(screen_geo.height() - h, 1) * 100
        self.cfg["pos_x"] = max(0, min(100, round(rx, 1)))
        self.cfg["pos_y"] = max(0, min(100, round(ry, 1)))
        from . import config as cfg_mod
        cfg_mod.save(self.cfg)
