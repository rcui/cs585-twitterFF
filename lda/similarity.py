# To run this file: python2 similarity.py twitter.txt from this directory

import lda
import json
import sys

def tuple_to_dict(topics):
    d = {}
    for topic in topics:
        words = {}
        for word in topic[1]:
            words[word[0].lower()] = word[1]
        d[topic[0]] = words
    return d


def run_lda(user, rerun=False):
    # run LDA for the user and save the output to a json file.
    # only rerun LDA when rerun = True or when the LDA json output for the user does not exist.
    if not rerun:
        try:
            with open("lda_data/" + user + "_lda.json", 'r') as inp:
                topics = json.load(inp)
                return topics
        except IOError:
            pass

    with open("lda_data/" + user + "_parsed.txt", 'r') as inp:
        doc_list = inp.readlines()
        topics = tuple_to_dict(lda.lda(doc_list))
        with open("lda_data/" + user + "_lda.json", 'w') as out:
            json.dump(topics, out, encoding='utf8', indent=4)
        return topics

import math

# sum of  cosine similarity of all possible pairs of topics
def cosine(topics1, topics2):
    score = 0
    for topic1 in topics1.values():
        for topic2 in topics2.values():
            numerator = 0
            dena = 0
            for key1,val1 in topic1.iteritems():
                numerator += val1*topic2.get(key1,0.0)
                dena += val1*val1
            denb = 0
            for val2 in topic2.values():
                denb += val2*val2
            score += numerator/math.sqrt(dena*denb)
    return score

# sum of jaccard similarity of all topics
def jaccard(topics1, topics2):
    score = 0
    for topic1 in topics1.values():
        for topic2 in topics2.values():
            t1 = set(topic1.keys())
            t2 = set(topic2.keys())
            score += len(t1.intersection(t2))
    return score


group = {}
with open(sys.argv[1], 'r') as inp:
    users = inp.readlines()
    user_topics = []
    for user in users:
        username = user.strip().split()[0]
        g = user.strip().split()[1]
        topics = run_lda(username)
        user_topics += [(username, topics)]
        group[username] = g

scores = []
for i in xrange(len(user_topics) - 1):
    for j in xrange(i+1, len(user_topics)):
        user1, topics1 = user_topics[i]
        user2, topics2 = user_topics[j]
        score = cosine(topics1, topics2)
        # score = jaccard(topics1, topics2)
        scores.append((score, user1, user2))

scores.sort()
with open('same_group.txt', 'w') as out:
    for item in scores:
        user1 = item[1]
        user2 = item[2]
        if group[user1] == group[user2]:
            out.write(str(item) + "\n")

with open('different_group.txt', 'w') as out:
    for item in scores:
        user1 = item[1]
        user2 = item[2]
        if group[user1] != group[user2]:
            out.write(str(item) + "\n")