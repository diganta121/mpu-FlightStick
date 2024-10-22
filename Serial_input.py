import serial


def readserial(comport, baudrate):

    ser = serial.Serial(comport, baudrate, timeout=0.1)         # 1/timeout is the frequency at which the port is read

    while True:
        data = ser.readline().decode().strip()
        if data:
            
            try:
                data = data.split()
                print(f"{float(data[0]):.2f} {float(data[1]):.2f} {data[2]} {data[3]} ")
            except:
                print(data)

if __name__ == '__main__':

    readserial('COM4', 115200)