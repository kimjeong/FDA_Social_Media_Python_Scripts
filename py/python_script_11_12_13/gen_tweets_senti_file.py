
import sys
import os
import json
import base64
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
 
def word_feats(words):
    return dict([(word, True) for word in words])

def get_classifier():
    negids = movie_reviews.fileids('neg')
    posids = movie_reviews.fileids('pos')
 
    negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
    posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]
 
    negcutoff = len(negfeats)*3/4
    poscutoff = len(posfeats)*3/4
 
    trainfeats = negfeats + posfeats
    #testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
    #print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))
 
    classifier = NaiveBayesClassifier.train(trainfeats)

    return classifier

if __name__ == '__main__':

    twitter_json_file = open('json_twitter_10_01_13.txt', 'r')

    tw_json = json.loads(twitter_json_file.read())

    b_classifier = get_classifier()

    len_key = len(tw_json.keys())
    key = tw_json.keys()
    cellset_len = len(tw_json['CellSet'].keys())
    cellset_key = tw_json['CellSet'].keys()
    row_len = len(tw_json['CellSet']['Row'])
    row_list = base64.b64decode(tw_json['CellSet']['Row'][0]['Cell']['content'])
    json_tweets = tw_json['CellSet']['Row']
#    print str(len_key) + ' ' + str(key) + ' ' + str(cellset_len) + ' ' + str(cellset_key) + ' ' + str(row_len) + ' ' + str(row_list)
    tweet_fh = open('tweets_senti_10_30_13.txt', 'w')
    for j_tw in json_tweets:
  
#        print j_tw['Cell']['content']
        
        try:
            tweet_str = base64.b64decode(j_tw['Cell']['content']).encode('utf8')
        except:
            try:
                tweet_str = str(base64.b64decode(j_tw['Cell']['content']))
            except:
                continue

        senti_words = tweet_str.split()
        senti_dict = {}
        for word in senti_words:
            senti_dict[word] = True
        confidence = b_classifier.classify(senti_dict)
 
        tweet_fh.write(tweet_str + ' == ' + str(confidence) + '\n')

    tweet_fh.close()
    twitter_json_file.close()

#    ctr = 0
#    for j_key in keys:
#        print str(tw_json[j_key])
#        ctr = ctr + 1
#        if ctr > 10:
#            break