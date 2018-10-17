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
        result = "ok"
        if os.system("ruby /source/code.rb < /source/in{0}.txt > /source/out/out{0}.txt 2> /source/out/err{0}.txt".format(i)) != 0:
            result = "runtime_error"
        with open("/source/out/result{0}.txt".format(i), "w") as f:
            f.write(result)
    print("ok")
    timeout.cancel()
    exit(0)

timeout = Timer(timeLimit, kill)
timeout.start()
thread = Thread(target=runCode, args=(timeout,), daemon=True)
thread.start()