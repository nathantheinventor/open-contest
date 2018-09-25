from threading import Timer, Thread
import time
import os
import sys

def kill():
    print("TLE")
    exit(1)

testCases = int(sys.argv[1])
timeLimit = int(sys.argv[2])

def runCode(timeout):
    for i in range(testCases):
        if os.system("python /source/code.py < /source/in{0}.txt > /source/out{0}.txt 2> /source/err{0}.txt".format(i)) != 0:
            print("runtime_error")
            timeout.cancel()
            exit(1)
    print("ok")
    timeout.cancel()
    exit(0)

timeout = Timer(timeLimit, kill)
timeout.start()
thread = Thread(target=runCode, args=(timeout,), daemon=True)
thread.start()