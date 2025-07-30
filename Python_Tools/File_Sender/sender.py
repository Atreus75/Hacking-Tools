import socket
from time import sleep
from argparse import ArgumentParser

import os

# Define os argumentos da linha de comando
parser = ArgumentParser(usage='python sender.py --host HOST --port PORT')
parser.add_argument('--host', help='Target host.', required=False)
parser.add_argument('--port', help='Target port.', required=False)
parser.add_argument('--file', help='Complete file path', required=False)
args = parser.parse_args()

print('\n\n--------------------------------------------------------')
print('\033[1;34m[+]\33[m                  \33[4;31mFILE SENDER\033[m                  \33[1;34m[+]\33[m')
print('--------------------------------------------------------\n')

# A quantidade de bytes do arquivo que vão ser enviados por vez
buffer = 4096


try:
    if args.port and args.host:
        host, port = args.host, args.port
    else:
        # Pergunta ao usuário o endereço e porta a se conectar
        host = str(args.host).strip() if args.host else str(input('Host: ')).strip()
        port = str(args.port).strip() if args.port else str(input('Port: ')).strip()
    # Verifica se o endereço IP e a porta estão corretos
    if len(host.split('.')) != 4 or not port.isnumeric():
        print('\n\033[1;31m[-] Invalid host or port.')
        exit()
    file_path = str(args.file).strip() if args.file else str(input('Full file path: '))
    try:
        file_size = os.path.getsize(file_path)
    except:
        print('\n\033[1;31m[-] Ocorreu um erro ao localizar o arquivo. Verifique se o caminho está correto e tente novamente.')
        exit()
    
    try:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('\n\033[1;36m[+] Socket iniciado com sucesso!')
        sleep(1)
    except socket.error:
        print('\n\033[1;31m[-] Ocorreu um erro ao iniciar o socket.')
        exit()

    try:
        print(f'[+] Tentado conexão com: {host}:{port}')
        tcp_socket.connect((host, int(port)))
        sleep(1)
        print('[+] Conexão bem sucedida!')
        sleep(1)
    except:
        print('\n\033[1;31m[-] Ocorreu um erro ao se conectar ao host. Verifique se endereço e porta foram digitados corretamente.')
        exit()  

    
    file_name = file_path[::-1]
    if '/' in file_name or '\\' in file_name:
        try:    
            file_name = file_name[:file_name.index('\\')]
        except:
            file_name = file_name[:file_name.index('/')]
        file_name = file_name[::-1]

    print(f'[+] Enviando {file_name} | {file_name} bytes')
    tcp_socket.send(f"{file_name} | {file_size}".encode())

    try:
        with open(file_path, 'rb') as file:
            while True:
                bytes_read = file.read(buffer)
                if not bytes_read:
                    break
                   
                tcp_socket.sendall(bytes_read)
            print('[+] Arquivo enviado com sucesso!')
            print("\033[1;32m[+] Fechando programa...\n\n")
            tcp_socket.close()
    except:
        print('\033[1;31m[-] Ocorreu um erro ao enviar o arquivo')


except KeyboardInterrupt:
    print("\033[1;32m\n\n[+] Fechando programa...")
