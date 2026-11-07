#!/usr/bin/env python3

from optparse import OptionParser

def testFunction(filename="superhot", verbose=False, num=42):
    print(filename)
    print(verbose)
    print(num)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename", help="write report to FILE", metavar="FILE")
    parser.add_option("-q", "--quiet", action="store_false", dest="verbose", default=True, help="don't print status messages to stdout")
    parser.add_option("-n", type="int", dest="num")

    (options, args) = parser.parse_args()

    print(str(options))
    testFunction(options.filename, options.verbose, options.num)
