#!/usr/bin/python
#encoding=utf-8

import jieba
import jieba.posseg as pseg 
import jieba.analyse
import codecs
import sys

def seg_query(query):
	seg_list = pseg.cut(query)

	seg_res = []
	pos_res = []
	for item in seg_list:
		seg_res.append(item.word)
		if item.flag[0] == u'l':
			item.flag = u'n'
		pos_res.append(item.flag)
	return seg_res, pos_res

def get_keywords(query):
	#of.write('KEYWORDS: ')
	keywords = jieba.analyse.extract_tags(query,2)
	return keywords
	#for w in keywords:
	#	of.write(w + ' ')
	#of.write('\n\n')
	'''
	rindex = []
	for idx in range(len(seg_res)):
		if pos_res[idx][0] == 'r':
			rindex.append(idx)
	
	of.write('R: ')
	for i in range(len(rindex)):
		of.write(seg_res[rindex[i]] + ' ' )
	of.write('\n')

	of.write('NN: ')
	for i in range(len(rindex)):
		for j in range(rindex[i] + 1, len(seg_res)):
			if pos_res[j][0] == 'n':
				of.write(seg_res[rindex[i]] + ' ' + seg_res[j] + ' ')
				break
	of.write('\n')
	'''
