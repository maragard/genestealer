#!/usr/bin/env python3

import sys
import socket
import subprocess
import re
import requests
import concurrent.futures

#basic scanning utility class
class scanner:
    #class doesn't need external arguments upon instantiation
    def __init__(self):
        #declare socket and executor objects up here to save the headache
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.executor = concurrent.futures.ThreadPoolExecutor(254)
        return

    #figure out what the current ip address is from the system
    def get_self_ip(self):
        curr_platform = sys.platform
        #regex matcher to extract the address from the output of ifconfig
        ip_find = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        #windows calls it 'ipconfig' instead of 'ifconfig'
        if curr_platform != 'linux':
            return ip_find.findall(str(subprocess.check_output('ipconfig')))[0]
        else:
            return ip_find.findall(str(subprocess.check_output('ifconfig')))[0]

    #rudimentary ping scan
    def ping_scan(self, ip_addr):
        possible_targets = []
        #define nested helper function that actually makes the ping call
        def ping_helper(self, candidate, self_ip):
            nonlocal possible_targets
            if candidate != self_ip:
                try:
                    subprocess.check_output(['ping', '-c', '1', candidate])
                    possible_targets.append(candidate)
                except:
                    pass

        #assume 24 bit netmask, and generate candidate IPs that way
        ip_mask = '.'.join(ip_addr.split('.')[:-1]) + '.'

        candidates = [ip_mask + str(last) for last in range(1,255)]
        #attempt to multithread the ping calls because those can take a while
        ping_cands = [executor.submit(ping_helper, candidate=cand, self_ip=ip_addr) for cand in candidates]

        return possible_targets

    #use the socket library to attempt to connect to a port; returns 0 if successful
    def port_scan(self, target_ip, portnum):
        return self.sock.connect_ex((target_ip, portnum))

    #basic web enumeration; try enpoints and record the status codes that come back
    def enumerate_endpoint(self, target_ip, endpoint_list):
        result = {}
        for end in endpoint_list:
            try:
                resp = requests.get("http://" + target_ip + "/" + end)
            except:
                pass
            result[end] = resp.status_code
        return result
