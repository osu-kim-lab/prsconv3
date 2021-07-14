'''
This module contains the code and interface to convert a fasta file into a CSV file.

Chris Kimmel
7-14-2021
chris.kimmel@live.com
'''

from sys import stdin, stdout
from warnings import warn

def register(subparsers):
    '''Add a subcommand to the subparsers object, thereby exposing the
    methods in this module via the command-line interface.'''

    parser = subparsers.add_parser('fasta',
        description='.fasta files (streams from stdin to stdout)')


def fasta_to_list_of_triples(inbuffer):
    '''Take a fasta file from inbuffer and return a list of (description,
    pos_zb, base) triples that represent every position on every sequence in
    the file.

    Every entry in every tuple is a string.'''

    # Get the first description
    description = inbuffer.readline()
    assert description.startswith('>'), 'The first line in the FASTA must be a '\
        '">"-initiated comment.'
    description = description[1:].strip() # remove ">" symbol and surrounding whitespace

    retval = []
    pos = 0
    for line in inbuffer.readlines():
        line = line.strip() # to remove trailing \n
        for base in line:
            retval.append((description, str(pos), base.upper()))
            pos += 1
    return retval


def run(args):
    global pd
    import pandas as pd
    
    MESS = '''This module is incomplete. It can currently only accept a FASTA
    file in which the first line is a ">" command, and the remaining lines are
    the corresponding nucleotide sequence.'''
    warn(MESS)

    rows = fasta_to_list_of_triples(stdin)
    stdout.write(','.join(['description', 'pos_zb', 'base']) + '\n')
    stdout.write('\n'.join(','.join(row) for row in rows) + '\n')
