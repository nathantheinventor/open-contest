from generator import generateStatic, generateDynamic
import time

generateStatic()
for i in range(1):
    generateDynamic()
    time.sleep(1)
