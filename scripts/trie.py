#!/usr/bin/python
#coding=utf-8

import codecs
import sys


class Trie(object):
	def __init__(self):
		self.val = None			# record transfer word
		self.extract = False	# if it's a lat
		self.child = {}			# map child via keys
		self.default = None     # if it needs default value for lat, i.e. '哪一年'
		self.ltype = None		# need to record what answer type it is
		self.end = False		# if a pattern is found

def build_lat_trie(lat_templates):
	root = Trie()
	for key in lat_templates.keys():
		for template in lat_templates[key]:
			insert_trie(root, template, key)
	return root

def insert_trie(root, template, ltype):
	cur = root
	for item in template:
		val = item.split(u':')[0]
		extract = item.split(u':')[1]
		if extract == '1':
			extract = True
		else:
			extract = False
		default = None
		if len(item.split(u':')) > 2:
			default = item.split(':')[2]
		if val in cur.child.keys():
			cur = cur.child[val]
			cur.extract = extract
			cur.default = default
			cur.ltype = ltype
		else:
			cur.child[val] = Trie()
			cur.child[val].val = val
			cur = cur.child[val]
			cur.extract = extract
			cur.default = default
			cur.ltype = ltype
	cur.end = True

def print_trie(root):
	for w in root.child.keys():
		print w.encode('utf-8'),
		print_trie(root.child[w])
	print 

def find_trie(root, start, seg_res, pos_res):
	cur = root
	ret = []
	isfound = False
	for idx in range(start, len(seg_res)):
		#print seg_res[idx]
		if seg_res[idx] in cur.child.keys():
			#print '1'
			#for w in cur.child.keys():
			#	print w.encode('utf-8'),
			#print 
			cur = cur.child[seg_res[idx]]
			if cur.extract == True:
				ret.append(seg_res[idx])
			if cur.default != None:
				ret.append(cur.default)
			if cur.end == True:
				isfound = True
			if not cur.child:
				#print ret
				if ret:
					return [cur.ltype, ret]
				else:
					return ret
		elif pos_res[idx][0] in cur.child.keys():
			#print '2'
			#for w in cur.child.keys():
			#	print w.encode('utf-8'),
			#print 
			cur = cur.child[pos_res[idx][0]]
			if cur.extract == True:
				ret.append(seg_res[idx])
			if cur.default != None:
				ret.append(cur.default)
			if cur.end == True:
				isfound = True
			if not cur.child:
				#print ret
				if ret:
					return [cur.ltype, ret]
				else:
					return ret
		elif u'*' in cur.child.keys():
			cur = cur.child[u'*']
			if cur.extract == True:
				ret.append(seg_res[idx])
			if cur.default != None:
				ret.append(cur.default)
			if cur.end == True:
				isfound = True
			if not cur.child:
				#print ret
				if ret:
					return [cur.ltype, ret]
				else:
					return ret
		elif u'-1' in cur.child.keys():
			ret.append(seg_res[-2])
			#print ret
			return [cur.ltype, ret]
		elif u'**' in cur.child.keys():
			cur = cur.child[u'**']
		elif cur.val != u'**':
			#print ret
			if isfound:
				return [cur.ltype, ret]
			return []
	return []
