#!/usr/bin/python

import codecs
import sys

def clean(ifn, ofn):
	sf = codecs.open(ifn, 'r', 'utf-8')
	of = codecs.open(ofn, 'w', 'utf-8')

	line = sf.readline()
	while line:
		line = clean_line(line)
		of.write(line)
		line = sf.readline()

def clean_line(line):


if __name__ == '__main__':
	if len(sys.argv) ==  1:
		clean('../data/raw-data/zhwiki-20141009-pages-articles-multistream.xml.bz2',\
				'../data/raw-data/clean')
	else:
		clean(sys.argv[1], sys.argv[2])

