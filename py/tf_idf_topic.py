import sys
from nltk.stem.wordnet import WordNetLemmatizer
import nltk
from nltk.corpus import wordnet

def check_stop_word(word, stopwords):
    if word.lower() not in stopwords:
        content = word.lower()
    else:
        content = ''
    if len(content) > 0:
        return content
    else:
        return ''

idea_data_file = open('../data/corpus_2/merged_corpus.txt','r')

corpus_words = []
for line in idea_data_file:
    for sent in line.lower().split('.'):
        corpus_words.append(sent.split())

stopwords = nltk.corpus.stopwords.words('english')
lmtzr = WordNetLemmatizer()
word_dict = {}

for word in corpus_words:
    sw_word = ''
    if len(word) > 0:
        sw_word = check_stop_word(word[0], stopwords)
    if sw_word != '':
        lm_word = lmtzr.lemmatize(sw_word.strip())
        if wordnet.synsets(lm_word):
            if lm_word not in word_dict.keys():
                word_dict[lm_word] = True


tc = nltk.TextCollection(corpus_words)

score_dict = {}

for idx in range(len(corpus_words)):
    for term in word_dict.keys():
        if len(corpus_words[idx]) > 0:
            score = tc.tf_idf(term, corpus_words[idx])
            score_dict[term] = score

sorted_score_dict = sorted(score_dict, key=score_dict.get, reverse=True)

for idx in range(0,2,10):
    print str(sorted_score_dict[idx]) + '  ' + str(sorted_score_dict[idx+1])

