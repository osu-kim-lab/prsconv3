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
    # 'stats',
    # 'browser_files',
    # 'fast5_dir',
]

DESC = "Convert Tombo files to CSV files"
EPILOG = "version 3.0"
parser = argparse.ArgumentParser(description=DESC, epilog=EPILOG)

HELP = "which kind of input file to convert to CSV"
subparsers = parser.add_subparsers(help=HELP, dest='which_kind')

# Import all the engine modules and call the "register" method on each one
for engine in ENGINE_LIST:
    import_module('.engines.' + engine)
    locals()['engines.' + engine].register(subparsers)

args = parser.parse_args()

# Send args to to the engine. It will take things from here.
if args.which_kind:
    locals()['engines.' + args.which_kind].run(args)
