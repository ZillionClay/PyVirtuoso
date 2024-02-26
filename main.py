import mido
from NoteSequence import Note, NoteSequence
from util import play_midi
from TestSet import CMajorScaleTest
print(mido.get_output_names())
n = int(input("choose output device:"))
port = mido.open_output(mido.get_output_names()[n])

# play_midi(r"C:\Users\11312\Music\CMajor.mid", port)

test = CMajorScaleTest(interval_secs=1)

i = 0
rate = 0
for question in test:
    if(i >= 20):
        break
    res = question.ask(port)
    i += 1
    if res:
        rate += (1-rate)/i
    else:
        rate += -rate/i

print('Correctness：{}'.format(rate))