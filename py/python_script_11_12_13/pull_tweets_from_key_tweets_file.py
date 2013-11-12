import os
import sys

if __name__ == '__main__':


    reverb_fh = open('../sw/reverb/reverb_output_11_04_13.txt', 'r')
    tweet_fh = open('../data/key_tweets_10_10_2013.txt', 'r')    
    output_fh = open('../data/key_tweet_reverb_11_04_2013.txt', 'w')
    line_ctr = 0

    tweet = tweet_fh.readline()
    for r_line in reverb_fh:
        r_line_sp = r_line.split('\t')
        if tweet.find('==') > 0:
            write_str = tweet.replace('\n','') + ' ' + str(r_line_sp[11]) + '\n'
            output_fh.write(write_str)

        tweet = tweet_fh.readline()
        if tweet.find('==') < 0:
            while tweet.find('==') < 0:
                tweet = tweet_fh.readline()

    reverb_fh.close()
    output_fh.close()
    tweet_fh.close()
