
import sys
import os
import json
import base64


if __name__ == '__main__':

    twitter_json_file = open('json_twitter_10_01_13.txt', 'r')

    tw_json = json.loads(twitter_json_file.read())

    len_key = len(tw_json.keys())
    key = tw_json.keys()
    cellset_len = len(tw_json['CellSet'].keys())
    cellset_key = tw_json['CellSet'].keys()
    row_len = len(tw_json['CellSet']['Row'])
    row_list = base64.b64decode(tw_json['CellSet']['Row'][0]['Cell']['content'])
    json_tweets = tw_json['CellSet']['Row']
    print str(len_key) + ' ' + str(key) + ' ' + str(cellset_len) + ' ' + str(cellset_key) + ' ' + str(row_len) + ' ' + str(row_list)
    tweet_fh = open('tweets_10_01_13.txt', 'w')
    for j_tw in json_tweets:
  
        print j_tw['Cell']['content']
        try:
            tweet_str = base64.b64decode(j_tw['Cell']['content']).encode('utf8') + '\n'.encode('utf8')
        except:
            tweet_str = str(base64.b64decode(j_tw['Cell']['content'])) + '\n'
        tweet_fh.write(tweet_str)

    tweet_fh.close()
    twitter_json_file.close()

#    ctr = 0
#    for j_key in keys:
#        print str(tw_json[j_key])
#        ctr = ctr + 1
#        if ctr > 10:
#            break
