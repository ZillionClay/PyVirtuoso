import time
import mido
from Note import Note

class NoteSequence:

    def __init__(self, bpm: int = 120, tickrate: int = 100):
        self.msg: dict[int, list[mido.Message]] = {}
        self.bpm = bpm
        self.tickrate = tickrate  # ticks per second
        self.endTick = 0

    def addNote(self, note: Note, tick: int = -1) -> tuple[int, int]:
        if tick < 0:
            tick = self.endTick

        if not self.msg.__contains__(tick):
            self.msg[tick]: list[mido.Message] = []
        self.msg[tick].append(note.noteOnMidoMsg())

        end: int = tick + note.dur2Tick(self.bpm, self.tickrate)
        if not self.msg.__contains__(end):
            self.msg[end]: list[mido.Message] = []
        self.msg[end].append(note.noteOffMidoMsg())

        self.endTick = end if end > self.endTick else self.endTick

        return tick, end

    def play(self, now=time.time):
        start_sec = now()
        for tick in self.msg.keys():
            msg_list = self.msg[tick]
            sleep_sec = self.ticks2seconds(tick) - (now() - start_sec)
            time.sleep(sleep_sec) if start_sec > 0 else None
            for msg in msg_list:
                yield msg

    def delay(self, duration: tuple[int, int]) -> int:
        seconds = (duration[0] / duration[1]) * 60 / self.bpm
        self.endTick += round(seconds * self.tickrate)
        return self.endTick

    def ticks2seconds(self, ticks) -> float:
        return ticks/self.tickrate

    def clear(self):
        self.msg: dict[int, list[mido.Message]] = {}

