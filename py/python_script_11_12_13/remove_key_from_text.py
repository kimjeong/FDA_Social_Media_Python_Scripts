import os
import sys
from nltk.stem.wordnet import WordNetLemmatizer

if __name__ == '__main__':

    tw_key_text_fh = open('../data/key_tweets_10_10_2013.txt','r')
    tw_text_fh = open('../data/tweets_10_10_2013.txt','w')

    for line in tw_key_text_fh:
        try:
            write_str = line.split('==')[1]
        except:
            continue
        tw_text_fh.write(write_str)

    tw_key_text_fh.close()
    tw_text_fh.close()
    
