#!/usr/bin/python

from nltk.stem.wordnet import WordNetLemmatizer
import sys

fr = open('../data/challenge_details_2.csv', 'r')
#fr = open('../data/corpus_2/lda_subtopic_homeless_match_topic_1_2.txt', 'r')
fw = open('../data/corpus_2/lda_sentence_match.txt', 'w')

sentence_lim = 3
topic_words = []
lda_sentences = []

lmtzr = WordNetLemmatizer()

#lda_topic_words = ['card', 'homeless', 'veteran'] # topic 1
#lda_topic_words = ['patient', 'appointment', 'time', 'information', 'medication', 'provider', 'system', 'veteran'] # topic 2
#lda_topic_words = ['care', 'process', 'team', 'system', 'patient'] # topic 3
#lda_topic_words = ['va', 'facility', 'medical', 'center', 'department'] # topic 5
#lda_topic_words = ['veteran', 'va', 'service', 'care', 'program', 'health', 'provide', 'medical']  # topic 8
#lda_topic_words = ['cost', 'va', 'time', 'employee', 'travel', 'save', 'money', 'pay', 'facility']  # topic 9
#lda_topic_words = ['employee', 'position', 'job']
#lda_topic_words = ['patient', 'time', 'area', 'day', 'staff', 'clinic', 'room', 'work', 'call'] # topic 19 not interesting
#lda_topic_words = ['patient', 'appointment', 'medication', 'information', 'time', 'veteran', 'provider', 'cpr', 'order'] # topic 2B
#lda_topic_words = ['employee', 'va', 'position', 'training', 'job', 'work'] # topic 13B

#lda_topic_words = ['id', 'appointment'] # topic 1 for homeless subtopic
#lda_topic_words = ['homeless', 'veteran', 'program'] # topic 2 for homeless subtopic
#lda_topic_words = ['medical', 'record', 'exam', 'veteran', 'service'] 
#lda_topic_words = ['claim', 'process', 'veteran', 'time', 'document', 'office'] 
#lda_topic_words = ['information', 'system', 'time', 'data', 'change']
#lda_topic_words = ['employee', 'work', 'training', 'time', 'job', 'year', 'staff']
#lda_topic_words = ['item', 'pay', 'travel', 'food', 'supply']
#lda_topic_words = ['time', 'va', 'cost', 'save', 'year', 'money', 'paper', 'saving']
#lda_topic_words = ['veteran', 'va', 'program', 'service']
#lda_topic_words = ['medication', 'patient', 'cpr', 'order', 'provider', 'pharmacy']
#lda_topic_words = ['care', 'veteran', 'health', 'service', 'va', 'patient', 'treatment', 'provide', 'medical']
#lda_topic_words = ['employee', 'work', 'position', 'idea']
lda_topic_words = ['veteran', 'appointment', 'time', 'information', 'system']
ctr = 0
for word in lda_topic_words:
    topic_words.append(lmtzr.lemmatize(word.lower().strip()))
    ctr = ctr + 1

lda_ctr = 0
for line in fr:
#    print line
#   split the data depending with '.'
    sentences = line.split('.')
    keep_sent = False
    if len(sentences) > 0:
        for sent in sentences:
            words = sent.split(' ')
            if len(words) > 0:
                stem_ctr = 0
                keep_sent = False
                topic_index = []
                for word in words:
                    try:
                        stem = lmtzr.lemmatize(word.lower().strip())
                        topic_ctr = 0
                        for topic_w in topic_words:
                            if stem == topic_w:
                                cnt_flag = True
                                for index in topic_index:
                                    if topic_ctr == index:
                                        cnt_flag = False
                                if cnt_flag:
                                    stem_ctr = stem_ctr + 1
                                topic_index.append(topic_ctr)
                            topic_ctr = topic_ctr + 1
                        if stem_ctr > sentence_lim:
                            keep_sent = True
                    except:
                        print('Error: ' + word.strip() + ' is not a word')
            if keep_sent:
                lda_sentences.append(sent)
                lda_ctr = lda_ctr + 1

print 'num_lda_sent = ' + str(len(lda_sentences))

for lda_sent in lda_sentences:
    out_sent = lda_sent + '\n'
    fw.write(out_sent)

fw.close()
fr.close()
