from firebase import firebase
from threading import Timer
import random

url = 'https://fir-rt-95bc6-default-rtdb.asia-southeast1.firebasedatabase.app/'
firebase = firebase.FirebaseApplication(url)

def kirim():
    global penumpang
    penumpang = random.randint(1, 36)
    firebase.put("/customer2", "Value", penumpang)
    print (penumpang)
    Timer(2, kirim).start()

kirim()




