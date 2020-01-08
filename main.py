#!/usr/bin/env python3

import argparse
import pathlib
from ipaddress import ip_address

def main():
    parser = argparse.ArgumentParser(prog="GENESTEALER")
    parser.add_argument('target',
                        help="Initial target for worm",
                        type=ip_address)
    parser.add_argument('-i', '--ignore',
                        help="IP addr(s) to ignore",
                        action='extend',
                        nargs='+',
                        metavar='safe_ip',
                        type=ip_address)

    args = parser.parse_args()
    print(args)


if __name__ == '__main__':
    main()
