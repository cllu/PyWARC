#!/usr/bin/env python

import sys
import gzip

class WARCRecord:
    def __init__(self):
        # maybe warcinfo/response/request etc
        self.type = ''
        self.content_length = -1
        self.date = ''
        self.content = ''
        
        # used in ClueWeb09
        self.trec_id = ''
        self.target_url = ''

class WARCFile:
    def __init__(self, filename, skip_content=False):
        if filename.endswith('gz'):
            self.f = gzip.open(filename, 'rb')
        else:
            self.f = open(filename, 'r')
        
        self.skip_content = skip_content
        self.HEADER = 'WARC/0.18'
        # skip the first record
        self.read_record()
        print "already skip the first record"
        self.next_record = self.read_record()

    def __iter__(self):
        return self

    def next(self):
        if not self.next_record:
            raise StopIteration
        else:
            record = self.next_record
            self.next_record = self.read_record()
            return record

    def close(self):
        self.f.close()

    def read_record(self):
                    
        # skip the leading empty line if any.
        first_line = ''
        while not first_line:
            first_line = self.f.readline()
            if not first_line:
                # end of file
                break
            first_line = first_line.strip()
            
        # check if the record is valid
        if first_line != self.HEADER:
            print "NOT A LEGAL WARC Record"
            print first_line
            return False

        record = WARCRecord

        # read the header.
        line = self.f.readline().strip()
        while line:
            colon_pos = line.find(':')
            if colon_pos == -1:
                print "line does not have named field format."
                print line
                break
            key = line[:colon_pos].strip()
            value = line[colon_pos+1:].strip()
            
            if key == "WARC-Target-URL":
                record.target_url = value
            elif key == "WARC-TREC-ID":
                record.trec_id = value
            elif key == "Content-Length":
                record.content_length = int(value)

            # read in next line and see if we are at the end of block
            line = self.f.readline().strip()

        if record.content_length == -1:
            return False

        if self.skip_content:
            # do not read in the content
            self.f.seek(record.content_length, 1)
        else:
            record.content = self.f.read(record.content_length)
        
        return record


def main():
    if len(sys.argv) < 2:
        print "pywarc <warc-file>"
        sys.exit()
    
    filename = sys.argv[1]
    
    warcfile = WARCFile(filename)
    
    for record in warcfile:
        print "find one record", record

    warcfile.close()

if __name__ == "__main__":
    main()
