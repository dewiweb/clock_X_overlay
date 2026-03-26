import json
import os
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "clock_x_overlay"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULTS = {
    "font_family": "Monospace",
    "font_size": 48,
    "font_bold": True,
    "font_italic": False,
    "text_color": "#FFFFFF",
    "bg_color": "#000000",
    "bg_enabled": True,
    "bg_opacity": 140,
    "text_opacity": 255,
    "time_format": "%H:%M:%S",
    "show_seconds": True,
    "pos_x": 50,
    "pos_y": 50,
    "screen_index": 0,
    "always_on_top": True,
    "click_through": True,
    "padding_h": 16,
    "padding_v": 8,
    "border_radius": 10,
    "visible": True,
}


def load() -> dict:
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            merged = dict(DEFAULTS)
            merged.update(data)
            return merged
        except Exception:
            pass
    return dict(DEFAULTS)


def save(cfg: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
