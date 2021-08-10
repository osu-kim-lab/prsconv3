'''
This module contains the code and interface to convert a fasta file into a CSV file.

Chris Kimmel
7-14-2021
chris.kimmel@live.com
'''

from warnings import warn


DESCRIPTION = '''
This command converts FASTA files to CSV files. The FASTA file must be of a
certain form.

The first line of the FASTA should begin with a ">", and the remainder of the
line should be a description of the sequence. The rest of the file should
be the sequence associated with this description, with no whitespace other than
newlines.

In particular, the code will break, perhaps without warning, if there is more
than one sequence in the FASTA file.

The output CSV has columns "description", "pos_0b", and "base".

Usage Example:
python prsconv3 fasta tests/files/fasta/RNA_section__454_9627.fa RNA_section__454_9627.fa.csv
'''

def register(subparsers):
    '''Add a subcommand to the subparsers object, thereby exposing the
    methods in this module via the command-line interface.'''

    parser = subparsers.add_parser('fasta', help='.fasta files',
        description=DESCRIPTION)

    parser.add_argument('input-filepath', metavar='INPUT-FILEPATH',
        help='The FASTA file to read')

    parser.add_argument('output-filepath', metavar='OUTPUT-FILEPATH',
        help='Where to write the CSV output (including the .csv extension)')


def fasta_to_list_of_triples(inbuffer):
    '''Take a fasta file from inbuffer and return a list of (description,
    pos_0b, base) triples that represent every position on every sequence in
    the file.

    Every entry in every tuple is a string.'''

    # Get the first description
    description = inbuffer.readline()
    assert description.startswith('>'), 'The first line in the FASTA must be a '\
        '">"-initiated description.'
    description = description[1:].strip() # remove ">" symbol and surrounding whitespace

    retval = []
    pos = 0
    for line in inbuffer.readlines():
        line = line.strip() # to remove trailing \n
        for base in line:
            if base == '>':
                raise NotImplementedError('This FASTA file appears to have '
                    'multiple sequences in it. Only one sequence per FASTA is '
                    'currently supported.')
            retval.append((description, str(pos), base.upper()))
            pos += 1
    return retval


def run(args):
    global pd
    import pandas as pd
    
    MESS = 'This module can currently only accept a FASTA file in which the '\
           'first line is a ">" identifier, and the remaining lines are the '\
           'corresponding nucleotide sequence.'
    warn(MESS)

    with open(args.input_filepath, 'rt') as input_file:
        rows = fasta_to_list_of_triples(input_file)

    with open(args.output_filepath, 'wr') as output_file:
        output_file.write(','.join(['description', 'pos_0b', 'base']) + '\n')
        output_file.write('\n'.join(','.join(row) for row in rows) + '\n')
