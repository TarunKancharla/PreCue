import json
from pathlib import Path

BUILTIN_DIR = Path(__file__).parent / "presets"
USER_DIR = Path.home() / "Library" / "Application Support" / "PreCue" / "user_presets"
def list_presets():
    presets = {}
    for folder in [BUILTIN_DIR, USER_DIR]:
        folder.mkdir(parents=True, exist_ok=True)
        for file in sorted(folder.glob("*.json")):
            presets[file.stem] = file
    return presets

def load_preset(path):
    with open(path) as f:
        return json.load(f)

def save_preset(name, s):
    USER_DIR.mkdir(parents=True, exist_ok=True)
    with open(USER_DIR / f"{name}.json", "w") as f:
        json.dump(s, f, indent=2)