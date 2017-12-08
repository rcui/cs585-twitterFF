from gensim import corpora, models
import re
import twokenize
import stopwords
from pprint import pprint

url = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
stopWords = stopwords.get_stopwords('en')

def clean_up(doc_list):
    doc_list = [filter(lambda x: x[0] != "@" and url.search(x) == None and any(char.isalpha() or char.isdigit() for char in x),
                       twokenize.tokenize(doc))
                for doc in doc_list]
    for i in range(len(doc_list)):
        doc_list[i] = map(lambda x: re.sub(r'\W+', '', x[1:]) if x[0] == "#" else re.sub(r'\W+', '', x), doc_list[i])
        doc_list[i] = filter(lambda x: x not in stopWords and "htt" not in x, doc_list[i])
    return doc_list

def lda(doc_list):
    doc_list = clean_up(doc_list)
    dictionary = corpora.Dictionary(doc_list)
    corpus = [dictionary.doc2bow(doc) for doc in doc_list]
    ldamodel = models.wrappers.LdaMallet('mallet-2.0.8/bin/mallet', corpus=corpus, num_topics=5, id2word=dictionary)
    return ldamodel.show_topics(num_topics=-1, num_words=10, formatted=False)

def main():
    with open("../sample_userdata/@LiuWenLW_parsed.txt", 'r') as inp:
        doc_list = inp.readlines()
    pprint(lda(doc_list))

if __name__ == "__main__":
    main()
