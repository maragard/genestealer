#!/usr/bin/env python3

import sys
import socket
import subprocess
import re
import requests
import concurrent.futures

class scanner:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.executor = concurrent.futures.ThreadPoolExecutor(254)
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
        def ping_helper(self, candidate, self_ip):
            nonlocal possible_targets
            if candidate != self_ip:
                try:
                    subprocess.check_output(['ping', '-c', '1', candidate])
                    possible_targets.append(candidate)
                except:
                    pass

        ip_mask = '.'.join(ip_addr.split('.')[:-1]) + '.'

        candidates = [ip_mask + str(last) for last in range(1,255)]
        ping_cands = [executor.submit(ping_helper, candidate=cand, self_ip=ip_addr) for cand in candidates]

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
