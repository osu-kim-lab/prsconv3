'''
This module contains the code and interface to convert information from the
events tables of fast5s into CSV files.

Chris Kimmel
8-6-2021
chris.kimmel@live.com
'''


# pylint: disable=invalid-name,global-statement,import-outside-toplevel


DEFAULT_CHRM = 'truncated_hiv_rna_genome'

SLOTS_TO_IMPORT = [
    'norm_mean',
    'norm_stdev',
    'start',
    'length',
    'base',
]

DESCRIPTION = '''
Extract the events tables from all fast5s in a directory to a single CSV file.

This code can write the CSV in either of two formats. By default, it prints
information in "tidy" form (also known as "long" or "tall" format).
Alternatively, the user can use the "--wide" option to format the output as
"wide" data, with a row for every read and a column for every nucleotide
position.

The default "tidy" output includes, in addition to "read_id" and "pos_0b"
columns, all five columns of the events table:
    - norm_mean (event-mean current levels, as normalized during resquiggling)
    - norm_stdev (standard deviation of current levels; by default Tombo leaves
        this column of the events table blank to save time.)
    - start (index of the ammeter measurement associated during resquiggling to
        the start of this event)
    - length (number of ammeter measurements associated during resquiggling to
        this event)
    - base (basecalled base; sometimes omitted from events table)

Because of the limits of "wide-format" data, the user must specify which column
he/she wants when using the "--wide" option (e.g., "--wide=norm-mean" to get
the current levels).

Usage Examples:
from sys import stdin, stdout
python prsconv3 events --wide=length tests/files/fast5_dir dwell_times.csv
python prsconv3 events tests/files/fast5_dir events_tables.csv
'''


def register(subparsers):
    '''Add a subcommand to the subparsers object, thereby exposing the
    methods in this module via the command-line interface.'''

    parser = subparsers.add_parser('events',
        help='fast5 events tables from directories of fast5 files (this '
        'includes dwell times and current levels)', description=DESCRIPTION)

    parser.add_argument('--wide', metavar='COLNAME', choices=SLOTS_TO_IMPORT,
        help='If this option is specified, only COLNAME is included in the '
        'output, and the data is printed in a wide format (rather than the '
        'default long format).')

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

    results = read_list_to_df(cs_reads, SLOTS_TO_IMPORT, args.corr_grp)
    if args.wide:
        results = results.reset_index().pivot(
            index='read_id',
            columns='pos_0b',
            values=args.wide
        )
        results.to_csv(args.output_path, index=True)
    else:
        results.to_csv(args.output_path, index=False)
