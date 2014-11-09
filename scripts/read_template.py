#!/usr/bin/python

import codecs
import sys

def read_template(ifn):
	sf = codecs.open(ifn, 'r', 'utf-8')

	lat_templates = {}
	line = sf.readline()
	while line:
		if u'====' in line:
			lat_type = line.split()[1]
			lat_templates[lat_type] = []
			line = sf.readline()
			while len(line.strip()) != 0:
				lat_templates[lat_type].append(line.strip().split())
				line = sf.readline()
		line = sf.readline()
	
	for key in lat_templates.keys():
		print key
		for w in lat_templates[key]:
			print w
		print
	
	return lat_templates

if __name__ == '__main__':
	read_template('lat-data/lat-template.txt')

