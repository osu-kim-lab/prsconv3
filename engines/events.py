'''
This module contains the code and interface to convert information from the
events tables of fast5s into CSV files.

Chris Kimmel
8-6-2021
chris.kimmel@live.com
'''


# pylint: disable=invalid-name,global-statement,import-outside-toplevel


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
        help='fast5 events tables from directories of fast5 files (this '
            'includes dwell times)')

    parser.add_argument('--strand', metavar='STRAND', default='+',
        choices=['+', '-'], help='Only reads mapped to this strand will appear '
        'in output ("+" or "-")')

    parser.add_argument('--chrm', metavar='CORRECTED-GROUP',
        help='Only reads mapped to this chromosome will appear in output',
        default='truncated_hiv_rna_genome')

    parser.add_argument('--corr-grp', metavar='CORRECTED-GROUP',
        help='Which corrected group of the fast5 files should be read',
        default='RawGenomeCorrected_000')

    parser.add_argument('fast5_dirs', help='The fast5 directories to read.',
        metavar='FAST5-DIRS', nargs='+')

    parser.add_argument('output_path', help='Path of the CSV file to be '
        'written (including the .csv extension)', metavar='OUTPUT-FILEPATH',
        type=str)


def read_to_df(read, slots_to_import, corr_grp):
    '''
    This is a wrapper for tombo_helper.get_multiple_slots_read_centric().  In
    addition to the returned value of get_multiple_slots_read_centric(), this
    subroutine also returns read_id and a zero-based positional index.

    Arguments:
        read:
            a tombo_helper.readData object
        slots_to_import:
            slots from the events table to fetch
            (valid values: norm_mean, norm_stdev, start, length, base)
        corr_grp:
            which corrected group of the fast5 file to fetch results from

    Returns:
        pandas dataframe:
            The index is a zero-based genomic position. There is one column for
            every slot in slots_to_import, plus a "read_id" column
    '''
    global np, tombo_helper, pd
    import numpy as np
    import pandas as pd
    from tombo import tombo_helper

    # Care must be taken to avoid reversing the events table along the genomic-
    # position axis. See https://nanoporetech.github.io/tombo/rna.html

    read_id = read.read_id
    index_0b = np.arange(read.start, read.end)
    slot_contents = zip(*tombo_helper.get_multiple_slots_read_centric(read,
        SLOTS_TO_IMPORT, corr_grp))

    # sometimes it's a numpy bytes object, sometimes it's not
    if isinstance(read_id, bytes): read_id = read_id.decode()

    return (
        pd.DataFrame(slot_contents, columns=slots_to_import)
        .assign(read_id=read_id)
        .set_index(index_0b)
        .rename_axis('pos_0b')
    )


def read_list_to_df(read_list, slots_to_import, corr_grp):
    '''
    Arguments:
        read_list:
            list of tombo_helper.readData objects
        slots_to_import:
            slots from the events table to fetch
            (valid values: norm_mean, norm_stdev, start, length, base)
        corr_grp:
            which corrected group of the fast5 file to fetch results from

    Returns:
        pandas dataframe:
            The index is a zero-based genomic position. There is one column for
            every slot in slots_to_import, plus a "read_id" column
    '''
    global pd
    import pandas as pd

    return pd.concat(
        read_to_df(read, slots_to_import, corr_grp)
        for read in read_list
    )


def run(args):
    '''This subroutine is called when the user selects the "events" module
    from the command line.'''

    global tombo_helper, pd, np
    from tombo import tombo_helper
    import numpy as np
    import pandas as pd

    cs_reads = (
        tombo_helper.TomboReads(args.fast5_dirs)
        .get_cs_reads(args.chrm, args.strand)
    )

    (
        read_list_to_df(cs_reads, SLOTS_TO_IMPORT, args.corr_grp)
        .to_csv(args.output_path)
    )
