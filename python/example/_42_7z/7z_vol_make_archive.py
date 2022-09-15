import py7zr  # pip install py7zr
import multivolumefile  # pip install multivolumefile
import random
import os


# https://py7zr.readthedocs.io/en/latest/user_guide.html
# https://py7zr.readthedocs.io/en/latest/api.html

def make_random_file(file_name, file_size):
    f = open(file_name, "wb")
    for i in range(int(file_size / 2)):
        random_v = random.random()
        random_v = (random_v * 65536) % 256
        random_v = int(random_v)
        f.write(random_v.to_bytes(2, 'big'))
    f.close()


orifile = "in/test.bin"  # 압축 하려고 하는 파일
outfile = "out/output1.7z"  # 압축된 결과 파일

try:
    os.mkdir("out")
except:
    pass
try:
    os.mkdir("in")
except:
    pass

# 임시 파일
make_random_file(orifile, 3 * 1024)

filters = [{'id': py7zr.FILTER_COPY}]
'''
LZMA2 + Delta
[{'id': FILTER_DELTA}, {'id': FILTER_LZMA2, 'preset': PRESET_DEFAULT}]

LZMA2 + BCJ
[{'id': FILTER_X86}, {'id': FILTER_LZMA2, 'preset': PRESET_DEFAULT}]

LZMA2 + ARM
[{'id': FILTER_ARM}, {'id': FILTER_LZMA2, 'preset': PRESET_DEFAULT}]

LZMA + BCJ
[{'id': FILTER_X86}, {'id': FILTER_LZMA}]

LZMA2
[{'id': FILTER_LZMA2, 'preset': PRESET_DEFAULT}]

LZMA
[{'id': FILTER_LZMA}]

BZip2
[{'id': FILTER_BZIP2}]

Deflate
[{'id': FILTER_DEFLATE}]

ZStandard
[{'id': FILTER_ZSTD, 'level': 3}]

PPMd
[{'id': FILTER_PPMD, 'order': 6, 'mem': 24}]

[{'id': FILTER_PPMD, 'order': 6, 'mem': "16m"}]

Brolti
[{'id': FILTER_BROTLI, 'level': 11}]

7zAES + LZMA2 + Delta
[{'id': FILTER_DELTA}, {'id': FILTER_LZMA2, 'preset': PRESET_DEFAULT}, {'id': FILTER_CRYPTO_AES256_SHA256}]

7zAES + LZMA2 + BCJ
[{'id': FILTER_X86}, {'id': FILTER_LZMA2, 'preset': PRESET_DEFAULT}, {'id': FILTER_CRYPTO_AES256_SHA256}]

7zAES + LZMA
[{'id': FILTER_LZMA}, {'id': FILTER_CRYPTO_AES256_SHA256}]

7zAES + Deflate
[{'id': FILTER_DEFLATE}, {'id': FILTER_CRYPTO_AES256_SHA256}]

7zAES + BZip2
[{'id': FILTER_BZIP2}, {'id': FILTER_CRYPTO_AES256_SHA256}]

7zAES + ZStandard
[{'id': FILTER_ZSTD}, {'id': FILTER_CRYPTO_AES256_SHA256}]
'''
zfilelist = [] # 파일 목록을 저장하는 변수
# 압축 안함 FILTER_COPY
with multivolumefile.open(outfile, mode='wb', volume=1023) as target_archive:
    with py7zr.SevenZipFile(target_archive, 'w', filters=filters) as archive:
        archive.writeall(orifile)

    for fileinfo in target_archive._fileinfo:
        zfilelist.append(fileinfo.filename)

# 파일 이름을 처리할때는 모두 완료된후 아래와 같은 형태로 처리 하도록 합니다.
for filename in zfilelist:
    print(filename)

# out\output1.7z.0001
# out\output1.7z.0002
# out\output1.7z.0003
# out\output1.7z.0004


# 기본 압축
outfile = "out/output2.7z"  # 압축된 결과 파일
with multivolumefile.open(outfile, mode='wb', volume=1023) as target_archive:
    with py7zr.SevenZipFile(target_archive, 'w') as archive:
        archive.writeall(orifile)

    for fileinfo in target_archive._fileinfo:
        print(fileinfo.filename)

# out\output2.7z.0001
# out\output2.7z.0002

# FILTER_ZSTD 압축
filters = [{'id': py7zr.FILTER_ZSTD}]
outfile = "out/output3.7z"  # 압축된 결과 파일
with multivolumefile.open(outfile, mode='wb', volume=1023) as target_archive:
    with py7zr.SevenZipFile(target_archive, 'w', filters=filters) as archive:
        archive.writeall(orifile)

    for fileinfo in target_archive._fileinfo:
        print(fileinfo.filename)

# out\output3.7z.0001
# out\output3.7z.0002
# out\output3.7z.0003

# 기본 압축 : 경로 저장 안함
outfile = "out/output4.7z"  # 압축된 결과 파일
with multivolumefile.open(outfile, mode='wb', volume=1023) as target_archive:
    with py7zr.SevenZipFile(target_archive, 'w') as archive:
        archive.write(orifile, arcname="a.bin")

    for fileinfo in target_archive._fileinfo:
        print(fileinfo.filename)

# out\output4.7z.0001
# out\output4.7z.0002
