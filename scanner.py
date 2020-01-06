#!/usr/bin/env python3

import sys
import socket
import subprocess
import re

class scanner:
    def __init__(self):
        return 0

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
                    subprocess.check_call(['ping', '-c1', ip_mask + candidate])
                    possible_targets.append(ip_mask + candidate)
                except:
                    pass
        return possible_targets
