import numpy as np

from pedalboard import (
    Pedalboard, HighpassFilter, LowpassFilter,
    LowShelfFilter, HighShelfFilter, PeakFilter,
)
from pedalboard.io import AudioFile

# All 7 bands, Pro Tools style
settings = {
    "hpf": {"freq": 20, "slope": 0},
    "lf":  {"freq": 100,   "gain": 0.0, "q": 0.7},
    "lmf": {"freq": 250,   "gain": 0.0, "q": 1.0},
    "mf":  {"freq": 1000,  "gain": 0.0, "q": 1.0},
    "hmf": {"freq": 3000,  "gain": 0.0, "q": 1.0},
    "hf":  {"freq": 8000,  "gain": 0.0, "q": 0.7},
    "lpf": {"freq": 20000, "slope": 0},
}

def build_board(s):
    hpf_count = s["hpf"]["slope"] // 6
    lpf_count = s["lpf"]["slope"] // 6
    hpf = [HighpassFilter(cutoff_frequency_hz=s["hpf"]["freq"]) for _ in range(hpf_count)]
    lpf = [LowpassFilter(cutoff_frequency_hz=s["lpf"]["freq"]) for _ in range(lpf_count)]
    middle = [
        LowShelfFilter(cutoff_frequency_hz=s["lf"]["freq"],  gain_db=s["lf"]["gain"],  q=s["lf"]["q"]),
        PeakFilter(cutoff_frequency_hz=s["lmf"]["freq"],     gain_db=s["lmf"]["gain"], q=s["lmf"]["q"]),
        PeakFilter(cutoff_frequency_hz=s["mf"]["freq"],      gain_db=s["mf"]["gain"],  q=s["mf"]["q"]),
        PeakFilter(cutoff_frequency_hz=s["hmf"]["freq"],     gain_db=s["hmf"]["gain"], q=s["hmf"]["q"]),
        HighShelfFilter(cutoff_frequency_hz=s["hf"]["freq"], gain_db=s["hf"]["gain"],  q=s["hf"]["q"]),
    ]
    return Pedalboard(hpf + middle + lpf)

def load_audio(path):
    with AudioFile(path) as f:
        return f.read(f.frames), f.samplerate

def process(audio, samplerate, s):
    board = build_board(s)
    return board(audio, samplerate)

def bounce(path, audio, samplerate, s):
    processed = process(audio, samplerate, s)
    with AudioFile(path, "w", samplerate, processed.shape[0]) as f:
        f.write(processed)

def frequency_response(s, samplerate=44100, n=16384):
    impulse = np.zeros((1, n), dtype=np.float32)
    impulse[0, 0] = 1.0
    out = build_board(s)(impulse, samplerate)
    spectrum = np.abs(np.fft.rfft(out[0]))
    freqs = np.fft.rfftfreq(n, 1 / samplerate)
    db = 20 * np.log10(np.maximum(spectrum, 1e-6))
    return freqs[1:], db[1:]

if __name__ == "__main__":
    audio, samplerate = load_audio("Test_Track.wav")
    bounce("test_eq.wav", audio, samplerate, settings)
    print("Done")