#!/usr/bin/env python3

import argparse
import pathlib

def main():
    parser = argparse.ArgumentParser(prog="")
    parser.add_argument('target',
                        help="Initial worm target")
    parser.add_argument('-i', '--ignore',
                        help="IP addr to ignore",
                        action='extend')

    args = parser.parse_args()
    print(args)

if __name__ == '__main__':
    main()
