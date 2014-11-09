#!/usr/bin/python
#encoding=utf-8

import codecs
import sys

from trie import *
from seg_query import *
from read_template import *

def process(ifn, tfn, ofn):
	sf = codecs.open(ifn, 'r', 'utf-8')
	root = build_extractor(tfn)
	print_trie(root)
	of = codecs.open(ofn, 'w', 'utf-8')

	line = sf.readline()
	query = extract_query(line)
	while line:
		print query
	#for i in range(1):
		seg_res, pos_res = seg_query(query)
		keywords = get_keywords(query)
		lats = extract_lat(root, seg_res, pos_res)
		
		of.write('SEGMENT: ')
		for idx in range(len(seg_res)):
			of.write(seg_res[idx] + '/' + pos_res[idx] + ' ')
		of.write('\n')
		of.write('KEYWORDS: ')
		for w in keywords:
			of.write(w + ' ')
		of.write('\n')
		of.write('LAT: ')
		for i in lats:
			of.write(i[0] + ' [')
			for k in i[1]:
				of.write(k + ',')
			of.write(']')
		of.write('\n\n')
		
		line = sf.readline()
		query = extract_query(line)
	
def extract_query(line):
	return '^' + line.split(u'？')[0] + '$'

def build_extractor(ifn):
	lat_templates = read_template(ifn)
	return build_lat_trie(lat_templates)

def extract_lat(root, seg_res, pos_res):
	ret = []
	for i in range(len(seg_res)):
		tmp_res = find_trie(root, i, seg_res, pos_res)
		if tmp_res:
			ret.append(tmp_res)
	
	for i in ret:
		for j in i:
			print j,
		print 
	return ret


if __name__ == '__main__':
	process('../data/raw-data/query-example', 'lat-data/lat-template.txt','out')
