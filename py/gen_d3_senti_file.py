import os
import sys
from nltk.stem.wordnet import WordNetLemmatizer

if __name__ == '__main__':
    char_limit = 5
    conf_limit = 0.005
    freq_limit = -20000
    topic_word_list = []
    topic_fh = open('../docs/fda_topic_list_10_03_13.txt', 'r')

    lmtzr = WordNetLemmatizer()

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
        if len(word_list[0]) < char_limit:
            continue
        word_confidence = float(word_list[1])
        if(word_confidence < conf_limit):
            continue
        # lemmatize topic word, and keep lemma w/ lowercase
        try:
            lemma_word = lmtzr.lemmatize(word_list[0][:-1])
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

    tweet_fh = open('tweets_senti_10_30_13.txt', 'r')

    topic_tw_word_info = {}
    for topic_word_info in topic_word_list:
        topic_tw_word_info[topic_word_info[0]] = []
    confidence_list = []
# for each tweet
    tweet_ctr = 1
    for tweet in tweet_fh:
        try:
            decision = float(tweet.split('==')[1].strip()) + 1.0
        except:
            decision = 0

        confidence_list.append(decision)

        tweet_list = tweet.split('==')[0].split()
#        print tweet_list
        tw_lemma_list = []
        for word in tweet_list:
        # lemmatize, and keep lemma of tweet words w/ lower case
            try:
                tw_lemma_list.append(lmtzr.lemmatize(word))
            except:
                continue
# for each topic
        for topic_word_info in topic_word_list:
            for tw_lemma in tw_lemma_list:
# for every topic word check if in tweet
                if topic_word_info[0] == tw_lemma:
# map topic word to tweet
                    topic_tw_word_info[topic_word_info[0]].append(tweet_ctr)
        tweet_ctr = tweet_ctr + 1

# count how many times topic word are in lines, only need to use len(topic_tw_word_info[topic_word])

    tweet_fh.close()

    topic_word_freq = {}
    confidence_dict = {}

    for topic_word_info in topic_word_list:
        for topic_word_info_2 in topic_word_list:
            words_key = topic_word_info[0] + '_' + topic_word_info_2[0]
            topic_word_freq[words_key] = 0
            confidence_dict[words_key] = 0

# for every topic 
    word_ctr_1 = 0
    for topic_word_info in topic_word_list:
        word_ctr_1 = word_ctr_1 + 1
        word_ctr_2 = 0
        for topic_word_info_2 in topic_word_list:
# word 1, and word 2, don't need word 2 and word 1 frequency
            word_ctr_2 = word_ctr_2 + 1
            if word_ctr_1 > word_ctr_2:
                continue
            if topic_word_info_2[0] == topic_word_info[0]:
                continue
            for topic_tw_num in topic_tw_word_info[topic_word_info[0]]:
                for topic_tw_num_2 in topic_tw_word_info[topic_word_info_2[0]]:
                     if topic_tw_num_2 == topic_tw_num:
                         words_key = topic_word_info[0] + '_' + topic_word_info_2[0]
#                         print len(confidence_list)
#                         print 'topic_tw_num = ' + str(topic_tw_num)

#                         topic_word_freq[words_key] = topic_word_freq[words_key] + 1
                         topic_word_freq[words_key] = topic_word_freq[words_key] + confidence_list[topic_tw_num]
                         confidence_dict[words_key] = confidence_dict[words_key] + 1
#                         print words_key
# for every topic word

# check if topic word 1 is in the same line as word n

# check if topic word 1 is in the same line as word 2,3,4,5...

# check if topic word 2 is in same line as word 3,4,5,6...

# calculate frequency of word 1 is in the same line with word 2 (multiply by 10)

# sort by frequency 

# if word 1, and word 2 are not in the same line, set frequency to 0

# write file that outputs topic word, and topic number

# write second file that outputs source, and target with frequency in line

    json_fh = open('senti_tweets.json', 'w')

    json_fh.write('{\n')
    json_fh.write('    \"nodes\":[\n')
    line_ctr = 0
    for word_info in topic_word_list:
        if line_ctr == word_list_ctr:
            write_str = '        {\"name\":\"' + word_info[0] + '\",' + '\"group\":' + str(word_info[2]) + '}\n'      
        else:
            write_str = '        {\"name\":\"' + word_info[0] + '\",' + '\"group\":' + str(word_info[2]) + '},\n'
        json_fh.write(write_str)
    json_fh.write('    ],\n')
    json_fh.write('    \"links\":[\n')

    word_ctr_1 = 0
    for word_info in topic_word_list:
        word_ctr_2 = 0
        for word_info_2 in topic_word_list:
            words_key = word_info[0] + '_' + word_info_2[0]
            if topic_word_freq[words_key] > freq_limit:
#                write_str = '        {\"source\":' + str(word_ctr_1) + ',\"target\":' + str(word_ctr_2) + ',\"value\":' + str(int(float(topic_word_freq[words_key])/tweet_ctr*1000)) + '},\n'
#                write_str = '        {\"source\":' + str(word_ctr_1) + ',\"target\":' + str(word_ctr_2) + ',\"value\":' + str(float(topic_word_freq[words_key])/float(confidence_dict[words_key])*10) + '},\n'
                write_str = '        {\"source\":' + str(word_ctr_1) + ',\"target\":' + str(word_ctr_2) + ',\"value\":' + str(float(topic_word_freq[words_key])) + '},\n'
                 
#                write_str = '        {\"source\":' + str(word_ctr_1) + ',\"target\":' + str(word_ctr_2) + ',\"value\":' + str(float(topic_word_freq[words_key])/tweet_ctr) + '},\n'
#                write_str = '        {\"source\":' + str(word_ctr_1) + ',\"target\":' + str(word_ctr_2) + ',\"value\":' + str(topic_word_freq[words_key]) + '},\n'
                json_fh.write(write_str)
            else:
#                print words_key
                word_ctr_2 = word_ctr_2 + 1
                continue
            word_ctr_2 = word_ctr_2 + 1
        word_ctr_1 = word_ctr_1 + 1

    json_fh.write('        ]\n')
    json_fh.write('    }\n')

    json_fh.close()
