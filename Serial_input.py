import serial

def read_serialinf(comport, baudrate):

    ser = serial.Serial(comport, baudrate, timeout=0.1)
    while True:
        data = ser.readline().decode().strip()
        
        if data:
            try:
                data = data.split()
                data = (f"{float(data[0]):.2f} {float(data[1]):.2f} {data[2]} {data[3]} {data[4]}")
                with open('inp.txt','a') as f:
                    f.write()
            except:
                print(data)
def read_serial(comport, baudrate):

    ser = serial.Serial(comport, baudrate, timeout=0.1)
    data = ser.readline().decode().strip()
    if data:
        try:
            data = data.split()
            data = (f"{float(data[0]):.2f} {float(data[1]):.2f} {data[2]} {data[3]} {data[4]}")
            with open('inp.txt','a') as f:
                f.write()
        except:
            print(data)



if __name__ == '__main__':

    read_serialinf('COM4', 115200)