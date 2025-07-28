import sys
input = sys.stdin.readline.rstrip('\r\n')


import os, io
input = io.BytesIO(os.read(0, os.fstat(0).st_size)).readline


import sys
print = sys.stdout.write # 줄바꿈 없음


import sys, os, io, atexit
stdout = io.BytesIO()
sys.stdout.write = lambda s: stdout.write(s.encode("ascii"))
atexit.register(lambda: os.write(1, stdout.getvalue()))



# 최종
import sys, os, io, atexit
input = io.BytesIO(os.read(0, os.fstat(0).st_size)).readline
stdout = io.BytesIO()
sys.stdout.write = lambda s: stdout.write(s.encode("ascii"))
atexit.register(lambda: os.write(1, stdout.getvalue()))