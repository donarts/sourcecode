

with open("test.bin", "w", encoding="utf-8") as f:
    f.write("[한글]")


with open("test.bin", "r", encoding="utf-8") as f:
    while True:
        data = f.read(1)
        if data=='':
            break
        print(data)

"""
[
한
글
]
"""

print('*** binary mode ***')

with open("test.bin", "rb") as f:
    while True:
        data = f.read(1)
        if data==b'':
            break
        print(data)

"""
b'['
b'\xed'
b'\x95'
b'\x9c'
b'\xea'
b'\xb8'
b'\x80'
b']'
"""

print('*** binary mode byte array ***')

byte_array = bytearray()
with open("test.bin", "rb") as f:
    while True:
        data = f.read(1)
        if data==b'':
            break
        byte_array += data
print(byte_array)

"""
bytearray(b'[\xed\x95\x9c\xea\xb8\x80]')
"""

print('*** binary mode read once ***')
# read의 size는 선택적인 숫자 인자입니다.
# size가 생략되거나 음수면 파일의 내용 전체를 읽어서 돌려줍니다;
byte_array = bytearray()
with open("test.bin", "rb") as f:
    data = f.read()
    print(len(data))
    byte_array = data
print(byte_array)
"""
8
b'[\xed\x95\x9c\xea\xb8\x80]'
"""

print('*** binary mode file pointer ***')
with open("test.bin", "rb") as f:
    while True:
        fp = f.tell()
        data = f.read(1)
        if data==b'':
            break
        print(f"fp:{fp},data:{data}")
"""
fp:0,data:b'['
fp:1,data:b'\xed'
fp:2,data:b'\x95'
fp:3,data:b'\x9c'
fp:4,data:b'\xea'
fp:5,data:b'\xb8'
fp:6,data:b'\x80'
fp:7,data:b']'
"""

def unread(file, count):
    file.seek(-count, 1)  # 1 seek_cur, 0 seek_first, 2 seek_end

print('*** binary mode unread ***')
with open("test.bin", "rb") as f:
    while True:
        fp1 = f.tell()
        data1 = f.read(1)
        fp2 = f.tell()
        unread(f, 1)
        fp3 = f.tell()
        data2 = f.read(1)
        if data1==b'' or data2==b'':
            break
        print(f"fp1:{fp1},data1:{data1},fp2:{fp2},fp3:{fp3},data2:{data2}")

"""
fp1:0,data1:b'[',fp2:1,fp3:0,data2:b'['
fp1:1,data1:b'\xed',fp2:2,fp3:1,data2:b'\xed'
fp1:2,data1:b'\x95',fp2:3,fp3:2,data2:b'\x95'
fp1:3,data1:b'\x9c',fp2:4,fp3:3,data2:b'\x9c'
fp1:4,data1:b'\xea',fp2:5,fp3:4,data2:b'\xea'
fp1:5,data1:b'\xb8',fp2:6,fp3:5,data2:b'\xb8'
fp1:6,data1:b'\x80',fp2:7,fp3:6,data2:b'\x80'
fp1:7,data1:b']',fp2:8,fp3:7,data2:b']'
"""