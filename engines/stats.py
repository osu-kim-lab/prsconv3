'''
This module contains the code and interface to convert .tombo.stats files to CSV
files

Chris Kimmel
7-14-2021
chris.kimmel@live.com
'''

# pylint: disable=invalid-name,global-statement,import-outside-toplevel


from argparse import RawTextHelpFormatter


DESCRIPTION = '''
Convert .tombo.stats files to CSV files

The output CSV file will have columns named "pos_0b", "chrm", "strand",
"damp_frac", and "frac". Additional columns may be present if other statistics
are stored in the statistics file.

Usage Examples:
python prsconv3 stats tests/files/stats/23456_WT_cellular.tombo.stats 23456_WT_cellular.csv
'''


def register(subparsers):
    '''Add a subcommand to the given subparsers object. The subcommand will
    expose the functionality of this module via the command-line.
    '''
    parser = subparsers.add_parser('stats', help='.tombo.stats files',
                        description=DESCRIPTION,
                        formatter_class=RawTextHelpFormatter)

    parser.add_argument('input_filepath', help='Path of the .tombo.stats '
                        + 'file', metavar='STATS-FILEPATH', type=str)

    parser.add_argument('output_filepath', help='Path of the CSV file to be '
                        + 'written (including the .csv extension)',
                        metavar='OUTPUT-FILEPATH', type=str)


def stats_to_df(stats_path):
    '''Open a Tombo statistics file and return it as a pandas DataFrame'''

    global TomboStats, pd
    from tombo.tombo_stats import TomboStats
    import pandas as pd

    ts = TomboStats(stats_path)
    assert ts.is_model_stats, "This appears not to be a ModelStats object. "\
        "It's probably a LevelStats object instead. This module was only tested "\
        "on Tombo statistics files produced by tombo "\
        "model_sample_compare."
    to_concat = []
    for chrm, strand, start, end, block_stats in ts: # pylint: disable=unused-variable

        # Correct for the fact that Tombo stores damp_frac and frac upside
        # down in ModelStats:
        for col in ['damp_frac', 'frac']:
            block_stats[col] = 1 - block_stats[col]
        # I believe every .tombo.stats file contains damp_frac and frac columns
        # due to the weirdness of Tombo's internals, so there's no risk of an
        # IndexError.

        to_concat.append(
            pd.DataFrame(block_stats).assign(chrm=chrm, strand=strand)
        )

    return pd.concat(to_concat).rename({'pos': 'pos_0b'}, axis=1)


def run(args):
    '''This subroutine is called when the user selects the "stats" module
    from the command line.'''

    MESS = '''Support for .tombo.stats files is still experimental.

    This module was designed to work with Tombo ModelStats objects.  I have not
    tested it on Tombo LevelStats objects.'''

    df = stats_to_df(args.input_filepath)
    df.to_csv(args.output_filepath, index=False)
