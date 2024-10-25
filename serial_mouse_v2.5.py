import pyautogui
import serial
import keyboard
import time
import threading
import multiprocessing
comport = 'COM5'
baudrate = 115200
d1 = {'x_off':10,
        'y_off':-200,
        'correct_state':False,
        'precise':False,
        'invert_x':True,
        'duration':0.1,
        'enbl':True,
        'loop':True
        }

def disable(*_):
    d1['loop'] = False

def disable_soft(*_):
    d1['enbl'] = not d1['enbl']

def correct_off_state(*_):
    d1['correct_state'] = True
def precise_state():
    d1['precise'] = not d1['precise']
def data_sp(s):
    a = []
    for i in str(s).split():
        try:
            a.append(float(i))
        except:
            return
    return a
dist = 0.1

def mouse_x3(x_val,x1,x2,y1,y2):
    # -80 , 80 , 0 , 1920
    return y1 + (x_val - x1) * (y2 - y1) / (x2 - x1)

def mov_mouse(x,y):
    pyautogui.moveTo(x=x,y=y,duration=0)


def deNoise(x1,x2,y1,y2):
    # TODO de noising of input
    # increase rate of input
    pass

# TODO use multithredding to speed up , optimize code

# plan 1 
input_data = []

def get_data():
    ser = serial.Serial(comport, baudrate,timeout=0.2)
    while d1['loop']:
        tdata = ser.readline().decode().strip()
        if tdata and d1['enbl']:
            try: 
                tdata = [float(x) for x in tdata.split()]
                print(tdata)
                with open('f.txt','w') as f:
                    f.write(str(tdata))
            except:
                print(tdata)

def read_data():
    with open('f.txt','r') as f:
        a = list(eval(f.read())[1:-1])
    return a
def main():
    x,y = d1['x_off'],d1['y_off']
    curr = []
    prev = []
    temp = -1
    print('main thread')
    # 1/timeout is the frequency at which the port is read
    # move_mouse = threading.Thread(target=mov_mouse, args=(x,y))
    while d1['loop']:
        #s1 = time.time_ns()
        #data = get_data(ser)
        curr = read_data()
        if curr and d1['enbl']:
            try:
                #s1 = time.time_ns()
                #print(data)
                x_angle = (curr[0])/1.2
                y_angle = (curr[1])/1.2
                # print(x_angle,y_angle)
                if d1['precise']:
                    x_angle /= 2
                    y_angle /= 2
                if d1['invert_x']:
                    x_angle *= -1
                x = (mouse_x3(x_angle,65,-60,0,1920)) - d1['x_off']
                y = (mouse_x3(y_angle,40,-40,0,1080)) - d1['y_off']
                
                if d1['correct_state']:
                    if temp == 0:
                        d1['x_off'] = x - prev[0]
                        d1['y_off'] = y - prev[1]
                        prev.clear()
                        temp = -1
                        d1['correct_state'] = False
                        print(d1)
                    elif temp == -1:
                        prev = [x, y]
                        temp = 10
                        time.sleep(1)
                        continue
                    else:
                        temp -= 1
                        continue
                #print(f"{x:.2f} {y:.2f}")
                s2 = time.time_ns()
                mov_mouse(x,y)
                # move_mouse.join()
                # move_mouse.start()
                
                s3 = time.time_ns()
                prev = curr
                print(time.perf_counter())
            except:
                pass


if __name__ == "__main__":
    data_getter = multiprocessing.Process(target=get_data)
    maint = multiprocessing.Process(target=main)
    keyboard.add_hotkey('`',disable)
    keyboard.add_hotkey('/',disable_soft)
    keyboard.add_hotkey('*',correct_off_state)
    keyboard.add_hotkey('.',precise_state)
    data_getter.start()
    maint.start()
    
    maint.join()
    data_getter.join()