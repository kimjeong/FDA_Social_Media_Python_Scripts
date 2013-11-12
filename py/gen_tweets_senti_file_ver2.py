
import sys
import os
import json
import base64
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from get_topic_info import get_topic_info
from nltk.stem.wordnet import WordNetLemmatizer
 
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

def get_topic_confidence_info(topic_tw_word_info, topic_word_list, num_topic_words, topic_conf_avg):
    total_conf = 0.0
    max_conf = 0.0
    topic_word_conf_avg = []
    for ctr in range(0,len(topic_word_list)):
        conf_sum = 0.0
        conf_ctr = 0
        for conf_num in topic_tw_word_info[topic_word_list[ctr][0]]: 
            conf_sum = conf_sum + conf_num
            conf_ctr = conf_ctr + 1

                
        if(conf_ctr > 0):
            topic_word_conf_avg.append(conf_sum/float(conf_ctr))
        else:
            topic_word_conf_avg.append(0.0)

    ctr = 0
    topic_ctr = 0
    for topic_ctr in range(0, num_topic_words):
        ele_ctr = 0
        conf_sum = 0.0
        while topic_word_list[ctr][2] == topic_ctr:
            conf_sum = topic_word_conf_avg[ctr] + conf_sum 
            ele_ctr = ele_ctr + 1
            if(ctr < (len(topic_word_list) - 1)):
                 ctr = ctr + 1
            else:
                 break

        if ele_ctr != 0:
            avg_num = conf_sum/float(ele_ctr)
#            if avg_num < 0.0:
#                avg_num = 100.0*(avg_num*-1.0 + 0.5)
#            else:
#                avg_num = avg_num*100.0
#           shift up by 0.5
            avg_num = 100.0*(avg_num + 0.6)            
            topic_conf_avg.append(avg_num)
        else:
            topic_conf_avg.append(0.0)


if __name__ == '__main__':
    char_limit = 4
    conf_limit = 0.005
    freq_limit = 0

    b_classifier = get_classifier()
    lmtzr = WordNetLemmatizer()

    topic_word_list = []
    get_topic_obj = get_topic_info()
    number_of_topics_set = get_topic_obj.get_topic_word_list('../docs/ecig_fda_topic_list_10_11_13.txt', topic_word_list, char_limit, conf_limit, freq_limit, lmtzr)

    topic_tw_word_info = {}
    senti_flag  = True

# initialize topic_tw_word_info with     
    for topic_word in topic_word_list:
        topic_tw_word_info[topic_word[0]] = []

    get_topic_obj.get_tw_words('../data/key_tweets_10_10_2013.txt', topic_tw_word_info, topic_word_list, b_classifier, senti_flag, lmtzr)
#    get_topic_obj.get_tw_words('test_d3_gen.txt', topic_tw_word_info, topic_word_list, b_classifier, senti_flag, lmtzr)

#    number_of_topics_set = 10

# for every topic word
    topic_num = 0
    flare_senti_fh = open('ecig_flare_tweets_ver1.json','w')

    flare_senti_fh.write('  {\n')
    flare_senti_fh.write('    \"name\":\"Twitter Sentiment Analysis\",\n')
    flare_senti_fh.write('    \"children\": [\n')
    topic_ctr = 0
    topic_conf_avg = []
    for topic_tuple_ctr in range(0,number_of_topics_set):
        flare_senti_fh.write('        {\"name\": \"Group ' + str(topic_num+1) + '\",\n')
        flare_senti_fh.write('        \"children\": [\n')

        get_topic_confidence_info(topic_tw_word_info, topic_word_list, number_of_topics_set, topic_conf_avg)
        while topic_word_list[topic_ctr][2] == topic_num:
#                print 'conf_num = ' + str(conf_num)
            if topic_conf_avg[topic_tuple_ctr] > 0:
                flare_senti_fh.write('            {\"name\": ' + '\"' + str(topic_word_list[topic_ctr][0]) + '\",' + ' \"value\":' + str(float(topic_word_list[topic_ctr][1]*1000.0)) + ', \"intensity\":' + str(topic_conf_avg[topic_tuple_ctr]) + '},\n')
            else:
                flare_senti_fh.write('            {\"name\": ' + '\"' + str(topic_word_list[topic_ctr][0]) + '\",' + ' \"value\":' + str(float(topic_word_list[topic_ctr][1]*1000.0)) + ', \"intensity\":0.0},\n')
            if(topic_ctr < (len(topic_word_list) - 1)):
                 topic_ctr = topic_ctr + 1
            else:
                 break
# for every topic_tw_word_info get the topic confidence, and for every senti get confidence
        topic_num = topic_num + 1
        flare_senti_fh.write('        ]\n')
        flare_senti_fh.write('    },\n')

    flare_senti_fh.write('    ]\n')
    flare_senti_fh.write(' }\n')
        
    flare_senti_fh.close()
