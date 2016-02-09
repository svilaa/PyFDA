#!/usr/bin/python

# Author: Sergi Vila Almenara

import argparse

def write(file_name, symbol_list, state_list):
	f = open(file_name, 'w')
	print >>f, 'p afd'
	print >>f, 's', ' '.join([x for x in symbol_list])
	print >>f, 'e', ' '.join([x for x in state_list])
	print >>f, 'i #'
	print >>f, 'f #'
	for state in state_list:
		for symbol in symbol_list:
			print >>f, 't', state, symbol, '#'
	f.close()

def parse_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--symbols', nargs='+', required=True, help='The alphabet accepted by the AFD')
	parser.add_argument('-e', '--states', nargs='+', required=True, help='The states of the AFD')
	parser.add_argument('-f', '--file', required=True, help='The name of the file that will be stored the AFD template')
	args = parser.parse_args()
	return args

if __name__ == "__main__":
	args = parse_arguments()
	write(args.file, args.symbols, args.states)