'''
This module contains the code and interface to convert .tombo.stats files to CSV
files

Chris Kimmel
7-14-2021
chris.kimmel@live.com
'''

from warnings import warn


def register(subparsers):
    '''Add a subcommand to the given subparsers object. The subcommand will
    expose the functionality of this module via the command-line.
    '''
    parser = subparsers.add_parser('stats', description='.tombo.stats files')

    parser.add_argument('stats_path', help='Path of the .tombo.stats '
                        + 'file', metavar='STATS-FILEPATH', type=str)

    parser.add_argument('output_path', help='Path of the CSV file to be '
                        + 'written (including the .csv extension)',
                        metavar='OUTPUT-FILEPATH', type=str)


def stats_to_df(stats_path):
    '''Open a Tombo statistics file and return it as a pandas DataFrame'''
    ts = TomboStats(stats_path)
    assert ts.is_model_stats, "This appears not to be a ModelStats object. "\
        "It's probably a LevelStats object instead. This module is only built "\
        "to support Tombo statistics files produced by tombo "\
        "model_sample_compare."
    to_concat = []
    for chrm, strand, start, end, block_stats in ts:

        # Correct for the fact that Tombo stores damp_frac and frac upside
        # down in ModelStats:
        for col in ['damp_frac', 'frac']:
            block_stats[col] = 1 - block_stats[col]

        to_concat.append(
            pd.DataFrame(block_stats).assign(chrm=chrm, strand=strand)
        )

    return pd.concat(to_concat)


def run(args):
    global TomboStats
    from tombo.tombo_stats import TomboStats
    global pd
    import pandas as pd

    MESS = '''Support for .tombo.stats files is still experimental.

    This module was designed to work with Tombo ModelStats objects.  I have not
    tested it on Tombo LevelStats objects.'''

    df = stats_to_df(args.stats_path)
    df.to_csv(args.output_path, index=False)
