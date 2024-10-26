import keyboard
d = {'a':True}
def disable():
    d['a'] = False
keyboard.add_hotkey('`',disable)
while d['a']:
    print('bbbb')