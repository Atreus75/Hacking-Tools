import requests
from time import sleep


print('\n\n\n\033[4;34m[+]                          DTORY FINDER\033[1;34m                            [+]\033[m')

# Lê a url inserida pelo usuário e a formata para ser usada
url = input('\n\n\n     Endereço a ser escaneado: \033[1;34m')
if 'http://' not in url and 'https://' not in url:
    url = f'http://{url}'.rstrip('/')


# Verifica se o endereço informado está acessível ou é inválido
try:
    print('     [+] Testando conexão com o alvo...')
    requests.get(url)
except:
    print('     [+] A conexão com o host falhou. Verifique se o mesmo está online ou se o endereço foi informado corretamente.')
    exit()
print('     [+] Conexão bem sucedida.')


# Pede uma wordlist ao usuário e verifica se a mesma existe
wordlist = str(input('\n\033[m     Caminho completo da wordlist a ser usada: ')).strip().lower()
try:
    wordlist = open(f'{wordlist}', 'r', encoding='utf-8').readlines()
except:
    print('\033[1;34m       [+] O arquivo não pode ser encontrado.')
    exit()
print('\033[1;34m     \n            [+] Iniciando ataque\n\n\033[m')


# Realiza o ataque
for l in wordlist:
    l = l.rstrip()
    req = requests.get(f'{url}/{l}')
    code = f'{req.status_code}'
    if code == '200':
        sleep(0.5)
        print(f'\033[1;32m    --> {url}/{l} | Code {code}\033[m')
    else:
        print(f'\033[K    --> {url}/{l}', end='\r')

print('\n\n[+] Ataque Finalizado.')