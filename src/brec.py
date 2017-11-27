#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Records Searchable Result Statistics for Instances.

This script records stats per isntance searchable way via md5 hashes.

"""
import sys
import argparse
import logging
import json

from benchmarktool.utils.logger import setup_logger
from benchmarktool.utils.record import Records

LOG = logging.getLogger('custom')

def main():
    """Main."""
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('result', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                            help="""XML-formatted result file produced by './bgen'; alternatively,
                            the result is read from stdin""")
    output_targets = arg_parser.add_mutually_exclusive_group()
    output_targets.add_argument('--hor', nargs='?', action='store', type=str, dest='horizon_enc',
                                const='default', default=None,
                                help="""For each instance file NAME.lp, store its horizon
                                as extra NAME.lp_hor file in same directory""")
    output_targets.add_argument('-s', '--store', type=argparse.FileType('wr'), default=sys.stdout,
                                help="File to write/read instance results stats in JSON format")
    arg_parser.add_argument('-r', '--runscript', type=str,
                            help="XML-formatted runscript file used to generate the benchmark set")
    arg_parser.add_argument('-v', '--verbose', action='store_const', dest='loglevel',
                            const=logging.INFO, default=logging.WARNING,
                            help='verbose output (default: %(default)s)')
    arg_parser.add_argument('-d', '--debug', action='store_const', dest='loglevel',
                            const=logging.DEBUG, default=logging.WARNING,
                            help='debug output (default: %(default)s)')

    args = arg_parser.parse_args()
    setup_logger(args.loglevel)

    Records(args.runscript, args.result, args.store, args.horizon_enc).store_stats()

if __name__ == '__main__':
    sys.exit(main())
