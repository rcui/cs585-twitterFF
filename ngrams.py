import re, sys, nltk
from nltk import word_tokenize
from nltk.collocations import *


def read(filename):
    f = open(filename, 'r')
    data = f.read()
    data = re.sub('http\S+', '', data)
    data = re.sub('[@#]\S+', '', data)
    data = re.sub('[^0-9a-zA-Z \n]+', '', data)
    data = re.sub('&', '', data)
    data = data.lower()
    return data


def bigrams(data):
    tokens = word_tokenize(data)
    bg = nltk.bigrams(tokens)
    # stopwords = nltk.corpus.stopwords.words('english')
    stopwords = word_tokenize(read('susie_code/common_words.txt'))
    bg = [tup for tup in bg if not False in [False for word in tup if word in stopwords]]
    return bg


def trigrams(data):
    tokens = word_tokenize(data)
    tg = nltk.trigrams(tokens)
    # stopwords = nltk.corpus.stopwords.words('english')
    stopwords = word_tokenize(read('susie_code/common_words.txt'))
    tg = [tup for tup in tg if not False in [False for word in tup if word in stopwords]]
    return tg


def most_common(ngrams, k):
    return nltk.FreqDist(ngrams).most_common(k)


koreanupdates = read('sample_userdata/@KoreanUpdates_parsed.txt')
liuwenlw = read('sample_userdata/@LiuWenLW_parsed.txt')
tracysilverman = read('sample_userdata/@TracySilverman_parsed.txt')

print 'KoreanUpdates'
print most_common(bigrams(koreanupdates), 10)
print most_common(trigrams(koreanupdates), 10)

print 'LiuWenLW'
print most_common(bigrams(liuwenlw), 10)
print most_common(trigrams(liuwenlw), 10)

print 'TracySilverman'
print most_common(bigrams(tracysilverman), 10)
print most_common(trigrams(tracysilverman), 10)
