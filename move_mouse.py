from pynput.keyboard import Key, Listener
import pyautogui

def show(key):
    if key == Key.tab:
        print("enabled")
         
    if key != Key.tab:
        print("e")
         
    # by pressing 'delete' button 
    # you can terminate the loop 
    if key == Key.delete: 
        return False
 
# Collect all event until released
with Listener(on_press = show) as listener:
    listener.join()
