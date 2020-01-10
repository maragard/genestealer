#!/usr/bin/env python3

import sys
import subprocess
import os

class scriptrunner:
    def __init__(self):
        return

    def run_script(self, script_name, *args, **kwargs):
        #may have to add stuff for windows-specific options
        command = "./" + script_name
        cmd_array = [command]
        cmd_array += args
        for key in kwargs:
            cmd_array += key + "=" + kwargs[key]
        try:
            subprocess.call(cmd_array)
        except:
            print(script_name + " failed.")
