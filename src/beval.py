'''
Created on Jan 13, 2010

@author: Roland Kaminski
'''

from benchmarktool.runscript.parser import Parser
import benchmarktool.tools as tools
import argparse
import sys
import logging

from benchmarktool.utils.logger import setup_logger

if __name__ == '__main__':
    usage  = "usage: %prog [options] <runscript>"
    parser = argparse.ArgumentParser(usage)
    parser.add_argument('runscript_file',type=str,
                        help="XML-formatted runscript file; alternatively, read from stdin")
    parser.add_argument('-d', '--debug', action='store_const', dest='loglevel',
                        const=logging.DEBUG, default=logging.WARNING,
                        help='debug output (default: %(default)s)')

    args = parser.parse_args()

    setup_logger(args.loglevel)
    
    # if len(argsfiles) == 1:
    #     fileName = files[0]
    # else:
    #     parser.error("Exactly on file has to be given")
    
    p = Parser()
    run = p.parse(args.runscript_file)
    run.evalResults(sys.stdout)
