BG = "#16261d"        # deep forest
PANEL = "#1d3126"     # moss shade
BORDER = "#2f4a3a"    # tree bark green
TEXT = "#efe6cf"      # warm cream
MUTED = "#9fb39a"     # sage
ACCENT = "#a8d08d"    # spring leaf
DOT = "#f2d479"       # firefly gold
FILL = (168, 208, 141, 45)  # soft leaf glow

STYLE = """
QWidget {
    background-color: #16261d;
    color: #efe6cf;
    font-family: "Avenir Next";
    font-size: 13px;
}
QLabel { background: transparent; }
QLabel#title {
    color: #a8d08d;
    font-family: "Snell Roundhand";
    font-size: 52px;
    font-weight: 700;
}
QLabel#subtitle {
    color: #9fb39a;
    font-family: "Baskerville";
    font-style: italic;
    font-size: 15px;
}
QLabel#fileLabel { color: #c9d4bf; font-family: "Baskerville"; font-size: 14px; }
QLabel#bandLabel {
    color: #a8d08d;
    font-family: "Copperplate";
    font-size: 14px;
    letter-spacing: 1px;
}
QLabel#rowLabel {
    color: #9fb39a;
    font-family: "Copperplate";
    font-size: 12px;
}

QFrame#panel {
    background-color: #1d3126;
    border: 1px solid #2f4a3a;
    border-radius: 14px;
}

QPushButton {
    background-color: #1d3126;
    border: 1px solid #2f4a3a;
    border-radius: 10px;
    padding: 8px 18px;
    color: #efe6cf;
    font-family: "Copperplate";
    font-size: 13px;
}
QPushButton:hover { border-color: #f2d479; color: #f2d479; }
QPushButton:disabled { color: #5b7363; border-color: #24392d; }
QPushButton#primary {
    background-color: #a8d08d;
    color: #16261d;
    border: none;
    font-weight: 700;
}
QPushButton#primary:hover { background-color: #f2d479; color: #16261d; }
QPushButton#primary:disabled { background-color: #24392d; color: #5b7363; }

QDoubleSpinBox, QComboBox {
    background-color: #16261d;
    border: 1px solid #2f4a3a;
    border-radius: 6px;
    padding: 4px 6px;
    min-height: 22px;
    color: #efe6cf;
}
QDoubleSpinBox:focus, QComboBox:focus { border-color: #f2d479; }
QComboBox QAbstractItemView {
    background-color: #1d3126;
    border: 1px solid #2f4a3a;
    selection-background-color: #a8d08d;
    selection-color: #16261d;
}
"""