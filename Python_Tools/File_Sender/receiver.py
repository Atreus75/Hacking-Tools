import socket
import os
from argparse import ArgumentParser

# Define os argumentos da linha de comando
parser = ArgumentParser(usage='python receiver.py --port PORT')
parser.add_argument('--port', help='Target port.', required=False)
args = parser.parse_args()


try:
    #                             IPv4              TCP/IP
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print("Ocorreu um preblema ao criar o socket")
    exit()


# Define o host da conexão e a porta a escutar
host = '127.0.0.1'
port = int(args.port) if args.port else 4444
buffer = 4096


# Começa a escutar na porta escolhida
tcp_socket.bind((host, port)) 


# Define o número de conexões simultâneas que serão permitidas
tcp_socket.listen(1)


while True:
    # Espera a conexão com um cliente e captura seu IP e Porta usados para se conectar
    connection, host = tcp_socket.accept()
    print(f'\033[1;36m[+] Conexão estabelecida com  {host[0]}:{host[1]}')
    
    received = connection.recv(buffer).decode()
    file_name, file_size = received.split(' | ')

    file_name = os.path.basename(file_name)
    file_size = int(file_size.replace('bytes', '').strip())


    with open(file_name, "wb") as file:
        while True:
            received_bytes = connection.recv(buffer)
            if not received_bytes:
                break
            file.write(received_bytes)
    # Fecha a conexão
    print('[+] Arquivo recebido!')
    connection.close
    break

# Para de escutar a porta e a fecha
tcp_socket.close()
