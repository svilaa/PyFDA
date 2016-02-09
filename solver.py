#!/usr/bin/python

# Author: Sergi Vila Almenara

import sys
from automats import AFD, Solver, AFDReader

if __name__ == '__main__':
	if len(sys.argv) is not 3:
		print 'Usage:', sys.argv[0], '<AFD file> <word | [void_word]>'
		sys.exit(-1)
	r = AFDReader(sys.argv[1])
	automat = r.get_AFD()
	s = Solver(automat)
	if sys.argv[2] == 'void_word':
		print s.solve('')
	else:
		print s.solve(sys.argv[2])