from gensim import corpora, models
import re
import twokenize
import sys
import json
from nltk.corpus import stopwords

# This regex is used to remove URL from the text
url = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
stopWords = list(stopwords.words('english'))
# A list of additional stopwords to removed for this problem
with open('additional_stopwords.txt', 'r') as sw:
    stopWords += ' '.join(sw.readlines()).split()


def clean_up(doc_list):
    # Filtered out mentions and tokens without any alphabet characters / urls
    doc_list = [filter(lambda x: x[0] != "@" and url.search(x) == None and any(char.isalpha() for char in x),
                       twokenize.tokenize(doc))
                for doc in doc_list]
    for i in range(len(doc_list)):
        # remove all non-alphanumeric characters
        doc_list[i] = map(lambda x: re.sub(r'\W+', '', x[1:]) if x[0] == "#" else re.sub(r'\W+', '', x), doc_list[i])
        # remove stopwords & links
        doc_list[i] = filter(lambda x: x.lower() not in stopWords and "htt" not in x, doc_list[i])
    return doc_list

def tuple_to_dict(topics):
    # Convert the output of LDA to a dict of dict to store as json
    d = {}
    for topic in topics:
        words = {}
        for word in topic[1]:
            words[word[0].lower()] = word[1]
        d[topic[0]] = words
    return d

def lda(doc_list):
    doc_list = clean_up(doc_list)
    dictionary = corpora.Dictionary(doc_list)
    corpus = [dictionary.doc2bow(doc) for doc in doc_list]
    ldamodel = models.wrappers.LdaMallet('mallet-2.0.8/bin/mallet', corpus=corpus, num_topics=5, id2word=dictionary)
    return ldamodel.show_topics(num_topics=-1, num_words=7, formatted=False)

# This piece of code will take a list of usernames and compute the LDA output for those users.
# This requires that the twitter-log of a user is downloaded, parsed and put in the lda_data directory with the filename
# username_parsed.txt
def main():
    user_file = sys.argv[1]
    with open(user_file, 'r') as inp:
        users = inp.readlines()

    for user in users:
        try:
            with open("lda_data/" + user.strip() + "_parsed.txt", 'r') as inp:
                doc_list = inp.readlines()
            topics = tuple_to_dict(lda(doc_list))
            with open("lda_data/" + user.strip() + "_lda.json", 'w') as out:
                json.dump(topics, out, encoding='utf8', indent=4)
        except IOError:
            pass

if __name__ == "__main__":
    main()
