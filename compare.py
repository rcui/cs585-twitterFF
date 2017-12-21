import numpy as np
from scipy import spatial
from nltk.stem import *
from nltk.corpus import wordnet as wn
import re
import ast


def read(filepath):
    with open(filepath) as f:
        topics = ast.literal_eval(f.read())
    topics = [topic[1] for topic in topics]
    topics = [[word[0].encode('ascii') for word in topic] for topic in topics]

    '''
    begin preprocessing
    '''
    # stemmer = LancasterStemmer()
    for i in range(len(topics)):
        for j in range(len(topics[i])):
            topics[i][j] = topics[i][j].lower()
            syns = wn.synsets(topics[i][j])
            for syn in syns:
                topics[i].append(re.sub('\.\S+', '', syn.name()).encode('utf8'))
            # topics[i][j] = stemmer.stem(topics[i][j])

    return topics


def generate_vectors(v1, v2):
    master = list(set(v1 + v2))
    nv1 = np.zeros(shape=(len(master), 1))
    nv2 = np.zeros(shape=(len(master), 1))
    for i in range(len(master)):
        if master[i] in v1:
            nv1[i] = 1
        if master[i] in v2:
            nv2[i] = 1
    return nv1, nv2


def compare(lda1, lda2):
    sims = np.zeros(shape=(len(lda1), len(lda2)))
    for i in range(len(lda1)):
        for j in range(len(lda2)):
            vectors = generate_vectors(lda1[i], lda2[j])
            sims[i, j] = (1 - spatial.distance.cosine(vectors[0], vectors[1])) / len(lda1)


    return sims

text1 = 'test1.txt'
text2 = 'test2.txt'
text3 = 'test3.txt'
text4 = 'test4.txt'
text5 = 'test5.txt'
text6 = 'test6.txt'

lda1 = read(text1)
lda2 = read(text2)
lda3 = read(text3)
lda4 = read(text4)
lda5 = read(text5)
lda6 = read(text6)

print 'group 1'
res = compare(lda1, lda2)
print res
print res.sum()
print np.amax(res)

print 'group 2'
res = compare(lda3, lda4)
print res
print res.sum()
print np.amax(res)

print 'group 3'
res = compare(lda1, lda3)
print res
print res.sum()
print np.amax(res)

print 'group 4'
res = compare(lda2, lda4)
print res
print res.sum()
print np.amax(res)

print 'group 5'
res = compare(lda1, lda4)
print res
print res.sum()
print np.amax(res)

print 'group 6'
res = compare(lda2, lda3)
print res
print res.sum()
print np.amax(res)

print 'group 7'
res = compare(lda5, lda6)
print res
print res.sum()
print np.amax(res)

print 'group 8'
res = compare(lda5, lda2)
print res
print res.sum()
print np.amax(res)

print 'group 9'
res = compare(lda6, lda3)
print res
print res.sum()
print np.amax(res)
