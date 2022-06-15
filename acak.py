from threading import Timer

text = ""
def hello():
    global text
    text +="."
    print (text)
    Timer(1, hello).start()

hello()


