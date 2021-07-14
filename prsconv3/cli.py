'''
This module figures out which subcommand the user is trying to run.

Chris Kimmel
7-13-2021
chris.kimmel@live.com
'''

import argparse
from importlib import import_module

ENGINE_LIST = [
    'per_read_stats',
    'stats',
    'browser_files',
    # 'fast5_dir',
]

DESC = "Convert Tombo files to CSV files"
EPILOG = "version 3.0"
parser = argparse.ArgumentParser(description=DESC, epilog=EPILOG)

HELP = "which kind of input file to convert to CSV"
subparsers = parser.add_subparsers(help=HELP, dest='which_kind')

# Import all the engine modules and call the "register" method on each one
engine_dict = {name: import_module('engines.' + name) for name in ENGINE_LIST}
for engine in engine_dict.values():
    engine.register(subparsers)
