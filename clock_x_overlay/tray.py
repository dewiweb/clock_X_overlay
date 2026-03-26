from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from PyQt6.QtCore import Qt, QRect


def _make_tray_icon() -> QIcon:
    pix = QPixmap(32, 32)
    pix.fill(Qt.GlobalColor.transparent)
    p = QPainter(pix)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setBrush(QColor("#89b4fa"))
    p.setPen(Qt.PenStyle.NoPen)
    p.drawEllipse(1, 1, 30, 30)
    p.setPen(QColor("#1e1e2e"))
    font = QFont("Monospace", 9, QFont.Weight.Bold)
    p.setFont(font)
    p.drawText(QRect(1, 1, 30, 30), Qt.AlignmentFlag.AlignCenter, "⏰")
    p.end()
    return QIcon(pix)


class TrayIcon(QSystemTrayIcon):
    def __init__(self, overlay, settings_dialog_factory, app: QApplication):
        super().__init__(_make_tray_icon(), app)
        self._overlay = overlay
        self._settings_factory = settings_dialog_factory
        self._settings_win = None
        self.setToolTip("Clock X Overlay")
        self._build_menu()
        self.activated.connect(self._on_activated)

    def _build_menu(self):
        menu = QMenu()
        menu.setStyleSheet("""
            QMenu {
                background-color: #1e1e2e; color: #cdd6f4;
                border: 1px solid #45475a; border-radius: 6px;
                padding: 4px;
            }
            QMenu::item { padding: 6px 24px 6px 12px; border-radius: 4px; }
            QMenu::item:selected { background-color: #89b4fa; color: #1e1e2e; }
            QMenu::separator { height: 1px; background: #45475a; margin: 4px 8px; }
        """)

        self._act_toggle = menu.addAction("🙈  Masquer l'horloge")
        self._act_toggle.triggered.connect(self._toggle_overlay)

        menu.addSeparator()

        act_settings = menu.addAction("⚙️  Paramètres…")
        act_settings.triggered.connect(self._open_settings)

        menu.addSeparator()

        act_quit = menu.addAction("✖  Quitter")
        act_quit.triggered.connect(QApplication.quit)

        self.setContextMenu(menu)

    def _on_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self._toggle_overlay()

    def _toggle_overlay(self):
        if self._overlay.isVisible():
            self._overlay.hide()
            self._act_toggle.setText("👁  Afficher l'horloge")
        else:
            self._overlay.show()
            self._act_toggle.setText("🙈  Masquer l'horloge")

    def _open_settings(self):
        if self._settings_win is None or not self._settings_win.isVisible():
            self._settings_win = self._settings_factory()
            self._settings_win.config_changed.connect(self._on_config_changed)
            self._settings_win.show()
            self._settings_win.raise_()
        else:
            self._settings_win.raise_()
            self._settings_win.activateWindow()

    def _on_config_changed(self, cfg: dict):
        self._overlay.update_config(cfg)
