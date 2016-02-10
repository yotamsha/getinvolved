import argparse
import os

import sys

__author__ = 'avishayb'


def _validate_mode(mode):
    if not mode:
        raise argparse.ArgumentTypeError('mode can not be None or empty')
    modes = ['dev', 'prod', 'local']
    if mode not in modes:
        raise argparse.ArgumentTypeError('mode should be a value in %s', str[modes])
    return mode

if 'utrunner.py' not in sys.argv[0]:
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', dest='mode', required=True, type=_validate_mode,
                        help='The GI server mode (prod|dev)')
    args = parser.parse_args()
    mode = args.mode
    os.environ['__MODE'] = mode
