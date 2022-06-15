from threading import Timer
import random

def kirim():
    global penumpang
    penumpang = random.randint(1, 36)
    Timer(2, kirim).start()



kirim()