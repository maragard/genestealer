#!/usr/bin/env python3

import os
import sys

def main():
    root = os.path.join('..')
    for directory, subdir_list, file_list in os.walk(root):
        for name in file_list:
            source = os.path.join(directory, name)
            print(f'File with name: {source}')

if __name__ == '__main__':
    main()
