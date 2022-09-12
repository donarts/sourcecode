import numpy as np


class MidFile:

    # https://faydoc.tripod.com/formats/mid.htm
    # https://github.com/mido/mido/blob/main/mido/midifiles/midifiles.py
    def __init__(self):
        self.ticks_per_beat = None
        self.trackcount = None
        self.type = None

    def process_chunk(self, type, length, body):
        if type == 'MThd':
            ''' 
            * type (2)
              0:single-track
              1:multiple tracks, synchronous
              2:multiple tracks, asynchronous
            * trackcount (2)
            * ticks_per_beat (2)
              is the number of delta-time ticks per quarter note.
              4분 노트(음표)당 델타-타임 틱들의 갯수
              https://www.recordingblogs.com/wiki/header-chunk-of-a-midi-file
              16비트의 상위 비트가 0이면 "박자당 틱"(또는 "4분음표당 펄스(틱수)")입니다. 
              상위 비트가 1이면 시간 분할은 "초당 프레임 수"입니다.
              - BPM = 1분당 bit수 
                120BPM은 1분에 120Bit로 표현 = 4분 음표(1박)가 1분에 120번 나올 수 있음(1번 나오는데 0.5초)
                ticks_per_beat = 480 이면, time delta가 480인 경우 4분 음표로 표현됨  
            '''
            self.type = int.from_bytes(body[0:2].tobytes(), 'big')
            self.trackcount = int.from_bytes(body[2:4].tobytes(), 'big')
            self.ticks_per_beat = int.from_bytes(body[4:6].tobytes(), 'big')
            print(self.type, self.trackcount, self.ticks_per_beat)

    def read(self, filename):
        with open(filename) as f:
            rectype = np.dtype(np.uint8)
            bdata = np.fromfile(f, dtype=rectype)
        # MID 파일은 chunk의 연속으로 되어 있습니다.
        # Chunk Type(4), chunk body length (4), body(chunk body length)
        read_pos = 0
        while True:
            chunk_type = bdata[read_pos:read_pos + 4].tobytes()
            chunk_type = chunk_type.decode('utf-8')
            chunk_length = int.from_bytes(bdata[read_pos + 4:read_pos + 8].tobytes(), 'big')

            print(chunk_type, chunk_length)

            self.process_chunk(chunk_type, chunk_length, bdata[read_pos + 8:read_pos + 8 + chunk_length])

            read_pos = read_pos + chunk_length + 8
            if len(bdata) <= read_pos:
                break


if __name__ == "__main__":
    mid = MidFile()
    mid.read("../00_data/tests_for-elise.mid")

'''
MThd 6
1 2 480
MTrk 3909
MTrk 3034
'''