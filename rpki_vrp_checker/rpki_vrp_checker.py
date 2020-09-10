#!/usr/bin/env python
# Copyright (C) 2020 Job Snijders <job@ntt.net>
#
# This file is part of rpki-vrp-checker
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF  THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import sys


def parse_args(args):
    import argparse
    parser = argparse.ArgumentParser(
        description="Perform various test operations on a given set of RPKI\
based VRPs")
    parser.add_argument("-v", dest="verbose", action="store_true",
                        help="Display verbose information about tests")
    parser.add_argument("-i", dest="inputpath",
                        help="Input JSON file containing to-be-checked VRPs")
    parser.add_argument("-b", dest="blessedpath",
                        help="Path to output the blessed JSON file checked VRPs")
    parser.add_argument("-s", dest="slurmpath",
                        help="Path to SLURM JSON file")
    parser.add_argument("-c", dest="assertpath",
                        help="Path to JSON file with expected ROA assertions")
    parser.add_arguments("-V", dest="version", action="store_true",
                         help="Display rpki-vrp-checker version")

    return parser.parse_args(args)


def main():

    args = parse_args(sys.argv[1:])
    if args.version: # pragma: no cover
        print("rpki-vrp-checker %s" % rpki_vrp_checker.__version__)
        sys.exit()
