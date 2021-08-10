'''
This module contains the code and interface for a tool that converts
.tombo.per_read_stats files to CSV files
'''

# pylint: disable=invalid-name,redefined-outer-name


import os.path
import cli # Module from this directory that defines an argparse parser


DESCRIPTION = '''
This command converts .tombo.per_read_stats files into CSV files.

As with some other commands in this package, the user must specify either
"--wide" or "--long" when running the command. The former results in CSV files
with one row per read and one column per genomic position, while the latter
results in a CSV file with columns "read_id", "pos_0b", and "stat"

Because of the way Tombo's Python interface works, the user must also specify a
chromosome, strand, and region of the genome for which he/she wants statistics.
The defaults (bases zero through one billion on the "+" strand of the
"truncated_hiv_rna_genome") are correct for the analysis our team was doing at
the time this tool was written.

Usage Examples:
python prsconv3 per-read-stats --wide tests/files/23456_WT_cellular.tombo.per_read_stats output.csv
python prsconv3 per-read-stats --long tests/file/23456_WT_cellular.tombo.per_read_stats output.csv
'''


def register(subparsers):
    '''
    Register a subparser with the provided subparsers object
    '''
    parser = subparsers.add_parser('per-read-stats', description=DESCRIPTION,
                        help='.tombo.per_read_stats files')

    parser.add_argument('input-filepath', help='Path of the .tombo.per_read_stats '
                        + 'file to read', metavar='PRS-FILEPATH', type=str)

    parser.add_argument('output-filepath', help='Path of the CSV file to be '
                        + 'written (including the .csv extension)',
                        metavar='OUTPUT-FILEPATH', type=str)

    grp = parser.add_mutually_exclusive_group(require=True)
    grp.add_argument('--wide', help='output wide-format data, with a row for '
                        'each read and a column for each nucleotide position')
    grp.add_argument('--long', help='output long-format data, with columns '
                        '"read_id", "pos_0b", and "stat"')

    parser.add_argument('--chromosome', help='Name of the chromosome for '
                        + 'which to give statistics (DEFAULT: '
                        + '"truncated_hiv_rna_genome")', metavar='CHROMOSOME',
                        default='truncated_hiv_rna_genome', type=str)

    parser.add_argument('--strand', help='Either "+" or "-" (DEFAULT: "+")',
                        metavar='STRAND', default='+', type=str)

    parser.add_argument('--start', help='Beginning of the genomic region for '
                        'which you want statistics (DEFAULT: 0)',
                        metavar='START', default=0, type=int)

    parser.add_argument('--end', help='End of the genomic region for which you '
                        + 'want statistics (DEFAULT: 1,000,000,000)',
                        metavar='END', default=10**9, type=int)


def recarray_to_df(recarray):
    '''Convert record array output from tombo.tombo_stats.PerReadStatistics
    into a one-column pandas dataframe with a two-level index ['read_id',
    'pos'] named "stat"'''
    return (
        pd.DataFrame(recarray)
        .set_index(['read_id', 'pos'])
        .rename({'pos': 'pos_zb'}, axis=1)
        .rename_axis('stat', axis=1)
    )


def df_to_csv(series, output_path, wide_or_long):
    '''Print dataframe output from recarray_to_series to a CSV file at output_path.

    If wide_to_long == 'wide', the output CSV will have a row for every read and
    a column for every position. Otherwise, if wide_to_long == 'long', the
    output will be a three-column CSV file.
    '''
    if wide_or_long == 'wide':
        # The three operations below that involve 'stat_level' are just to delete
        # extraneous labelling information from the table before we export to CSV
        (
            series
            .rename_axis('stat_level', axis=1)
            .unstack('pos')
            .stack('stat_level')
            .reset_index('stat_level', drop=True)
            .to_csv(output_path)
        )
    elif wide_or_long == 'long':
        series.to_csv(output_path)
    else:
        raise NotImplementedError(
            f'"{wide_or_long}" not valid. Supported options: "wide" and "long"')


def run(args):
    global pd
    import pandas as pd
    from tombo import tombo_helper, tombo_stats

    wide_or_long = 'wide' if args.wide else 'long'

    reg = tombo_helper.intervalData(
        chrm=args.chromosome,
        start=args.start,
        end=args.end,
        strand=args.strand,
    )
    prs_recarray = (
        tombo_stats.PerReadStats(args.input_filepath)
        .get_region_per_read_stats(reg)
    )
    df = recarray_to_df(prs_recarray)
    df_to_csv(df, wide_or_long=wide_or_long, output_path=args.output_filepath)
