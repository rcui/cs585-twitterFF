import re, sys
from collections import defaultdict

import nltk
import enchant

def parse(filename):
    f = open(filename, 'r')
    data = f.read()
    tweets = re.findall("    .*$", data, re.MULTILINE)
    tweets = [tweet.strip() for tweet in tweets]
    tweets = '\n'.join(tweets)
    return tweets

def tokenize_tweets(tweet_txt, exclude_list):
    bow = defaultdict(float)
    d = enchant.Dict("en_US")

    tokens = tweet_txt.split()
    lowered_tokens = map(lambda t: t.lower(), tokens)

    for token in lowered_tokens:
        token = re.sub(r'\W+', '', token)

        if len(token) <= 2:
            continue
        if token[:4] == "http":
            continue
        if token in exclude_list:
            continue
        # if not d.check(token):
        #     continue

        bow[token] += 1.0

    return dict(bow)

def exclude_list(filename):
    f = open(filename, 'r')
    data = f.read()
    exclude_words = data.split()
    return exclude_words

def print_top(word_score_list, top_num):
    for k,v in word_score_list[:top_num]:
        print k, ":", v


def main():
    if len(sys.argv) is 3:
        name_ext = sys.argv[1].split(".")
        name = name_ext[0]
        f = open(name + "_filtered.txt", 'w')

        filter_list = exclude_list(sys.argv[2]) + [name.lower()]

        tweets_text = parse(sys.argv[1])
        tweets_bow = tokenize_tweets(tweets_text, filter_list)

        sorted_bow = sorted(tweets_bow.items(), key=lambda x: -x[1])
        print_top(sorted_bow, 30)

        f.write(tweets_text)
        f.write('\n')
        f.close()
    else:
        print 'Usage: python filter_tweet.py input output'

if __name__ == "__main__":
    main()
