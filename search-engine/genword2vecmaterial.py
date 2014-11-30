# coding:utf-8
import xml.sax
import sys
import time
import chardet
sys.path.insert(0, 'scripts')
from langconv import *
import jieba
import jieba.posseg as pseg

reload(sys)
sys.setdefaultencoding('utf-8')

class GenWord2VecMaterial(xml.sax.ContentHandler):
    def __init__(self, of):
        self.CurrentData = ""
        self.title = ""
        self.text = ""
        self.counter = 0
        self.file = open(of, 'w')
        jieba.enable_parallel(20)

    def __del__(self):
        self.file.close()

    def startDocument(self):
        pass

    def endDocument(self):
        pass

    def startElement(self, tag, attributes):
        self.CurrentData = tag

    def endElement(self, tag):
        if self.CurrentData == "text":
            if self.title.startswith('Wikipedia:'):
                print "Skip", self.title
                self.title = ""
                return
            print self.title
            print len(self.text)
            time0 = time.time()

            line = Converter('zh-hans').convert(self.text.decode('utf-8'))
            self.text = line.encode('utf-8')

            #words = pseg.cut(self.text)
            time_set=time.time()
            words = jieba.cut_for_search(self.text)
            sentenceStart = True
            for w in words:
                self.file.write(w + ' ')

            print time.time() - time0

            self.counter += 1
            self.title = ""

            print "Counter", self.counter

        self.CurrentData = ""
        self.text = ""
        


    def characters(self, content):
        if self.CurrentData == "title":
            self.title = self.title + content
        elif self.CurrentData == "text":
            self.text = self.text + content


if __name__ == "__main__":
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    filename = 'data/wiki-zh/wiki.xml'
    print "Processing", filename

    Handler = GenWord2VecMaterial('data/word2vec/words.txt')

    parser.setContentHandler(Handler)


    parser.parse(filename)



