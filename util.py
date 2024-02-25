import time
import mido


def play_midi(filepath, port):
    # 读取MIDI文件内容
    pattern = mido.MidiFile(filepath)

    for msg in pattern.play():
        print(msg)
        port.send(msg)


def narrow(obj, bottom, top):
    if obj > top:
        return top
    elif obj < bottom:
        return bottom
    else:
        return obj
