import sys
from nltk.stem.wordnet import WordNetLemmatizer
import nltk
from nltk.corpus import wordnet
from collections import OrderedDict
from operator import itemgetter

def check_stop_word(word, stopwords):
    if word.lower() not in stopwords:
        content = word.lower()
    else:
        content = ''
    if len(content) > 0:
        return content
    else:
        return ''

def get_word_syns(word):
    word_syns = wordnet.synsets(word)

    return word_syns
    
def gen_sent_dict(sent_ctr, info, info_list, info_ctr, part_of_sp, start_char_pos, stopwords, lmtzr):

    tmp_ctr = info_ctr
    for word in info.split():
        word = check_stop_word(word, stopwords)
        if word == '':
#            print 'Sent_ctr = ' + str(sent_ctr)
            continue
        lemma_word = lmtzr.lemmatize(word)
#        print 'lemma = ' + lemma_word
        pos_word = part_of_sp[info_ctr]
#        print ' pos_word ' + pos_word + ' ' + 'start_char_pos = ' + start_char_pos
        if pos_word[0] == start_char_pos:
#            print 'lemma = ' + lemma_word + ' pos = ' + pos_word
            info_list.append(lemma_word)
        info_ctr = info_ctr + 1
    if tmp_ctr == info_ctr:
        info_list.append('All_Stop_Words')
    
reverb_data_file = open('../data/reverb_output_09_20_13.txt','r')
#reverb_data_file = open('../data/test_reverb.txt','r')
fuxi_fh = open('../data/test_fuxi_facts.n3', 'w')
stopwords = nltk.corpus.stopwords.words('english')
lmtzr = WordNetLemmatizer()

pos_fh = open('../data/corpus_2/pos.txt')
part_of_spe_tag = {}
for pos in pos_fh:
    part_of_spe_tag[pos.strip()] = True

sentence_list = {}
sent_num_list = {}
list_ctr = 0
sent_ctr = 0
r_subj_list = []
r_rel_list = []
r_obj_list = []
subj_list = []
obj_list = []
rel_list = []
for line in reverb_data_file:
    confidence = float(line.split('\t')[11])
    if confidence < 0.5:
        continue
    sent = line.split('\t')
    subj = sent[2]
    subj_list.append(subj)
    relation = sent[3]
    rel_list.append(relation)
    obj = sent[4]
    obj_list.append(obj)
    rel = sent[3]
    rel_list.append(rel)
    part_of_sp = sent[13].split()
    start_subj_index = int(sent[5])
    end_subj_index = int(sent[6])
    start_rel_index = int(sent[7])
    end_rel_index = int(sent[8])
    start_obj_index = int(sent[9])
    end_obj_index = int(sent[10])
    sentence_list[str(sent_ctr)] = sent[12]
    sent_num_list[str(sent_ctr)] = sent[1]

    subj_ctr = start_subj_index
    gen_sent_dict(sent_ctr, subj, r_subj_list, subj_ctr, part_of_sp, 'N', stopwords, lmtzr)

    obj_ctr = start_obj_index
    # perform above sbj counting for object
    gen_sent_dict(sent_ctr, obj, r_obj_list, obj_ctr, part_of_sp, 'N', stopwords, lmtzr)
 
    rel_ctr = start_rel_index
    # perform above sbj counting for object
    gen_sent_dict(sent_ctr, rel, r_rel_list, rel_ctr, part_of_sp, 'V', stopwords, lmtzr)
  
    sent_ctr = sent_ctr + 1

# sort both subj_dict, and obj_dict by [0]
#sorted_obj_dict = OrderedDict(sorted(obj_dict.items(), key=itemgetter(1), reverse=True))
#sorted_subj_dict = OrderedDict(sorted(subj_dict.items(), key=itemgetter(1), reverse=True))
#sorted_rel_dict = OrderedDict(sorted(rel_dict.items(), key=itemgetter(1), reverse=True))

s_ctr = 0
ctr_lim = 20
#for s_key in sorted_subj_dict.keys():
#    print s_key + ' ' + str(sorted_subj_dict[s_key])
#    if s_ctr > ctr_lim:
#        break
#    s_ctr = s_ctr + 1

# print top 10 sentences by printing lines of [1]
ctr_lim = 20
o_ctr = 0
s_ctr = 0
fuxi_fh.write('@prefix ex: <http://example.org/> .\n')
fuxi_fh.write('@prefix owl: <http://www.w3.org/2002/07/owl#>.\n\n')
for (ss, rr, oo) in zip(r_subj_list, r_rel_list, r_obj_list):
    if (ss == 'All_Stop_Words') | (rr == 'All_Stop_Words') | (oo == 'All_Stop_Words'):
        continue
    write_str = 'ex:' + ss + ' ' + 'ex:' + rr + ' '+ '\"' + oo + '\".\n'
    fuxi_fh.write(write_str)


reverb_data_file.close()
fuxi_fh.close()
