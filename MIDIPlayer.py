import mido
import time
import threading


class PlayerThread(threading.Thread):

    def __init__(self, player):
        self.player: MIDIPlayer = player
        self.started = False
        self.tick = 0
        super().__init__()

    def run(self) -> None:
        while True:
            start = time.time_ns()
            self.worker()
            print(time.time_ns() - start)
            sleep_secs: float = self.player.timebase - (time.time_ns() - start) / 1e9
            while(sleep_secs > 0):
                time.sleep(sleep_secs)

    def start(self):
        self.started = True
        super().start()

    def worker(self):
        self.tick += 1


class MIDIPlayer:

    def __init__(self, device_name='', bpm=120, time_sign=(4, 4)):
        self.midiout = mido.open_output(device_name) if device_name else mido.get_output_names()[0]

        self.timebase = 1 / (bpm * 128)
        self.playThread = PlayerThread(self)

    def play(self, noteSequence):
        if not self.playThread.started:
            self.playThread.start()

    def worker(self):
        pass


if __name__ == '__main__':
    midi = MIDIPlayer()
    midi.play(None)
