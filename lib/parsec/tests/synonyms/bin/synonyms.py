#!/usr/bin/env python

from __future__ import print_function
import os
import sys

fpath = os.path.dirname(os.path.abspath(__file__))

# spec
sys.path.append(fpath + '/../lib/python')
# parsec
sys.path.append(fpath + '/../../..')

from cfgspec import SPEC
from config import config

rcname = sys.argv[1]
rcfile = rcname + '.rc'

cfg = config(SPEC)

cfg.loadcfg(rcfile)

res = cfg.get(sparse=True)

for expected in res[rcname].keys():

    vals = cfg.get([rcname, expected], sparse=True).values()
    expected = expected.replace('COMMA', ',').replace('NULL', '')

    if rcname == 'boolean':
        expected = (expected == 'True') or False

    elif rcname == 'integer':
        expected = int(expected)

    elif rcname == 'float':
        expected = float(expected)

    elif rcname == 'integer_list':
        expected = [int(i) for i in expected.split('_')]

    elif rcname == 'float_list':
        expected = [float(i) for i in expected.split('_')]

    elif rcname == 'string_list':
        if expected:
            expected = expected.split('_')
        else:
            expected = []

    if vals.count(expected) != len(vals):
        print(vals, ' is not all ', expected, file=sys.stderr)
        sys.exit("FAIL")
    else:
        print("OK")
