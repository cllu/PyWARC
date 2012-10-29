#!/usr/bin/env python

import os
from pywarc import WARCFile, WARCRecord

def main():
    fullpaths = []
    for part in range(1, 10):
        path = os.path.join('clueweb09', 'ClueWeb09_English_%d' % part)
        folders = os.listdir(path)
        for folder in folders:
            folderpath = os.path.join(path, folder)
            files = os.listdir(folderpath)
            for f in files:
                fullpath = os.path.join(folderpath, f)
                fullpaths.append(fullpath)

    print "total files:", len(fullpaths)
    total = len(fullpaths)

    f = open('mapping.csv', 'w')
    for idx,fullpath in enumerate(fullpaths):
        print "process file #%d (total %d)" % (idx, total)
        for record in WARCFile(fullpath):
            f.write("%s,%s\n" % (record.trec_id, record.target_uri))

    f.close()
    
if __name__ == '__main__':
    main()
