from threading import Timer
import random


def hello():
    global penumpang
    penumpang = random.randint(1, 36)
    print (penumpang)
    Timer(2, hello).start()

hello()

