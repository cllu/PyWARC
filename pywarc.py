#!/usr/bin/env python

import sys
import gzip

def main():
    if len(sys.argv) < 2:
        print "pywarc <warc-file>"
        sys.exit()
    
    filename = sys.argv[1]
    if filename.endswith('gz'):
        f = gzip.open(filename, 'rb')
    else:
        f = open(filename, 'r')

    print f.readline()

    f.close()

if __name__ == "__main__":
    main()
