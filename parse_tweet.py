import re, sys


def parse(filename):
    f = open(filename, 'r')
    data = f.read()
    tweets = re.findall("    .*$", data, re.MULTILINE)
    tweets = [tweet.strip() for tweet in tweets]
    tweets = '\n'.join(tweets)
    return tweets


def main():
    if len(sys.argv) is 3:
        f = open(sys.argv[2], 'w')
        f.write(parse(sys.argv[1]))
        f.write('\n')
        f.close()
    else:
        print 'Usage: python parse_tweet.py input output'

if __name__ == "__main__":
    main()
