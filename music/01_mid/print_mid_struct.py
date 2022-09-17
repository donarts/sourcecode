import numpy as np

# https://github.com/mido/mido

def _defmsg(status_byte, type_, value_names, length):
    return {
        'status_byte': status_byte,
        'type': type_,
        'value_names': value_names,
        'attribute_names': set(value_names) | {'type', 'time'},
        'length': length,
    }

# from modo mido/messages/specs.py
SPECS = [
    # https://www.recordingblogs.com/wiki/midi-voice-messages
    # MIDI voice messages
    _defmsg(0x80, 'note_off', ('channel', 'note', 'velocity'), 3),
    _defmsg(0x90, 'note_on', ('channel', 'note', 'velocity'), 3),
    _defmsg(0xa0, 'polytouch', ('channel', 'note', 'value'), 3),
    _defmsg(0xb0, 'control_change', ('channel', 'control', 'value'), 3),
    _defmsg(0xc0, 'program_change', ('channel', 'program',), 2),
    _defmsg(0xd0, 'aftertouch', ('channel', 'value',), 2),
    _defmsg(0xe0, 'pitchwheel', ('channel', 'pitch',), 3),

    # https://www.recordingblogs.com/wiki/midi-system-common-messages
    # System common messages.
    # 0xf4 and 0xf5 are undefined.
    _defmsg(0xf0, 'sysex', ('data',), float('inf')),
    _defmsg(0xf1, 'quarter_frame', ('frame_type', 'frame_value'), 2),
    _defmsg(0xf2, 'songpos', ('pos',), 3),
    _defmsg(0xf3, 'song_select', ('song',), 2),
    _defmsg(0xf6, 'tune_request', (), 1),

    # https://www.recordingblogs.com/wiki/midi-system-realtime-messages
    # System real time messages.
    # 0xf9 and 0xfd are undefined.
    _defmsg(0xf8, 'clock', (), 1),
    _defmsg(0xfa, 'start', (), 1),
    _defmsg(0xfb, 'continue', (), 1),
    _defmsg(0xfc, 'stop', (), 1),
    _defmsg(0xfe, 'active_sensing', (), 1),

    # https://www.recordingblogs.com/wiki/midi-meta-messages
    # MIDI meta messages
    _defmsg(0xff, 'reset', (), 1),
]

def _meta_defmsg(Meta_type,Message):
    return {
        'Message': Message,
        'Metatype': Meta_type,
    }

META_EVENT_SPEC = [
    _meta_defmsg(0x00, "Sequence number"),
    _meta_defmsg(0x01, "Text"),
    _meta_defmsg(0x02, "Copyright notice"),
    _meta_defmsg(0x03, "Track name"),
    _meta_defmsg(0x04, "Instrument name"),
    _meta_defmsg(0x05, "Lyrics"),
    _meta_defmsg(0x06, "Marker"),
    _meta_defmsg(0x07, "Cue point"),
    _meta_defmsg(0x20, "Channel prefix"),
    _meta_defmsg(0x2F, "End of track"),
    _meta_defmsg(0x51, "Set tempo"),
    _meta_defmsg(0x54, "SMPTE offset"),
    _meta_defmsg(0x58, "Time signature"),
    _meta_defmsg(0x59, "Key signature"),
    _meta_defmsg(0x7F, "Sequencer specific")
]

