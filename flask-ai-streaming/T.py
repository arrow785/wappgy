import time
import sys
strx = "Flask是一个轻量级的Python Web框架，它简单易用但功能强大。"
def yield_():
    for c in strx:
        yield c
       

for chunk in yield_():
    sys.stdout.write(chunk)
    sys.stdout.flush()
    time.sleep(0.1)  # 模拟延迟
