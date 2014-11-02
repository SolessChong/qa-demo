SEGMENTER=/Volume/STUPID-USB/stanford-segmenter-2014-10-26/segment.sh
RAWDATA=data/raw-data

target: query-preprocess document--process answer-retrivel

clean:
	rm -rf query-preprocess
	rm -rf data-process
	rm -rf answer-retrivel

query-preprocess: data/query-preprocess/query-segment data/query-preprocess/quer-analysis

data/query-preprocess/query-segment: $(RAWDATA)/query
	mkdir -p data/query-preprocess
	sh $(SEGMENTER) pku $^ UTF-8 0 > $@

data/query-preprocess/query-analysis: data/query-preprocess/query-segment
	mkdir -p data/query-preprocess

document-preprocess: data/document-preprocess/document-clean data/document-preprocess/document-extraction

data/document-preprocess/document-clean: $(RAWDATA)/document
	mkdir -p data/document-preprocess
	python scripts/clean-document.py $^ $@

data/document-preprocess/document-extraction: data/document-preprocess/document-clean
	mkdir -p data/document-preprocess
	python scripts/extract-documtent.py $^ $@


answer-retrivel: data/answer-retriveel/document-retrivel data/answer-retrivel/answer-rank
	
data/answer-retrivel/document-retrivel: ?
	mkdir -p data/answer-retrivel
	python scripts/retrivel-answer.py ?

