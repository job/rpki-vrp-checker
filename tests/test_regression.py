#!/usr/bin/env python

from vrp_checker import checker

from mock import patch
import io
import sys
import unittest


def stub_stdin(testcase_inst, inputs):
    stdin = sys.stdin

    def cleanup():
        sys.stdin = stdin

    testcase_inst.addCleanup(cleanup)
    sys.stdin = StringIO(inputs)


def stub_stdouts(testcase_inst):
    stderr = sys.stderr
    stdout = sys.stdout

    def cleanup():
        sys.stderr = stderr
        sys.stdout = stdout

    testcase_inst.addCleanup(cleanup)
    sys.stderr = StringIO()
    sys.stdout = StringIO()


class TestAggregate(unittest.TestCase):

    def test_00__roa_missing(self):
        pass

    def test_15_verbose(self):
        stub_stdin(self, '10.0.0.0/24 10.0.1.0/24 172.16.0.0/24 10.0.0.0/32\n')
        stub_stdouts(self)
        with patch.object(sys, 'argv', ["prog.py", "-v"]):
            agg_main()
        self.assertEqual(sys.stdout.getvalue(), "+ 10.0.0.0/23\n- 10.0.0.0/24\n- 10.0.0.0/32\n- 10.0.1.0/24\n  172.16.0.0/24\n")


class StringIO(io.StringIO):
    """
    A "safely" wrapped version
    """

    def __init__(self, value=''):
        value = value.encode('utf8', 'backslashreplace').decode('utf8')
        io.StringIO.__init__(self, value)

    def write(self, msg):
        io.StringIO.write(self, msg.encode(
            'utf8', 'backslashreplace').decode('utf8'))


def main():
    unittest.main()

if __name__ == '__main__':
    main()
