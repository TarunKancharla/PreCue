import json
from presets import BUILTIN_DIR

def band(freq, gain=0.0, q=1.0):
    return {"freq": freq, "gain": gain, "q": q}

PRESETS = {
    "Vocals": {
        "hpf": {"freq": 100, "slope": 18},
        "lf":  band(100, 0.0, 0.7),
        "lmf": band(300, -3.0, 1.0),     # cut mud
        "mf":  band(1000, 0.0),
        "hmf": band(3500, 2.5, 1.0),     # presence
        "hf":  band(10000, 3.0, 0.7),    # air
        "lpf": {"freq": 20000, "slope": 12},
    },
    "Kick": {
        "hpf": {"freq": 30, "slope": 12},
        "lf":  band(60, 3.0, 0.7),       # thump
        "lmf": band(350, -4.0, 1.4),     # cut boxiness
        "mf":  band(1000, 0.0),
        "hmf": band(4000, 3.0, 1.2),     # beater click
        "hf":  band(10000, 0.0, 0.7),
        "lpf": {"freq": 15000, "slope": 12},
    },
    "Snare": {
        "hpf": {"freq": 80, "slope": 12},
        "lf":  band(100, 0.0, 0.7),
        "lmf": band(200, 2.0, 1.2),      # body
        "mf":  band(800, -3.0, 1.4),     # cut boxiness
        "hmf": band(5000, 3.0, 1.0),     # crack
        "hf":  band(10000, 2.0, 0.7),    # sizzle
        "lpf": {"freq": 20000, "slope": 12},
    },
    "Bass": {
        "hpf": {"freq": 35, "slope": 12},
        "lf":  band(80, 2.0, 0.7),       # weight
        "lmf": band(250, -3.0, 1.2),     # cut mud
        "mf":  band(800, 2.0, 1.0),      # growl, helps on small speakers
        "hmf": band(2500, 1.5, 1.0),     # string attack
        "hf":  band(8000, 0.0, 0.7),
        "lpf": {"freq": 10000, "slope": 12},
    },
    "Acoustic Guitar": {
        "hpf": {"freq": 80, "slope": 12},
        "lf":  band(100, 0.0, 0.7),
        "lmf": band(200, -3.0, 1.0),     # cut boom
        "mf":  band(1000, 0.0),
        "hmf": band(3000, 2.0, 1.0),     # pick detail
        "hf":  band(10000, 2.0, 0.7),    # sparkle
        "lpf": {"freq": 20000, "slope": 12},
    },
    "Electric Guitar": {
        "hpf": {"freq": 90, "slope": 12},
        "lf":  band(100, 0.0, 0.7),
        "lmf": band(300, -2.0, 1.0),     # cut mud
        "mf":  band(1000, 0.0),
        "hmf": band(2500, 2.0, 1.0),     # bite
        "hf":  band(8000, 0.0, 0.7),
        "lpf": {"freq": 10000, "slope": 12},  # tame fizz
    },
    "Piano": {
        "hpf": {"freq": 40, "slope": 6},
        "lf":  band(100, 0.0, 0.7),
        "lmf": band(300, -2.0, 1.0),     # cut mud
        "mf":  band(1000, 0.0),
        "hmf": band(3000, 1.5, 1.0),     # clarity
        "hf":  band(9000, 2.0, 0.7),     # brightness
        "lpf": {"freq": 20000, "slope": 12},
    },
}

BUILTIN_DIR.mkdir(exist_ok=True)
for name, data in PRESETS.items():
    with open(BUILTIN_DIR / f"{name}.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"Wrote {name}")