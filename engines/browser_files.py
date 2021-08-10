'''
This module contains the code and interface to access browser files.

Chris Kimmel
7-14-2021
chris.kimmel@live.com
'''

from warnings import warn
from argparse import RawTextHelpFormatter


DESCRIPTION = '''
Convert wiggle and bedgraph files to CSV files.

Please note that this tool does not work for all wiggle and bedgraph files. It
was only built to work on special cases.

Usage Examples:
python3 prsconv3 browser-files --wig -c "dampened_frac" d_frac.wig out.csv
python3 prsconv3 browser-files --bed -c "covg" coverage.bed out.csv
'''


def register(subparsers):
    '''Attach a subcommand to the given subparsers object, through which the
    user will access the functionality of this module.'''

    parser = subparsers.add_parser('browser-files', description=DESCRIPTION,
        help='wiggle and bedgraph files', formatter_class=RawTextHelpFormatter)

    grp = parser.add_mutually_exclusive_group(required=True)
    grp.add_argument('--wig', help='Use when the input is a wiggle file', action='store_true')
    grp.add_argument('--bed', help='Use when the input is a bedgraph file', action='store_true')

    parser.add_argument('-c', '--column-name', metavar='COLNAME',
        help='What to name the data column of the output CSV '\
        '(suggestions: "covg", "dampened_frac", etc.)',
        default='file_contents')

    parser.add_argument('input_filepath', metavar='INPUT-FILEPATH',
        help='The wiggle or bedgraph file to read.')

    parser.add_argument('output_filepath', metavar='OUTPUT-FILEPATH',
        help='Filepath to the output CSV, including the .csv extension.')


def write_bed_to_csv(inbuffer, outbuffer, column_name):
    '''Stream data from a BED format to a CSV format'''

    header = ','.join(['pos_0b', column_name])

    try:
        # consume bedgraph header
        for _ in range(1):
            _ = inbuffer.readline()
    except EOFError:
        pass
    finally:
        print(header, file=outbuffer)

        # print contents
        for line in inbuffer.readlines():
            chrom, chromStart, chromEnd, dataValue = line.split() # pylint: disable=invalid-name,unused-variable
            for pos_0b in map(str, range(int(chromStart), int(chromEnd))):
                outbuffer.write(','.join([pos_0b, dataValue]) + '\n')


def write_wig_to_csv(inbuffer, outbuffer, column_name):
    '''Stream data from a WIG format to a CSV format'''

    header = ','.join(['pos_0b', column_name])

    try:
        # consume wiggle header
        for _ in range(2):
            _ = inbuffer.readline()
    except EOFError:
        pass
    finally:
        print(header, file=outbuffer)

        # print contents
        for line in inbuffer.readlines(): # line includes trailing newline
            pos_ob, data = line.split()
            pos_0b = str(int(pos_ob) - 1)
            outbuffer.write(','.join([pos_0b, data]) + '\n')


def run(args):
    '''This subroutine is called when the user selects the "browser-files" module
    from the command line.'''

    MESS = "The browser-file tools in this package are built to work on " \
        "simple cases. This code is not suitable for all wiggle/bedgraph files."
    warn(MESS)

    with open(args.input_filepath, 'rt') as input_file:
        with open(args.output_filepath, 'wt') as output_file:
            if args.wig:
                write_wig_to_csv(input_file, output_file, args.column_name)
            elif args.bed:
                write_bed_to_csv(input_file, output_file, args.column_name)
