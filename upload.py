from firebase import firebase

myDB = firebase.FirebaseApplication("https://penumpang-6ad20-default-rtdb.asia-southeast1.firebasedatabase.app//", None)

print(myDB)

name = input("Darius")

data = {
    "Darius": name,
    "Usia": 23
}

myDB.post("Video", data)