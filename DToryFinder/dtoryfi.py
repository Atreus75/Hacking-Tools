import requests
from sys import argv
from time import sleep


class Errors():
    def __init__(self):
        pass
    def Empty_Arguments(self):
        print('\n\033[1;31mError:\033[m Make sure you passed all parameters.')
    def Invalid_Wordlist_Path(self, path):
        print(f'\n\033[1;31mError:\033[m Path: {path} its not valid!')
    def Connection_Failure(self):
        print('     \033[1;31m[+]\033[m Connection failure')
    def Force_exit(self):
        print('\n\033[1;31mKeyboard Interrupt\033[m')
    
def help():
    print('\033[1;34mUsage:\033[m ./dtoryfi.py [path to wordlist] [url]')



Errors = Errors()
# Presentation
print('\n\n\n\033[1;34m[+]  DTORY FINDER  [+]\033[m\n'.center(20))

# Read and format the url and wordlist gived by the user
try:
    wordlist = argv[1]
    url = argv[2]
except IndexError:
    Errors.Empty_Arguments()
    help()
    exit()

if 'http://' not in url or 'https://' not in url:
    url = f'http://{str(url)}/'
elif url[-1] != '/':
    url = f'{url}/'

url = url.strip().lower()
wordlist = str(wordlist).strip().lower()

# Validates the address
try:
    print(f'     [+] Testing connection to the target: {url}')
    requests.get(url)
    print('     \033[1;34m[+]\033[m Connection success.')
except:
    Errors.Connection_Failure()
    exit()

# Validates the wordlist
try:
    wordlist = open(f'{wordlist}', 'r', encoding='utf-8').readlines()
except:
    Errors.Invalid_Wordlist_Path(path=wordlist)
    help()
        
        
print('\n\033[1;34m[+]\033[m Starting Directory Enumeration:\n')


# Enumeration 
try:
    for l in wordlist:
        l = l.rstrip()
        req = requests.get(f'{url}{l}')
        code = f'{req.status_code}'
        if code in ['200', '301', '403']:
            sleep(0.5)
            print(f'\033[1;32m    --> {url}{l} | Code {code}\033[m')
        else:
            print(f'\033[K    --> {url}{l}', end='\r')   
except KeyboardInterrupt:
    Errors.Force_exit()

print('\n\033[1;34m[+] Finished.\033[m')
