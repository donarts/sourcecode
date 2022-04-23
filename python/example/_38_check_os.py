import os
import sys

'''
https://docs.python.org/3/library/sys.html#sys.platform
AIX
'aix'
Linux
'linux'
Windows
'win32'
Windows/Cygwin
'cygwin'
macOS
'darwin'
'''
print(sys.platform)
# windows 32 / 64 bit 모두 'win32' 로 나옴

# 32/64 bit 구별방법
print(os.environ.get('PROCESSOR_ARCHITECTURE'))
print(os.environ.get('PROCESSOR_ARCHITEW6432'))
#Windows 64 bit
#AMD64
#None