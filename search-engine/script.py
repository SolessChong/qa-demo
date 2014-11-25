import xml.etree.ElementTree as etree
import jieba
import collections
import jieba.posseg as pseg
import jieba.analyse
import numpy

xml = 'data/wiki-zh/wiki-mini.xml'
cnt = 10

def process_text(text, D, inv):
	d = get_text_freq_dict(text)
	D.append(d)
	for w in d.keys():
		inv[w].append(len(D)-1)


def get_text_freq_dict(text):
	cm = collections.defaultdict(int)
	words = list(jieba.cut(text, cut_all=False))
	pos = ['ns', 'n', 'vn', 'v']
	pos_filt = frozenset(pos)
	for i in xrange(len(words)):
		cm[words[i]] += 1
	return cm

def idf(q, D, inv, N):
	return numpy.log((N-len(inv[q])+0.5)/(len(inv[q])+0.5))

def score(Q, D, inv, N, avgdl):
	k = 1.5
	b = 0.75
	def _score(q, D):
		return idf(q, D, inv, N)*(D[q]*(k+1))/(D[q]+k*(1-b+b*len(D.keys())/avgdl))

	rst = 0
	for q in Q:
		rst += _score(q, D)
	return rst

if __name__ == "__main__":
	"""
	for event, elem in etree.iterparse(xml, events=('end', 'start-ns')):
		if event == 'end':
			print elem.find('{http://www.mediawiki.org/xml/export-0.9/}subversion')
	"""

	dicts = []
	inv = collections.defaultdict(list)
	ind = 0
	for event, elem in etree.iterparse(xml, events=('end', 'start-ns')):
		if event == 'end':
			if elem.tag[-4:] == 'page':
				for child in elem:
					if child.tag[-4:] == 'sion':
						for child2 in child:
							if child2.tag[-4:] == 'text':
								process_text(child2.text, dicts, inv)
								ind += 1
		if ind == 10:
			break

	avgdl = 0
	for dict in dicts:
		avgdl += float(len(dict.keys())) / len(dicts)

	fin = open('data/wiki-zh/wiki-mini.xml', 'r')
	source = fin.read()

	corpus_dict = get_text_freq_dict(source)

	Q = [u'\u9ad8\u7dad']
	N = 10
	for dict in dicts:
		print dict[Q[0]]
		print score(Q, dict, inv, N, avgdl)