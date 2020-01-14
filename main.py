#!/usr/bin/env python3

import argparse
import pathlib
from ipaddress import ip_address
from shocker import shockshell

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
        if args.mode == 'manual':
            for victim_ip in args.target:
                print(f"Manual attack started against {victim_ip}")
                # scan
                # print scan output
                # id exploit to use
                # attack
        else:
            # The same but for all visible network ranges
            pass

if __name__ == '__main__':
    main()
