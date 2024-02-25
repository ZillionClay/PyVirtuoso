import mido

from util import narrow

NamePitch: dict[str, int] = {
    'c': +0,
    'd': +2,
    'e': +4,
    'f': +5,
    'g': +7,
    'a': +9,
    'b': +11
}

OffsetSign: dict[str, int] = {
    '': +0,
    '#': +1,
    'b': -1,
    'x': +2,
    '##': +2,  # 不标准
    'bb': -2,
}

BasePitch: int = 12  # pitch of C0


def sciName2Pitch(note_name: str) -> int:
    """
    返回科学音高记名法对应的midi音高
    :param note_name: 音名不区分大小写，例如c4和C4都为中央C。变音记号可写在前面或后面，前后都有变音记号则以前面的为准。升降号具体为#：升，x或##：重升，b：降，bb：重降, /：还原
    :return:
    """

    note_name = note_name.strip()
    res = 0
    offset = 0
    num = 0

    numFlagBit = -1
    for i in range(len(note_name)):
        if note_name[i] in '0123456789':
            num = int(note_name[i])
            numFlagBit = i
            break

    if (numFlagBit == 1):
        pitchName = note_name[numFlagBit - 1].lower()
        sign = note_name[numFlagBit + 1:].strip()
        if len(sign) > 1 and sign[0] == '/':
            sign = ''
        if not NamePitch.__contains__(pitchName):
            return 0
        if not OffsetSign.__contains__(sign):
            return 0
        return BasePitch + NamePitch[pitchName] + OffsetSign[sign] + num * 12

    elif (numFlagBit > 1):
        pitchName = note_name[numFlagBit - 1].lower()
        sign = note_name[:numFlagBit - 1].strip()
        if len(sign) > 1 and sign[0] == '/':
            sign = ''
        if not NamePitch.__contains__(pitchName):
            return 0
        if not OffsetSign.__contains__(sign):
            return 0
        return BasePitch + NamePitch[pitchName] + OffsetSign[sign] + num * 12
    else:
        return 0


class Note:

    def __init__(self, pitch: int, vel: int, duration: tuple[int, int], name: str = '', channel=0):
        self.pitch: int = narrow(pitch, 0, 128)
        self.vel: int = narrow(vel, 0, 128)
        self.duration: tuple[int, int] = duration
        self.name = name
        self.channel = channel

    def dur2Tick(self, bpm, tickrate) -> int:
        seconds = (self.duration[0] / self.duration[1]) * 60 / bpm
        return round(seconds * tickrate)

    def noteOnMidoMsg(self) -> mido.Message:
        return mido.Message('note_on',
                            channel=self.channel,
                            note=self.pitch,
                            velocity=self.vel)

    def noteOffMidoMsg(self) -> mido.Message:
        return mido.Message('note_off',
                            channel=self.channel,
                            note=self.pitch,
                            velocity=self.vel)

    @staticmethod
    def makeNote(pitch: str | int, vel: int, duration: tuple[int, int], name: str = '', channel=0):
        if isinstance(pitch, int):
            return Note(pitch, vel, duration, name, channel)
        elif isinstance(pitch, str):
            return Note(sciName2Pitch(pitch), vel, duration, name, channel)
        else:
            return None

    def copy(self, **kwargs):
        infos = {}
        for key in ['pitch', 'duration', 'vel', 'name','channel']:
            if kwargs.__contains__(key):
                infos[key] = kwargs[key]
            else:
                infos[key] = getattr(self, key)
        return Note(**infos)


if __name__ == '__main__':
    print(Note.makeNote('c8', 100, (1, 1)))
