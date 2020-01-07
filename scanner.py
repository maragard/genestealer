#!/usr/bin/env python3

import sys
import socket
import subprocess
import re
import requests

class scanner:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return

    def get_self_ip(self):
        curr_platform = sys.platform
        ip_find = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        if curr_platform != 'linux':
            return ip_find.findall(str(subprocess.check_output('ipconfig')))[0]
        else:
            return ip_find.findall(str(subprocess.check_output('ifconfig')))[0]

    def ping_scan(self, ip_addr):
        possible_targets = []
        ip_mask = '.'.join(ip_addr.split('.')[:-1]) + '.'
        for last in range(1, 255):
            candidate = ip_mask + str(last)
            if candidate != ip_addr:
                try:
                    subprocess.check_call(['ping', '-c1', '-i0.1', candidate])
                except:
                    pass
                possible_targets.append(candidate)
        return possible_targets

    def port_scan(self, target_ip, portnum):
        return self.sock.connect_ex((target_ip, portnum))

    def enumerate_endpoint(self, target_ip, endpoint_list):
        result = {}
        for end in endpoint_list:
            try:
                resp = requests.get("http://" + target_ip + "/" + end)
            except:
                pass
            result[end] = resp.status_code
        return result
