'''
This module contains the code and interface to access browser files.

Chris Kimmel
7-14-2021
chris.kimmel@live.com
'''

from warnings import warn
from sys import stdin, stdout


def register(subparsers):
    '''Attach a subcommand to the given subparsers object, through which the
    user will access the functionality of this module.'''

    parser = subparsers.add_parser('browser_files',
        help='.wig and .bed files (streams from stdin to stdout)')
    
    parser.add_argument('wig_or_bed', metavar='WIG_OR_BED',
        choices=['wig', 'bed'], help='Which type of file to expect '\
        '("wig" for wiggle or "bed" for bedgraph)')

    parser.add_argument('column_name', metavar='COLNAME',
        help='What to name the data column of the output CSV '\
        '(suggestions: "covg", "dampened_frac", etc.)')


def write_bed_to_csv(inbuffer, outbuffer, column_name):
    '''Stream data from a BED format to a CSV format'''
    header = ','.join(['pos_zb', column_name])

    # consume bedgraph header; print our own header
    try:
        for _ in range(1):
            _ = input()
    except EOFError:
        print(header)
        return
    print(header)

    # print contents
    for line in inbuffer.readlines():
        chrom, chromStart, chromEnd, dataValue = line.split()
        for pos_zb in map(str, range(int(chromStart), int(chromEnd))):
            outbuffer.write(','.join([pos_zb, dataValue]) + '\n')


def write_wig_to_csv(inbuffer, outbuffer, column_name):
    '''Stream data from a WIG format to a CSV format'''
    header = ','.join(['pos_zb', column_name])

    # consume wiggle header; print our own header
    try:
        for _ in range(2):
            _ = input()
    except EOFError:
        print(header)
        return
    print(header)

    # print contents
    for line in inbuffer.readlines(): # line includes trailing newline
        pos_ob, data = line.split()
        pos_zb = str(int(pos_ob) - 1)
        outbuffer.write(','.join([pos_zb, data]) + '\n')


def run(args):
    MESS = "The browser-file tools in this package are hacked together to "\
           "work on simple cases. This code is not suitable for all "\
           "wiggle/bedgraph files."
    warn(MESS)
    if args.wig_or_bed == 'wig':
        write_wig_to_csv(stdin, stdout, args.column_name)
    elif args.wig_or_bed == 'bed':
        write_bed_to_csv(stdin, stdout, args.column_name)
    else:
        raise NotImplementedError(
            f'Unrecognized wig_or_bed option {args.wig_or_bed}')
