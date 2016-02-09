#!/usr/bin/python

# Author: Sergi Vila Almenara

import sys
from automats import AFD, AFDReader, AFDWriter

if __name__ == '__main__':
	if len(sys.argv) is not 4:
		print 'Usage:', sys.argv[0], '<AFD file> <AFD file> <name output file>'
		sys.exit(-1)
	r1 = AFDReader(sys.argv[1])
	r2 = AFDReader(sys.argv[2])
	automat1 = r1.get_AFD()
	automat2 = r2.get_AFD()
	union = automat1.get_intersection(automat2)
	w = AFDWriter(union)
	w.write(sys.argv[3])