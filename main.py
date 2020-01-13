#!/usr/bin/env python3

import argparse
import pathlib
from ipaddress import ip_address

def attack(args):
    #step 1 perform target ping scan
    #step 2 perform target os detection
    #step 3 perform target port scan on necessary ports
    #step 4 pick and execute exploit
    #step 5 post exploit (potentially repeat 2 thru 4 on all targets in sequence)

def main():
    parser = argparse.ArgumentParser(prog="GENESTEALER")
    parser.add_argument('target',
                        action='extend',
                        nargs='+',
                        help="Initial target for worm",
                        type=ip_address)

    args = parser.parse_args()
    print(args)
    attack(args)


if __name__ == '__main__':
    main()
