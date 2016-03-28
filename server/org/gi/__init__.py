import argparse
import os

import sys

__author__ = 'avishayb'
global args


def _validate_mode(mode):
    if not mode:
        raise argparse.ArgumentTypeError('mode can not be None or empty')
    modes = ['dev', 'prod', 'local']
    if mode not in modes:
        raise argparse.ArgumentTypeError('mode should be a value in %s', str[modes])
    return mode

if 'utrunner.py' not in sys.argv[0] and 'run_all.py' not in sys.argv[0]:
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', dest='mode', default='dev', type=_validate_mode,
                        help='The GI server mode (prod|dev)')
    parser.add_argument('-c', '--clear', action="store_true")
    args = parser.parse_args()
    os.environ['__MODE'] = args.mode
else:
    os.environ['__MODE'] = 'dev'
