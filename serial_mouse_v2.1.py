import pyautogui
import serial
import keyboard
import time
import threading
comport = 'COM5'
baudrate = 115200

d1 = {'x_off':0,
        'y_off':-200,
        'correct_state':False,
        'precise':False,
        'invert_x':True,
        'duration':0.01,
        'min_diff':0.30,
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


# pyautogui.PAUSE = 0.001
def mov_mouse(x,y,x1,y1):
    if d1['enbl']:
        if abs(x-x1)>d1['min_diff'] or abs(y-y1)>d1['min_diff']:
            pyautogui.moveTo(x=x,y=y,duration=0)
            pyautogui.PAUSE = 0.05

def Nsteps(start, end,n):
    step = (end - start) / (n-1)
    return [start + i * step for i in range(n)]

def deNoise(curr,prev,n):
    inter_points = []
    if len(prev) > 2:
        for i in range(2):
            t = Nsteps(prev[i],curr[i],n)
            inter_points.append(t)
    return inter_points


# TODO predict next movement to make it smoother 
# and reduce the sens if the diff between the prev and curr is very less


def get_data():
    global data
    ser = serial.Serial(comport, baudrate,timeout=0.2)
    while True:
        tdata = ser.readline().decode().strip()
        if tdata and d1['enbl']:
            try: 
                tdata = [float(x) for x in tdata.split()]
                data = tdata
                print(tdata)
            except:
                print(data)


def main():
    global data
    x,y = d1['x_off'],d1['y_off']
    curr = []
    prev = []
    curr_pos = []
    prev_pos = []
    temp = -1
    # 1/timeout is the frequency at which the port is read
    # move_mouse = threading.Thread(target=mov_mouse, args=(x,y))
    keyboard.add_hotkey('`',disable)
    keyboard.add_hotkey('/',disable_soft)
    keyboard.add_hotkey('*',correct_off_state)
    keyboard.add_hotkey('.',precise_state)
    while d1['loop']:
        #data = get_data(ser)
        curr = data
        if curr and d1['enbl']:
            try:
                x_angle = (curr[0])/1.2
                y_angle = (curr[1])/1.2
                s1 = time.time_ns()
                #print(data)
                # print(x_angle,y_angle)
                if d1['precise']:
                    x_angle /= 2
                    y_angle /= 2
                if d1['invert_x']:
                    x_angle *= -1
                x = (mouse_x3(x_angle,65,-60,0,1920)) - d1['x_off']
                y = (mouse_x3(y_angle,45,-45,0,1080)) - d1['x_off']
                curr_pos = [x,y]
                
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
                inter_p = deNoise(curr_pos, prev_pos,5)
                print('dl',inter_p)
                for i in range(len(inter_p[0])):
                    mov_mouse(inter_p[0][i],inter_p[1][i],prev[0],prev[1])
                else:
                    time.sleep(0.04)
                s3 = time.time_ns()
                print(s3-s1)
                # move_mouse.join()
                # move_mouse.start()
                
                prev = curr
                prev_pos = curr_pos
            except:
                prev = curr
                prev_pos = curr_pos
                

data = []
data_getter = threading.Thread(target=get_data,daemon=True)
data_getter.start()
main()
