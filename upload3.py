from firebase import firebase
from threading import Timer


url = 'https://test-project-3dc48-default-rtdb.asia-southeast1.firebasedatabase.app/'
firebase = firebase.FirebaseApplication(url)

def kirim():
    global penumpang
    penumpang = totalLeft+totalRight
    firebase.put("/Test Val", "Value", penumpang)
    Timer(2, kirim).start()

kirim()




