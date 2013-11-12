import os
import sys
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import wordnet

class get_topic_info():


    def __init__(self):
        self.__number = 0

    def get_topic_word_list(self, file_name, topic_word_list, char_limit, conf_limit, freq_limit, lmtzr):

        topic_fh = open(file_name, 'r')

# read in topic words, and confidence
        topic_num = 0
        first_line_flag = True
        word_list_ctr = 0
        for line in topic_fh:
            if line == '\n':
                continue
            if line[0] == '-':
                if first_line_flag:
                    first_line_flag = False
                    continue
                else:
                    topic_num = topic_num + 1
                    continue
            word_list = line.split()
            if (len(word_list[0]) < char_limit):
                continue
            word_confidence = float(word_list[1])
            if(word_confidence < conf_limit):
                continue
            # lemmatize topic word, and keep lemma w/ lowercase
            try:
                lemma_word = lmtzr.lemmatize(word_list[0][:-1])
        
                if (not wordnet.synsets(lemma_word)) | (lemma_word == 'ecig') | (lemma_word == 'http'):
                    if (lemma_word == 'ecig'):
                        tmp_word = True
                    else:
                        continue
            except:
                continue
            word_lemma_flag = False
            for topic_word in topic_word_list:
                if topic_word[0] == lemma_word:
                    word_lemma_flag = True

            if word_lemma_flag:
                continue
            else:
                topic_word_list.append([lemma_word, word_confidence, topic_num])
                word_list_ctr = word_list_ctr + 1

        topic_fh.close()

        return (topic_num + 1)



    def get_tw_words(self, file_name, topic_tw_word_info, topic_word_list, b_classifier, senti_flag, lmtzr):
        tweet_fh = open(file_name, 'r')

# for each tweet
        tweet_ctr = 1
        for tweet in tweet_fh:
            try:
                tw_sp = tweet.split('==')
                tw_key = tw_sp[0]
                tw_text = tw_sp[1]
            except:
                continue
            tweet_list = tw_text.split()
            if senti_flag:
                senti_dict = {}
                for word in tweet_list:
                    senti_dict[word] = True
                confidence = b_classifier.classify(senti_dict)
                print str(confidence)

            tw_lemma_list = []
            for word in tweet_list:
        # lemmatize, and keep lemma of tweet words w/ lower case
                try:
                    tw_lemma_list.append(lmtzr.lemmatize(word.lower().replace(',','').replace('.','').replace(':','').replace('\'','').replace('\"','').replace('?','').replace('!','').replace('@','')))
                except:
                    continue
# for each topic
#            print str(topic_word_list) + ' ' + str(tw_lemma_list)
#            print str(tw_lemma_list)
            for topic_word_info in topic_word_list:
                for tw_lemma in tw_lemma_list:
# for every topic word check if in tweet
#                    if topic_word_info[0] == tw_lemma.lower().replace('?','').replace(',','').replace('.','').replace('\'','').replace('\"','').replace('@','').replace(':','').replace('!',''):
                    if topic_word_info[0] == tw_lemma:
# map topic word to tweet
                        if senti_flag:
                            topic_tw_word_info[topic_word_info[0]].append(confidence + 1.0)
                            break
                        else:
                            topic_tw_word_info[topic_word_info[0]].append(tw_key)
            tweet_ctr = tweet_ctr + 1

# count how many times topic word are in lines, only need to use len(topic_tw_word_info[topic_word])

        tweet_fh.close()


