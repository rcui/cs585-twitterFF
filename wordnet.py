import re, sys, nltk
from nltk import word_tokenize
from nltk.corpus import wordnet as wn
from nltk.collocations import *


def read(filename):
    f = open(filename, 'r')
    data = f.read()
    data = re.sub('https\S+', '', data)
    data = re.sub('[@#]\S+', '', data)
    data = re.sub('[^0-9a-zA-Z \n]+', '', data)
    data = re.sub('amp', '', data)
    data = data.lower()
    return data

def get_synsets(data):
    tokens = word_tokenize(data)
    # stopwords = nltk.corpus.stopwords.words('english')
    stopwords = word_tokenize(read('susie_code/common_words.txt'))
    words = [word for word in tokens if word not in stopwords]
    syns = [wn.synsets(word) for word in words]
    syns = [syn[0] for syn in syns if syn]
    return syns


def synsethize(data):
    syns = [syn.name() for syn in get_synsets(data)]
    return syns


def lemmatize(data):
    lemmas = [syn.lemmas()[0].name() for syn in get_synsets(data)]
    return lemmas


def most_common(data, k):
    fd = nltk.FreqDist(data).most_common(k)
    fd = [(re.sub('\.\S+', '', word[0]).encode('utf8'), word[1]) for word in fd]
    return fd


koreanupdates = read('sample_userdata/@KoreanUpdates_parsed.txt')
liuwenlw = read('sample_userdata/@LiuWenLW_parsed.txt')
tracysilverman = read('sample_userdata/@TracySilverman_parsed.txt')

print 'KoreanUpdates'
print most_common(synsethize(koreanupdates), 10)
print most_common(lemmatize(koreanupdates), 10)

print 'LiuWenLW'
print most_common(synsethize(liuwenlw), 10)
print most_common(lemmatize(liuwenlw), 10)

print 'TracySilverman'
print most_common(synsethize(tracysilverman), 10)
print most_common(lemmatize(tracysilverman), 10)
