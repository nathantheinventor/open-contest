from generator import generateStatic, generateDynamic
import time

generateStatic()
while True:
    generateDynamic()
    time.sleep(1)
