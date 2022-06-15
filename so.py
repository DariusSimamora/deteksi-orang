ser = serial.Serial(
    port='COM5',
    baudrate = 9600,
    timeout=1)
while 1:
    x=str(ser.readline())
    x = re.findall("\d+\.\d+", x)
    x = float(x[0])
    return(x) #loop stopped
    print(x)