class mid_file():

    # https://faydoc.tripod.com/formats/mid.htm
    # https://github.com/mido/mido/blob/main/mido/midifiles/midifiles.py
    def __init__(self):
        self.ticks_per_beat = None
        self.trackcount = None
        self.type = None
        self.note_str = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    def get_note_number_str(self, nnumber):
        octave = int(nnumber / len(self.note_str))
        note_ = self.note_str[nnumber % len(self.note_str)]
        return note_+str(octave)

    def read_variable_int(self, byte_data, pos):
        delta = 0
        i = 0
        while True:
            byte = np.uint8(byte_data[i+pos])
            delta = (delta << 7) | (byte & 0x7f)
            if byte < 0x80:
                return delta, i+1
            i = i + 1

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
            '''
            self.type = int.from_bytes(body[0:2].tobytes(), 'big')
            self.trackcount = int.from_bytes(body[2:4].tobytes(), 'big')
            self.ticks_per_beat = int.from_bytes(body[4:6].tobytes(), 'big')
            print(self.type, self.trackcount, self.ticks_per_beat)
        elif type == 'MTrk':
            # time delta + event type(status_byte) + data
            # time delta :
            #    - 가변길이로 127 보다 추가 byte 사용 : 7bit로 구성된 길이 사용(big endian)
            # event type (status_byte):
            #    - 0x00 ~ 0x7F : Running Status
            #         - same status_byte
            #    - 0x8? ~ 0xE? : Midi messages
            #         - SPECS
            #    - 0xF0, 0xF7 : 일단 처리 안함
            #         - data 가변 길이(7bit) + data
            #    - 0xF0 ~ 0xFE : System messages
            #         - SPECS
            #    - 0xFF : Meta messages (see, read_meta_message in mido )
            #         - command + data 가변 길이(7bit) + data
            pos = 0
            last_status_byte = None
            while True:
                time_delta, delta_size = self.read_variable_int(body, pos)
                pos = pos + delta_size
                print(f"delta {pos} {time_delta}(0x{time_delta:02x}) {delta_size}")

                status_byte = np.uint8(body[pos])
                pos = pos + 1

                if status_byte <= 0x7F:
                    status_byte = last_status_byte
                    pos = pos - 1

                if status_byte == 0xFF:
                    # https://www.recordingblogs.com/wiki/midi-meta-messages
                    # Meta messages
                    command = np.uint8(body[pos])
                    if command == 0x2F:
                        print("End of track")
                        return
                    pos = pos + 1
                    data_delta, delta_size = self.read_variable_int(body, pos)
                    pos = pos + delta_size
                    data = body[pos:pos+data_delta]
                    pos = pos + data_delta
                    find = False
                    for spec_data in META_EVENT_SPEC:
                        if command == spec_data['Metatype']:
                            print(f"Meta message {spec_data['Message']} FF {command:02x} {data} {data_delta:02x} {delta_size:02x}")
                            find = True
                            break
                    if find == False:
                        print(f"error metatype:{command:02x}" )
                        #exit(-1)

                elif status_byte == 0xF0 or status_byte == 0xF7:
                    # 일단 처리 안함
                    data_delta, delta_size = self.read_variable_int(body, pos)
                    pos = pos + delta_size
                    data = body[pos:pos + data_delta]
                    pos = pos + data_delta
                    print(f"skip messages {data_delta:02x} {data} {delta_size:02x}")
                else:
                    pos_len = 1
                    find = False
                    for spec_data in SPECS:
                        if status_byte <= 0xEF and spec_data['status_byte'] == (status_byte & 0xF0):
                            # status_byte <= 0xEF 작은 조건은 Midi messages 가 됩니다.
                            # Midi messages
                            if spec_data['type'] == 'note_on' or spec_data['type'] == 'note_off' :
                                ch = status_byte & 0x0F
                                nn = body[pos]
                                vv = body[pos+1]
                                print(f"{spec_data['type']} {status_byte:02x} {ch} {self.get_note_number_str(nn)} {vv}")
                            else:
                                print(f"{status_byte:02x} {spec_data['type']} {spec_data['length']}")
                            pos_len = spec_data['length'] - 1
                            find = True
                            break
                        elif spec_data['status_byte'] == status_byte:
                            # status_byte > 0xEF 이면 System messages 가 된다.
                            # System messages
                            print(f"{status_byte:02x} {spec_data['type']} {spec_data['length']}")
                            pos_len = spec_data['length'] - 1
                            find = True
                            break
                    if find == False:
                        print(f"error status_byte:{status_byte}" )
                        exit(-1)
                    pos = pos + pos_len
                last_status_byte = status_byte
                if pos >= length:
                    return

    def read(self, filename):
        with open(filename) as f:
            rectype = np.dtype(np.uint8)
            bdata = np.fromfile(f, dtype=rectype)
        # MID 파일은 chunk의 연속으로 되어 있습니다.
        # Chunk Type(4), chunk body length (4), body(chunk body length)
        read_pos = 0
        while True:
            chunk_type = bdata[read_pos:read_pos+4].tobytes()
            chunk_type = chunk_type.decode('utf-8')
            chunk_length = int.from_bytes(bdata[read_pos+4:read_pos+8].tobytes(), 'big')

            print(chunk_type, chunk_length)

            self.process_chunk(chunk_type, chunk_length, bdata[read_pos+8:read_pos+8+chunk_length])

            read_pos = read_pos + chunk_length + 8
            if len(bdata) <= read_pos:
                break


if __name__ == "__main__":
    print(SPECS)
    mid = mid_file()
    mid.read("../00_data/tests_for-elise.mid")
