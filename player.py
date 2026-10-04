import numpy as np
import sounddevice as sd
from engine import build_board, load_audio, settings

class Player:
    def __init__(self, audio, samplerate, s):
        self.audio = audio
        self.samplerate = samplerate
        self.position = 0
        self.board = build_board(s)
        self.stream = sd.OutputStream(
            samplerate=samplerate,
            channels=audio.shape[0],
            callback=self.callback,
        )

    def callback(self, outdata, frames, time, status):
        total = self.audio.shape[1]
        indices = np.arange(self.position, self.position + frames) % total
        chunk = self.audio[:, indices]
        processed = self.board(chunk, self.samplerate, reset=False)
        outdata[:] = processed.T
        self.position = (self.position + frames) % total

    def update(self, s):
        self.board = build_board(s)

    def play(self):
        self.stream.start()

    def stop(self):
        self.stream.stop()

if __name__ == "__main__":
    audio, samplerate = load_audio("Test_Track.wav")
    player = Player(audio, samplerate, settings)
    player.play()
    print("Playing. Type an MF gain (like 9 or -6), or q to quit.")
    while True:
        cmd = input("> ")
        if cmd == "q":
            break
        try:
            settings["mf"]["gain"] = float(cmd)
            player.update(settings)
        except ValueError:
            print("Type a number or q")
    player.stop()