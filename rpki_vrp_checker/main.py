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

import json
import radix
import sys
import yaml

from rpki_vrp_checker import __version__


def parse_args(args):
    import argparse

    parser = argparse.ArgumentParser(
        description="Perform various business logic test operations on a "
                    "given collection of RPKI based VRPs.")
    parser.add_argument("-v", dest="verbose", action="store_true",
                        default=False,
                        help="Be verbose")
    parser.add_argument("-i", dest="inputpath", required=True,
                        help="Input JSON file containing to-be-checked VRPs")
    parser.add_argument("-b", dest="blessedpath", required=True,
                        help="Path to output the blessed JSON file checked VRPs")
# parser.add_argument("-s", dest="slurmpath",
#                       help="Path to SLURM JSON file")
    parser.add_argument("-c", dest="canariespath", required=True,
                        help="Path to YAML file with expected ROA canaries")
    parser.add_argument("-V", dest="version", action="store_true",
                         help="Display rpki-vrp-checker version")

    return parser.parse_args(args)


def pretty_print(pack, num=False):
    if num:
        print("Entry #%s:" % num)
    print("  Prefix       : %s (MaxLength: %s)" % (pack['p'], pack['ml']))
    print("  Origin AS    : %s" % pack['asn'])
    print("  Trust Anchor : %s" % pack['ta'].upper())
    print()

def main():

    args = parse_args(sys.argv[1:])

    if args.version: # pragma: no cover
        print("rpki-vrp-checker %s" % __version__)
        sys.exit()

    verbose = args.verbose

    f = open(args.inputpath)
    roas = json.load(f)
    f.close()

    f = open(args.canariespath)
    canaries = yaml.safe_load(f)
    f.close()

    vrp_count = 0

    tree = radix.Radix()

    for r in roas['roas']:
        asn = int(r['asn'][2:])
        ta = r['ta']
        ml = r['maxLength']
        prefix = r['prefix']
        rnode = tree.search_exact(prefix)
        pack = {'p': prefix, 'ta': ta, 'ml': ml, 'asn': asn}

        if not rnode:
            rnode = tree.add(prefix)
            rnode.data['vrps'] = [pack]
        else:
            if pack not in rnode.data['vrps']:
                rnode.data['vrps'].append(pack)
        vrp_count += 1

    if verbose:
        print("loaded %s prefixes (%s vrps)" % (len(tree.prefixes()), vrp_count))

    roas_of_interest = []
    canaries_of_interest = []

    for c in canaries:
        prefix = c['prefix']
        pack = {'p': prefix, 'ta': c['ta'], 'ml': c['maxlength'],
                'asn': c['origin']}
        canaries_of_interest.append(pack)
        rnode = tree.search_worst(prefix)
        if rnode:
            for r in tree.search_covered(rnode.prefix):
                for vrp in r.data['vrps']:
                    if vrp not in roas_of_interest:
                        roas_of_interest.append(vrp)

    if verbose:
        print("loaded %s canaries" % len(canaries))

    print("The following RPKI VRPs have been registered at the RIR level, "
          "that were not added as canaries:\n")
    c = 0
    for vrp in roas_of_interest:
        if vrp not in canaries_of_interest:
            c += 1
            pretty_print(vrp, c)

    print("\n---------------\n\n")

    c = 0
    print("The following canaries are not visible in "
          "RPKI data at the RIR level:\n")
    for canarie in canaries_of_interest:
        if canarie not in roas_of_interest:
            c += 1
            pretty_print(canarie, c)

    # each canary must *exactly* be present in the VRP tree
    # no less-specific VRPs must exist for any not-exactly registered canaries
    # no more-specific VRPs must exist for any not-exactly registered canaries

if __name__ == '__main__':
    sys.exit(main())
