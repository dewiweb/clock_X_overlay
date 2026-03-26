import sys
import os

# Required for transparent/overlay windows on X11
os.environ.setdefault("QT_XCB_GL_INTEGRATION", "none")

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from . import config as cfg_mod
from .overlay import ClockOverlay
from .settings import SettingsDialog
from .tray import TrayIcon


def main():
    # High DPI support
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("Clock X Overlay")
    app.setApplicationVersion("1.0.0")
    app.setQuitOnLastWindowClosed(False)

    cfg = cfg_mod.load()

    overlay = ClockOverlay(cfg)
    if cfg.get("visible", True):
        overlay.show()

    def make_settings():
        dlg = SettingsDialog(overlay.cfg)
        return dlg

    tray = TrayIcon(overlay, make_settings, app)
    tray.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
