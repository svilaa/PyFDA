#!/usr/bin/python

# Author: Sergi Vila Almenara

import sys
from automats import AFD, AFDReader

if __name__ == '__main__':
	if len(sys.argv) is not 2:
		print 'Usage:', sys.argv[0], '<AFD file>'
		sys.exit(-1)
	r = AFDReader(sys.argv[1])
	automat = r.get_AFD()
	automat.show()