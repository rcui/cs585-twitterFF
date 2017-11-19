import re, sys
from collections import defaultdict

import nltk
from nltk.corpus import wordnet as wn
# import enchant

from sets import Set


# NOTE FOR WORD REPLACEMENT:
# IF WORD.SYNSET < 5: (not commonly used term) 
#   GET DEFINITION OF FIRST LEMMA AND REPLACE TERM WITH DEFINITION

def parse(filename):
    f = open(filename, 'r')
    data = f.read()
    tweets = re.findall("    .*$", data, re.MULTILINE)
    tweets = [tweet.strip() for tweet in tweets]
    tweets = '\n'.join(tweets)
    return tweets

def tokenize_tweets(tweet_txt, exclude_list):
    bow = defaultdict(float)
    tokens = tweet_txt.split()

    lowered_tokens = map(lambda t: t.lower(), tokens)
    for token in lowered_tokens:
        token = re.sub(r'\W+', '', token)
        if len(token) <= 2:
            continue
        if token[:4] == "http" or token == "amp":
            continue
        if token in exclude_list:
            continue
        if nltk.pos_tag([token])[0][1] == "NNS":
            continue
        if nltk.pos_tag([token])[0][1] in ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]:
            continue
        bow[token] += 1.0
    return dict(bow)

def get_exclude_list(filename):
    f = open(filename, 'r')
    data = f.read()
    exclude_words = data.split()
    return exclude_words

def get_top_words(word_score_list, top_num, filename):
    f = filename
    # d = enchant.Dict("en_US")
    eng = []
    non_eng = []
    for word,val in word_score_list:
        if len(wn.synsets(word)) > 0:
            eng.append((word,val))
        else:
            non_eng.append((word,val))

    print "%-20s %s" % ("ENG", "NON-ENG")
    for i in range(top_num+5):
        print "%-20s %s" % (eng[i][0], non_eng[i][0])

    for lst in [(eng, "ENG"), (non_eng, "NON-ENG")]:
        f.write(lst[1])
        f.write('\n')
        for i in range(top_num):
            l = lst[0]
            f.write(l[i][0])
            f.write('\n')
        f.write('\n')
    return 

def bag_of_words(tweet_txt, exclude_list, limit, filename):
    tweets_bow = tokenize_tweets(tweet_txt, exclude_list)
    sorted_tweets = sorted(tweets_bow.items(), key=lambda x: -x[1])
    get_top_words(sorted_tweets, limit, filename)
    return


def main():
    if len(sys.argv) is 3:
        name = sys.argv[1].split(".")[0]
        f = open(name + "_BOW.txt", 'w')

        tweets_text = parse(sys.argv[1])
        filter_list = get_exclude_list(sys.argv[2]) + [name[1:].lower()]

        bag_of_words(tweets_text, filter_list, 15, f)

        # f.write(tweets_text)
        f.write('\n')
        f.close()
    else:
        print 'Usage: python filter_tweet.py input_file filter_file'

if __name__ == "__main__":
    main()
