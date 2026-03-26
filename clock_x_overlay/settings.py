from PyQt6.QtWidgets import (
    QDialog, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QSlider, QSpinBox, QCheckBox, QPushButton, QComboBox,
    QFontComboBox, QLineEdit, QGroupBox, QDialogButtonBox, QApplication,
    QColorDialog, QFrame,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QIcon, QPalette
from . import config as cfg_mod


class ColorButton(QPushButton):
    color_changed = pyqtSignal(str)

    def __init__(self, color: str, parent=None):
        super().__init__(parent)
        self.setFixedSize(44, 28)
        self.set_color(color)
        self.clicked.connect(self._pick)

    def set_color(self, hex_color: str):
        self._color = hex_color
        self.setStyleSheet(
            f"background-color: {hex_color}; border: 2px solid #555; border-radius: 4px;"
        )

    def color(self) -> str:
        return self._color

    def _pick(self):
        c = QColorDialog.getColor(QColor(self._color), self, "Choisir une couleur")
        if c.isValid():
            self.set_color(c.name())
            self.color_changed.emit(self._color)


class SettingsDialog(QDialog):
    config_changed = pyqtSignal(dict)

    def __init__(self, cfg: dict, parent=None):
        super().__init__(parent)
        self.cfg = dict(cfg)
        self.setWindowTitle("Clock X Overlay — Paramètres")
        self.setMinimumWidth(480)
        self.setModal(False)
        self._build_ui()
        self._load_values()
        self._apply_dark_theme()

    def _apply_dark_theme(self):
        self.setStyleSheet("""
            QDialog, QWidget { background-color: #1e1e2e; color: #cdd6f4; }
            QTabWidget::pane { border: 1px solid #45475a; border-radius: 6px; }
            QTabBar::tab {
                background: #313244; color: #cdd6f4; padding: 8px 18px;
                border-top-left-radius: 6px; border-top-right-radius: 6px;
                margin-right: 2px;
            }
            QTabBar::tab:selected { background: #89b4fa; color: #1e1e2e; font-weight: bold; }
            QTabBar::tab:hover { background: #45475a; }
            QGroupBox {
                border: 1px solid #45475a; border-radius: 6px;
                margin-top: 10px; padding: 8px;
                font-weight: bold; color: #89b4fa;
            }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 4px; }
            QLabel { color: #cdd6f4; }
            QSpinBox, QComboBox, QFontComboBox, QLineEdit {
                background: #313244; border: 1px solid #45475a;
                border-radius: 4px; padding: 3px 6px; color: #cdd6f4;
            }
            QSpinBox:focus, QComboBox:focus, QLineEdit:focus {
                border: 1px solid #89b4fa;
            }
            QSlider::groove:horizontal {
                height: 4px; background: #45475a; border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: #89b4fa; width: 14px; height: 14px;
                margin: -5px 0; border-radius: 7px;
            }
            QSlider::sub-page:horizontal { background: #89b4fa; border-radius: 2px; }
            QCheckBox { color: #cdd6f4; spacing: 6px; }
            QCheckBox::indicator {
                width: 16px; height: 16px; border-radius: 3px;
                border: 1px solid #45475a; background: #313244;
            }
            QCheckBox::indicator:checked { background: #89b4fa; border-color: #89b4fa; }
            QPushButton {
                background: #313244; border: 1px solid #45475a;
                border-radius: 6px; padding: 6px 16px; color: #cdd6f4;
            }
            QPushButton:hover { background: #45475a; }
            QPushButton:pressed { background: #89b4fa; color: #1e1e2e; }
            QDialogButtonBox QPushButton { min-width: 90px; }
        """)

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(8)

        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        self.tabs.addTab(self._tab_display(), "🖥  Affichage")
        self.tabs.addTab(self._tab_font(), "🔤  Police")
        self.tabs.addTab(self._tab_time(), "⏰  Horloge")
        self.tabs.addTab(self._tab_position(), "📐  Position")

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Apply |
            QDialogButtonBox.StandardButton.Close
        )
        buttons.button(QDialogButtonBox.StandardButton.Apply).setText("Appliquer")
        buttons.button(QDialogButtonBox.StandardButton.Close).setText("Fermer")
        buttons.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(self._apply)
        buttons.rejected.connect(self.close)
        main_layout.addWidget(buttons)

    # ── Tab: Display ─────────────────────────────────────────────────────────

    def _tab_display(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setSpacing(12)

        grp_bg = QGroupBox("Fond")
        form_bg = QFormLayout(grp_bg)
        form_bg.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.chk_bg = QCheckBox("Activer le fond")
        form_bg.addRow("", self.chk_bg)

        self.btn_bg_color = ColorButton("#000000")
        form_bg.addRow("Couleur fond :", self.btn_bg_color)

        self.sld_bg_opacity = self._make_slider(0, 255)
        self.lbl_bg_opacity = QLabel("140")
        row_bg_op = QHBoxLayout()
        row_bg_op.addWidget(self.sld_bg_opacity)
        row_bg_op.addWidget(self.lbl_bg_opacity)
        self.sld_bg_opacity.valueChanged.connect(lambda v: self.lbl_bg_opacity.setText(str(v)))
        form_bg.addRow("Opacité fond :", row_bg_op)

        self.spn_border_radius = QSpinBox()
        self.spn_border_radius.setRange(0, 60)
        form_bg.addRow("Rayon bordure :", self.spn_border_radius)

        layout.addWidget(grp_bg)

        grp_txt = QGroupBox("Texte")
        form_txt = QFormLayout(grp_txt)
        form_txt.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.btn_text_color = ColorButton("#FFFFFF")
        form_txt.addRow("Couleur texte :", self.btn_text_color)

        self.sld_text_opacity = self._make_slider(0, 255)
        self.lbl_text_opacity = QLabel("255")
        row_txt_op = QHBoxLayout()
        row_txt_op.addWidget(self.sld_text_opacity)
        row_txt_op.addWidget(self.lbl_text_opacity)
        self.sld_text_opacity.valueChanged.connect(lambda v: self.lbl_text_opacity.setText(str(v)))
        form_txt.addRow("Opacité texte :", row_txt_op)

        layout.addWidget(grp_txt)

        grp_misc = QGroupBox("Comportement")
        form_misc = QFormLayout(grp_misc)
        form_misc.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.chk_always_on_top = QCheckBox("Toujours au-dessus")
        form_misc.addRow("", self.chk_always_on_top)

        self.chk_click_through = QCheckBox("Click-through (souris traversante)")
        form_misc.addRow("", self.chk_click_through)

        layout.addWidget(grp_misc)
        layout.addStretch()
        return w

    # ── Tab: Font ─────────────────────────────────────────────────────────────

    def _tab_font(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setSpacing(12)

        grp = QGroupBox("Police")
        form = QFormLayout(grp)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.cmb_font = QFontComboBox()
        form.addRow("Famille :", self.cmb_font)

        self.spn_font_size = QSpinBox()
        self.spn_font_size.setRange(8, 300)
        form.addRow("Taille :", self.spn_font_size)

        self.chk_bold = QCheckBox("Gras")
        self.chk_italic = QCheckBox("Italique")
        row_style = QHBoxLayout()
        row_style.addWidget(self.chk_bold)
        row_style.addWidget(self.chk_italic)
        row_style.addStretch()
        form.addRow("Style :", row_style)

        grp_pad = QGroupBox("Marges internes")
        form_pad = QFormLayout(grp_pad)
        form_pad.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.spn_pad_h = QSpinBox()
        self.spn_pad_h.setRange(0, 80)
        form_pad.addRow("Horizontale (px) :", self.spn_pad_h)

        self.spn_pad_v = QSpinBox()
        self.spn_pad_v.setRange(0, 80)
        form_pad.addRow("Verticale (px) :", self.spn_pad_v)

        layout.addWidget(grp)
        layout.addWidget(grp_pad)

        self._preview = QLabel("12:34:56")
        self._preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._preview.setMinimumHeight(80)
        self._preview.setStyleSheet(
            "background: #11111b; border: 1px solid #45475a; border-radius: 8px;"
        )
        layout.addWidget(QLabel("Aperçu :"))
        layout.addWidget(self._preview)

        for w_ in [self.cmb_font, self.spn_font_size, self.chk_bold, self.chk_italic,
                   self.btn_text_color, self.sld_text_opacity]:
            try:
                w_.currentFontChanged.connect(self._update_preview)
            except AttributeError:
                pass
            try:
                w_.valueChanged.connect(self._update_preview)
            except AttributeError:
                pass
            try:
                w_.stateChanged.connect(self._update_preview)
            except AttributeError:
                pass
            try:
                w_.color_changed.connect(self._update_preview)
            except AttributeError:
                pass

        layout.addStretch()
        return w

    # ── Tab: Time ─────────────────────────────────────────────────────────────

    def _tab_time(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setSpacing(12)

        grp = QGroupBox("Format de l'heure")
        form = QFormLayout(grp)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.cmb_format = QComboBox()
        self.cmb_format.addItems([
            "%H:%M:%S",
            "%H:%M",
            "%I:%M:%S %p",
            "%I:%M %p",
            "%H:%M:%S — %A %d %B %Y",
            "%H:%M — %d/%m/%Y",
            "Personnalisé…",
        ])
        self.cmb_format.currentIndexChanged.connect(self._on_format_changed)
        form.addRow("Préréglage :", self.cmb_format)

        self.edt_format = QLineEdit()
        self.edt_format.setPlaceholderText("ex: %H:%M:%S")
        form.addRow("Format (strftime) :", self.edt_format)

        hint = QLabel(
            "<small>%H=heure 24h &nbsp; %I=heure 12h &nbsp; %M=minutes &nbsp; %S=secondes<br>"
            "%p=AM/PM &nbsp; %A=jour &nbsp; %d=date &nbsp; %B=mois &nbsp; %Y=année</small>"
        )
        hint.setTextFormat(Qt.TextFormat.RichText)
        hint.setStyleSheet("color: #6c7086; padding-top: 4px;")
        form.addRow("", hint)

        layout.addWidget(grp)
        layout.addStretch()
        return w

    # ── Tab: Position ─────────────────────────────────────────────────────────

    def _tab_position(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setSpacing(12)

        grp_screen = QGroupBox("Écran")
        form_s = QFormLayout(grp_screen)
        form_s.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.cmb_screen = QComboBox()
        screens = QApplication.screens()
        for i, s in enumerate(screens):
            g = s.geometry()
            self.cmb_screen.addItem(f"Écran {i+1} — {g.width()}×{g.height()} @ ({g.x()},{g.y()})")
        form_s.addRow("Écran cible :", self.cmb_screen)

        layout.addWidget(grp_screen)

        grp_pos = QGroupBox("Position (% de l'écran)")
        form_p = QFormLayout(grp_pos)
        form_p.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.sld_pos_x = self._make_slider(0, 100)
        self.lbl_pos_x = QLabel("50%")
        row_x = QHBoxLayout()
        row_x.addWidget(self.sld_pos_x)
        row_x.addWidget(self.lbl_pos_x)
        self.sld_pos_x.valueChanged.connect(lambda v: self.lbl_pos_x.setText(f"{v}%"))
        form_p.addRow("Horizontal :", row_x)

        self.sld_pos_y = self._make_slider(0, 100)
        self.lbl_pos_y = QLabel("50%")
        row_y = QHBoxLayout()
        row_y.addWidget(self.sld_pos_y)
        row_y.addWidget(self.lbl_pos_y)
        self.sld_pos_y.valueChanged.connect(lambda v: self.lbl_pos_y.setText(f"{v}%"))
        form_p.addRow("Vertical :", row_y)

        grp_presets = QGroupBox("Raccourcis de position")
        grid = QVBoxLayout(grp_presets)
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()

        presets = [
            ("↖ Haut-Gauche", 2, 2), ("↑ Haut-Centre", 50, 2), ("↗ Haut-Droite", 98, 2),
            ("← Centre-Gauche", 2, 50), ("✛ Centre", 50, 50), ("→ Centre-Droite", 98, 50),
            ("↙ Bas-Gauche", 2, 98), ("↓ Bas-Centre", 50, 98), ("↘ Bas-Droite", 98, 98),
        ]
        rows = [row1, row2, row3]
        for i, (label, px, py) in enumerate(presets):
            btn = QPushButton(label)
            btn.setFixedHeight(30)
            btn.clicked.connect(lambda _, x=px, y=py: self._set_preset(x, y))
            rows[i // 3].addWidget(btn)

        grid.addLayout(row1)
        grid.addLayout(row2)
        grid.addLayout(row3)

        layout.addWidget(grp_pos)
        layout.addWidget(grp_presets)
        layout.addStretch()
        return w

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _make_slider(self, min_val: int, max_val: int) -> QSlider:
        s = QSlider(Qt.Orientation.Horizontal)
        s.setRange(min_val, max_val)
        return s

    def _set_preset(self, x: int, y: int):
        self.sld_pos_x.setValue(x)
        self.sld_pos_y.setValue(y)

    def _on_format_changed(self, idx: int):
        formats = [
            "%H:%M:%S", "%H:%M", "%I:%M:%S %p", "%I:%M %p",
            "%H:%M:%S — %A %d %B %Y", "%H:%M — %d/%m/%Y",
        ]
        if idx < len(formats):
            self.edt_format.setText(formats[idx])
            self.edt_format.setEnabled(False)
        else:
            self.edt_format.setEnabled(True)

    def _load_values(self):
        cfg = self.cfg

        self.chk_bg.setChecked(cfg["bg_enabled"])
        self.btn_bg_color.set_color(cfg["bg_color"])
        self.sld_bg_opacity.setValue(cfg["bg_opacity"])
        self.lbl_bg_opacity.setText(str(cfg["bg_opacity"]))
        self.spn_border_radius.setValue(cfg["border_radius"])
        self.btn_text_color.set_color(cfg["text_color"])
        self.sld_text_opacity.setValue(cfg["text_opacity"])
        self.lbl_text_opacity.setText(str(cfg["text_opacity"]))
        self.chk_always_on_top.setChecked(cfg["always_on_top"])
        self.chk_click_through.setChecked(cfg["click_through"])

        self.cmb_font.setCurrentFont(QFont(cfg["font_family"]))
        self.spn_font_size.setValue(cfg["font_size"])
        self.chk_bold.setChecked(cfg["font_bold"])
        self.chk_italic.setChecked(cfg["font_italic"])
        self.spn_pad_h.setValue(cfg["padding_h"])
        self.spn_pad_v.setValue(cfg["padding_v"])

        fmt = cfg["time_format"]
        presets = [
            "%H:%M:%S", "%H:%M", "%I:%M:%S %p", "%I:%M %p",
            "%H:%M:%S — %A %d %B %Y", "%H:%M — %d/%m/%Y",
        ]
        if fmt in presets:
            self.cmb_format.setCurrentIndex(presets.index(fmt))
            self.edt_format.setText(fmt)
            self.edt_format.setEnabled(False)
        else:
            self.cmb_format.setCurrentIndex(len(presets))
            self.edt_format.setText(fmt)
            self.edt_format.setEnabled(True)

        screens = QApplication.screens()
        idx = min(cfg["screen_index"], len(screens) - 1)
        self.cmb_screen.setCurrentIndex(idx)

        self.sld_pos_x.setValue(int(cfg["pos_x"]))
        self.lbl_pos_x.setText(f"{int(cfg['pos_x'])}%")
        self.sld_pos_y.setValue(int(cfg["pos_y"]))
        self.lbl_pos_y.setText(f"{int(cfg['pos_y'])}%")

        self._update_preview()

    def _update_preview(self, *_):
        font = self.cmb_font.currentFont()
        font.setPointSize(self.spn_font_size.value())
        font.setBold(self.chk_bold.isChecked())
        font.setItalic(self.chk_italic.isChecked())
        self._preview.setFont(font)
        c = QColor(self.btn_text_color.color())
        c.setAlpha(self.sld_text_opacity.value())
        self._preview.setStyleSheet(
            f"background: #11111b; border: 1px solid #45475a; border-radius: 8px;"
            f"color: rgba({c.red()},{c.green()},{c.blue()},{c.alpha()});"
            f"padding: {self.spn_pad_v.value()}px {self.spn_pad_h.value()}px;"
        )

    def _collect(self) -> dict:
        cfg = dict(self.cfg)
        cfg["bg_enabled"] = self.chk_bg.isChecked()
        cfg["bg_color"] = self.btn_bg_color.color()
        cfg["bg_opacity"] = self.sld_bg_opacity.value()
        cfg["border_radius"] = self.spn_border_radius.value()
        cfg["text_color"] = self.btn_text_color.color()
        cfg["text_opacity"] = self.sld_text_opacity.value()
        cfg["always_on_top"] = self.chk_always_on_top.isChecked()
        cfg["click_through"] = self.chk_click_through.isChecked()
        cfg["font_family"] = self.cmb_font.currentFont().family()
        cfg["font_size"] = self.spn_font_size.value()
        cfg["font_bold"] = self.chk_bold.isChecked()
        cfg["font_italic"] = self.chk_italic.isChecked()
        cfg["padding_h"] = self.spn_pad_h.value()
        cfg["padding_v"] = self.spn_pad_v.value()
        cfg["time_format"] = self.edt_format.text() or "%H:%M:%S"
        cfg["screen_index"] = self.cmb_screen.currentIndex()
        cfg["pos_x"] = self.sld_pos_x.value()
        cfg["pos_y"] = self.sld_pos_y.value()
        return cfg

    def _apply(self):
        new_cfg = self._collect()
        self.cfg = new_cfg
        cfg_mod.save(new_cfg)
        self.config_changed.emit(new_cfg)
