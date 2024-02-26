import random
import time
import types

from NoteSequence import NoteSequence
from Note import Note, sciName2Pitch


class TestSet:

    def __init__(self, interval_secs: float):
        self.interval_secs = interval_secs

    def __iter__(self):
        pass

class Question:

    def __init__(self, seq: NoteSequence, question: str, check):
        self.seq: NoteSequence = seq
        self.question: str = question
        self.check = check

    def ask(self, port):
        for msg in self.seq.play():
            port.send(msg)
        ans = input(self.question)
        return self.check(ans)



class CMajorScaleTest(TestSet):
    CMajorScale: list[str] = ['c4', 'd4', 'e4', 'f4', 'g4', 'a4', 'b4', 'c5']

    def __init__(self, interval_secs: float = 3):
        self.Notes = []
        for i in CMajorScaleTest.CMajorScale:
            self.Notes.append(Note.makeNote(i, 100, (1, 1), name=i))

        super().__init__(interval_secs)

    def generate(self):
        res = NoteSequence(bpm=60, tickrate=120)
        for n in self.Notes:
            res.addNote(n.copy(duration=(1, 2)))
        test_note: Note = random.choice(self.Notes)
        res.delay((2, 1))
        res.addNote(test_note.copy(duration=(2, 1)))
        # res.delay((1, 1))
        # res.addNote(test_note)

        question = "What's the name of the last note: "

        def check(ans: str):
            if sciName2Pitch(ans) == test_note.pitch:
                print("Correct")
                return True
            else:
                print("Wrong, the answer is {}".format(test_note.name))
                return False

        return Question(res, question, check)

    def __iter__(self):
        while True:
            yield self.generate()
            time.sleep(self.interval_secs)
