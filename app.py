import sys
import copy
import numpy as np
import pyqtgraph as pg
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QGridLayout, QFrame,
    QFileDialog, QDoubleSpinBox, QComboBox, QInputDialog,
)
from engine import load_audio, bounce, settings, frequency_response
from player import Player
from presets import list_presets, load_preset, save_preset
from style import STYLE, PANEL, BORDER, MUTED, ACCENT, DOT, FILL

BANDS = ["hpf", "lf", "lmf", "mf", "hmf", "hf", "lpf"]
FLAT = copy.deepcopy(settings)

def make_spin(minimum, maximum, value, step, suffix, decimals):
    box = QDoubleSpinBox()
    box.setRange(minimum, maximum)
    box.setDecimals(decimals)
    box.setSingleStep(step)
    box.setSuffix(suffix)
    box.setValue(value)
    return box

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PreCue")
        self.setMinimumWidth(920)
        self.player = None
        self.audio = None
        self.samplerate = None
        self.is_playing = False
        self.boxes = {}

        # Header
        title = QLabel("PreCue")
        title.setObjectName("title")
        subtitle = QLabel("EQ presets, made simple")
        subtitle.setObjectName("subtitle")

        # Transport row
        self.file_label = QLabel("No file loaded")
        self.file_label.setObjectName("fileLabel")
        self.load_button = QPushButton("Load")
        self.play_button = QPushButton("Play")
        self.play_button.setObjectName("primary")
        self.bounce_button = QPushButton("Bounce")
        self.play_button.setEnabled(False)
        self.bounce_button.setEnabled(False)

        self.load_button.clicked.connect(self.load_file)
        self.play_button.clicked.connect(self.toggle_play)
        self.bounce_button.clicked.connect(self.bounce_file)

        buttons = QHBoxLayout()
        buttons.addWidget(self.file_label, 1)
        buttons.addWidget(self.load_button)
        buttons.addWidget(self.play_button)
        buttons.addWidget(self.bounce_button)

        # Preset row
        preset_label = QLabel("PRESET")
        preset_label.setObjectName("rowLabel")
        self.preset_box = QComboBox()
        self.preset_box.currentTextChanged.connect(self.apply_preset)
        self.save_preset_button = QPushButton("Save Preset")
        self.save_preset_button.clicked.connect(self.save_preset_clicked)

        preset_row = QHBoxLayout()
        preset_row.addWidget(preset_label)
        preset_row.addWidget(self.preset_box, 1)
        preset_row.addWidget(self.save_preset_button)

        # EQ graph
        self.graph = pg.PlotWidget()
        self.graph.setBackground(PANEL)
        self.graph.setLogMode(x=True, y=False)
        self.graph.setXRange(np.log10(20), np.log10(20000))
        self.graph.setYRange(-24, 24)
        self.graph.showGrid(x=True, y=True, alpha=0.15)
        self.graph.setMouseEnabled(x=False, y=False)
        self.graph.hideButtons()
        self.graph.setMinimumHeight(260)
        for name in ("bottom", "left"):
            axis = self.graph.getAxis(name)
            axis.setPen(BORDER)
            axis.setTextPen(MUTED)
        ticks = [20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]
        labels = ["20", "50", "100", "200", "500", "1k", "2k", "5k", "10k", "20k"]
        self.graph.getAxis("bottom").setTicks([[(np.log10(f), l) for f, l in zip(ticks, labels)]])
        self.curve = self.graph.plot(
            pen=pg.mkPen(ACCENT, width=3),
            fillLevel=0,
            brush=pg.mkBrush(*FILL),
        )
        self.dots = self.graph.plot(
            pen=None, symbol="o", symbolSize=11,
            symbolBrush=DOT, symbolPen=pg.mkPen(PANEL, width=2),
            )

        graph_panel = QFrame()
        graph_panel.setObjectName("panel")
        graph_layout = QVBoxLayout(graph_panel)
        graph_layout.setContentsMargins(10, 10, 10, 10)
        graph_layout.addWidget(self.graph)

        # EQ grid
        grid = QGridLayout()
        grid.setContentsMargins(16, 14, 16, 14)
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(8)

        for row, text in enumerate(["FREQ", "GAIN", "Q", "SLOPE"], start=1):
            label = QLabel(text)
            label.setObjectName("rowLabel")
            grid.addWidget(label, row, 0)

        for col, band in enumerate(BANDS, start=1):
            self.boxes[band] = {}
            band_label = QLabel(band.upper())
            band_label.setObjectName("bandLabel")
            band_label.setAlignment(Qt.AlignCenter)
            grid.addWidget(band_label, 0, col)

            freq = make_spin(20, 20000, settings[band]["freq"], 10, " Hz", 0)
            freq.valueChanged.connect(lambda v, b=band: self.set_value(b, "freq", v))
            grid.addWidget(freq, 1, col)
            self.boxes[band]["freq"] = freq

            if "gain" in settings[band]:
                gain = make_spin(-18, 18, settings[band]["gain"], 0.5, " dB", 1)
                gain.valueChanged.connect(lambda v, b=band: self.set_value(b, "gain", v))
                grid.addWidget(gain, 2, col)
                self.boxes[band]["gain"] = gain

                q = make_spin(0.1, 10, settings[band]["q"], 0.1, "", 2)
                q.valueChanged.connect(lambda v, b=band: self.set_value(b, "q", v))
                grid.addWidget(q, 3, col)
                self.boxes[band]["q"] = q

            if "slope" in settings[band]:
                slope = QComboBox()
                slope.addItems(["Off", "6 dB/oct", "12 dB/oct", "18 dB/oct", "24 dB/oct"])
                slope.setCurrentIndex(settings[band]["slope"] // 6)
                slope.currentIndexChanged.connect(lambda i, b=band: self.set_value(b, "slope", i * 6))
                grid.addWidget(slope, 4, col)
                self.boxes[band]["slope"] = slope

        grid_panel = QFrame()
        grid_panel.setObjectName("panel")
        grid_panel.setLayout(grid)

        # Put it all together
        layout = QVBoxLayout()
        layout.setContentsMargins(28, 24, 28, 28)
        layout.setSpacing(14)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(6)
        layout.addLayout(buttons)
        layout.addLayout(preset_row)
        layout.addWidget(graph_panel, 1)
        layout.addWidget(grid_panel)
        self.setLayout(layout)

        self.update_graph()
        self.refresh_presets()

    def set_value(self, band, key, value):
        settings[band][key] = value
        if self.player:
            self.player.update(settings)
        self.update_graph()

    def update_graph(self):
        sr = self.samplerate or 44100
        freqs, db = frequency_response(settings, sr)
        self.curve.setData(freqs, db)
        band_freqs = [settings[b]["freq"] for b in BANDS]
        band_db = np.interp(band_freqs, freqs, db)
        self.dots.setData(band_freqs, band_db)

    def refresh_presets(self):
        self.presets = list_presets()
        self.preset_box.blockSignals(True)
        self.preset_box.clear()
        self.preset_box.addItem("Flat")
        self.preset_box.addItems(list(self.presets.keys()))
        self.preset_box.blockSignals(False)

    def apply_preset(self, name):
        if name == "Flat":
            data = FLAT
        else:
            data = load_preset(self.presets[name])
        for band in BANDS:
            settings[band].update(data[band])
            for key, box in self.boxes[band].items():
                box.blockSignals(True)
                if key == "slope":
                    box.setCurrentIndex(int(settings[band][key]) // 6)
                else:
                    box.setValue(settings[band][key])
                box.blockSignals(False)
        if self.player:
            self.player.update(settings)
        self.update_graph()

    def save_preset_clicked(self):
        name, ok = QInputDialog.getText(self, "Save Preset", "Preset name:")
        name = name.strip()
        if not ok or not name:
            return
        save_preset(name, settings)
        self.refresh_presets()
        self.preset_box.blockSignals(True)
        self.preset_box.setCurrentText(name)
        self.preset_box.blockSignals(False)

    def load_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Load audio", "",
            "Audio Files (*.wav *.mp3 *.aiff *.flac *.m4a)",
        )
        if not path:
            return
        if self.player:
            self.player.stop()
        self.audio, self.samplerate = load_audio(path)
        self.player = Player(self.audio, self.samplerate, settings)
        self.is_playing = False
        self.file_label.setText(path.split("/")[-1])
        self.play_button.setText("Play")
        self.play_button.setEnabled(True)
        self.bounce_button.setEnabled(True)
        self.update_graph()

    def toggle_play(self):
        if self.is_playing:
            self.player.stop()
            self.play_button.setText("Play")
        else:
            self.player.play()
            self.play_button.setText("Pause")
        self.is_playing = not self.is_playing

    def bounce_file(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Bounce", "bounced.wav", "WAV (*.wav)",
        )
        if not path:
            return
        if not path.endswith(".wav"):
            path += ".wav"
        bounce(path, self.audio, self.samplerate, settings)
        self.file_label.setText(f"Bounced to {path.split('/')[-1]}")

app = QApplication(sys.argv)
app.setStyle("Fusion")
app.setStyleSheet(STYLE)
window = MainWindow()
window.show()
sys.exit(app.exec())