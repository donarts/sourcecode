import numpy as np

filename = "../00_data/tests_for-elise.mid"

with open(filename) as f:
    rectype = np.dtype(np.byte)
    bdata = np.fromfile(f, dtype=rectype)

print(bdata)

# MID 파일은 chunk의 연속으로 되어 있습니다.
# Chunk Type(4), chunk body length (4), body(chunk body length)
read_pos = 0
while True:
    chunk_type = bdata[read_pos:read_pos+4].tobytes()
    chunk_type = chunk_type.decode('utf-8')
    chunk_length = int.from_bytes(bdata[read_pos+4:read_pos+8].tobytes(), 'big')

    print(chunk_type, chunk_length)

    read_pos = read_pos + chunk_length + 8
    if len(bdata) <= read_pos:
        break

'''
[ 77  84 104 ...  -1  47   0]
MThd 6
MTrk 3909
MTrk 3034
'''
