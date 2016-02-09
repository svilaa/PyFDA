#!/usr/bin/python

# Author: Sergi Vila Almenara

import sys
from automats import AFD, AFDReader, AFDWriter

if __name__ == '__main__':
	if len(sys.argv) is not 3:
		print 'Usage:', sys.argv[0], '<AFD file> <name output file>'
		sys.exit(-1)
	r = AFDReader(sys.argv[1])
	automat = r.get_AFD()
	automat.minimize()
	w = AFDWriter(automat)
	w.write(sys.argv[2])