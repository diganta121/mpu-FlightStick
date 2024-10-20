from pynput.keyboard import Key, Listener
import pyautogui

data = {'x':-100,
        'y':-1,
        'duration':0.1,
        'enbl':False,
        }


def show(key):
    #press tab to enable / disable
    if key == Key.tab:
        data['enbl'] = not data['enbl']
        print(data['enbl'])
    if data['enbl']: 
        # if space is pressed press w 
        # for testing
        if key == Key.space:
            pyautogui.press('w')
            pyautogui.moveRel(data['x'],data['y'],duration=data['duration'])


    # by pressing 'delete' button 8
    # you can terminate the loop 
    if key == Key.delete: 
        return False
 

# main loop
with Listener(on_press = show) as listener:
    listener.join()
