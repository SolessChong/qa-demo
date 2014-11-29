# coding:utf-8
import xml.sax
import sys
import chardet
from langconv import *
import jieba.posseg as pseg

reload(sys)
sys.setdefaultencoding('utf-8')


class MovieHandler(xml.sax.ContentHandler):
    def __init__(self, of):
        self.CurrentData = ""
        self.title = ""
        self.text = ""
        self.counter = 0
        self.file = open(of, 'w')

    def __del__(self):
        self.file.close()

    def startDocument(self):
        self.file.write('<wiki>\n')

    def endDocument(self):
        self.file.write('</wiki>')

    def startElement(self, tag, attributes):
        self.CurrentData = tag

    def endElement(self, tag):
        if self.CurrentData == "text":
            #f = open("E:\\pages\\" + str(self.counter) + ".txt", 'w')
            self.file.write('<page>\n')
			
			line = Converter('zh-hans').convert(self.title.decode('utf-8'))
            self.title = line.encode('utf-8')
            self.file.write('<title>' + self.title + '</title>' + "\n")

            self.file.write('<text>\n')
            line = Converter('zh-hans').convert(self.text.decode('utf-8'))
            self.text = line.encode('utf-8')

            words = pseg.cut(self.text)
            self.file.write('<sentence>\n')
            sentenceStart = True
            for w in words:
                if w.word == '。':
                    sentenceStart = False
                    self.file.write('</sentence>\n')

                if w.flag != 'x':
                    if sentenceStart == False:
                        self.file.write('<sentence>\n')
                        sentenceStart = True

                    self.file.write(w.word + '\t' + w.flag + '\n')

            if sentenceStart == True:
                sentenceStart = False
                self.file.write('</sentence>\n')

            #self.file.write(self.text)
            self.file.write('</text>\n')

            self.file.write('</page>\n')

            self.counter += 1
            self.title = ""
            self.text = ""

        self.CurrentData = ""


    def characters(self, content):
        if self.CurrentData == "title":
            self.title = self.title + content
        elif self.CurrentData == "text":
            self.text = self.text + content


if __name__ == "__main__":
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    Handler = MovieHandler('../data/raw-data/pages.xml')
    parser.setContentHandler(Handler)

    parser.parse('../data/raw-data/zhwiki-20141009-pages-articles-multistream.xml.bz2')
