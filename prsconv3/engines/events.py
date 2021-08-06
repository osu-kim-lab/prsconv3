'''
This module contains the code and interface to convert information from the
events tables of fast5s into CSV files.

Chris Kimmel
8-6-2021
chris.kimmel@live.com
'''

from warnings import warn
from inspect import cleandoc


DEFAULT_CHRM = 'truncated_hiv_rna_genome'

SLOTS_TO_IMPORT = [
    'norm_mean',
    'norm_stdev',
    'start',
    'length',
]


def register(subparsers):
    '''Add a subcommand to the subparsers object, thereby exposing the
    methods in this module via the command-line interface.'''

    parser = subparsers.add_parser('events',
        help='fast5 events tables (this includes dwell times)')

    parser.add_argument('--strand', metavar='STRAND', default='+',
        choices=['+', '-'], help='Only reads mapped to this strand will appear '
        'in output ("+" or "-")')

    parser.add_argument('--chrm', metavar='CORRECTED-GROUP',
        help='Only reads mapped to this chromosome will appear in output',
        default='truncated_hiv_rna_genome')

    parser.add_argument('output_path', help='Path of the CSV file to be '
        'written (including the .csv extension)', metavar='OUTPUT-FILEPATH',
        type=str)

    parser.add_argument('--corr-grp', metavar='CORRECTED-GROUP',
        help='Which corrected group of the fast5 files should be read',
        default='RawGenomeCorrected_000')

    parser.add_argument('fast5_dirs', help='The fast5 directories to read.',
        metavar='FAST5-DIRS', nargs='+')


def run(args):
    global tombo_helper, pd
    from tombo import tombo_helper
    import pandas as pd

    MESS = '''This module is still under development.'''
    warn(cleandoc(MESS))

    reads_index = tombo_helper.TomboReads(args.fast5_dirs)
    cs_reads = reads_index.get_cs_reads(args.chrm, args.strand)
    slot_contents = [tombo_helper.get_multiple_slots_read_centric(read,
        SLOTS_TO_IMPORT, None) for read in cs_reads]

    # TODO: Use the mapped_start and mapped_end attributes of the corrected group to assign genomic position numbers
    # TODO: Add read IDs
    results = pd.DataFrame(dict(zip(SLOTS_TO_IMPORT, slot_contents)))
    results.to_csv(args.output_path)
