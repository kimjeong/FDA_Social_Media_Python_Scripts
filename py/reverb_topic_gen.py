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
    
def gen_sent_dict(sent_ctr, info, info_dict, info_ctr, part_of_sp, start_char_pos, stopwords, lmtzr):

    tmp_ctr = info_ctr
    for word in info.split():
        word = check_stop_word(word, stopwords)
        if word == '':
#            print 'Sent_ctr = ' + str(sent_ctr)
            continue
        lemma_word = lmtzr.lemmatize(word)

        pos_word = part_of_sp[info_ctr]
        if pos_word[0] == start_char_pos:
            if lemma_word not in info_dict.keys():
                info_dict[lemma_word] = [0, []]
            else:
                word_syns = get_word_syns(lemma_word)
                for ss in word_syns:
                    if ss.name.split('.')[0] in info_dict.keys():
                        info_dict[lemma_word][0] = info_dict[lemma_word][0] + 1
                        break
            info_dict[lemma_word][1].append(sent_ctr)
        info_ctr = info_ctr + 1
    if tmp_ctr == info_ctr:
        if 'All_Stop_Words' not in info_dict.keys():
            info_dict['All_Stop_Words'] = [-1, []]
        else:
            info_dict['All_Stop_Words'][0] = -1
            info_dict['All_Stop_Words'][1].append(sent_ctr)
    
reverb_data_file = open('../data/reverb_output_09_23_13.txt','r')
stopwords = nltk.corpus.stopwords.words('english')
lmtzr = WordNetLemmatizer()

sub_list = []

pos_fh = open('../data/corpus_2/pos.txt')
part_of_spe_tag = {}
for pos in pos_fh:
    part_of_spe_tag[pos.strip()] = True

sentence_list = {}
sent_num_list = {}
list_ctr = 0
sent_ctr = 0
subj_list = []
rel_list = []
obj_list = []
subj_dict = {}
obj_dict = {}
rel_dict = {}
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
    start_subj_index = int(sent[5]) - 1
    end_subj_index = int(sent[6])
    start_rel_index = int(sent[7])
    end_rel_index = int(sent[8])
    start_obj_index = int(sent[9])
    end_obj_index = int(sent[10])
    sentence_list[str(sent_ctr)] = sent[12]
    sent_num_list[str(sent_ctr)] = sent[1]

    subj_ctr = start_subj_index
    gen_sent_dict(sent_ctr, subj, subj_dict, subj_ctr, part_of_sp, 'N', stopwords, lmtzr)

    obj_ctr = start_obj_index
    # perform above sbj counting for object
    gen_sent_dict(sent_ctr, obj, obj_dict, obj_ctr, part_of_sp, 'N', stopwords, lmtzr)
 
    rel_ctr = start_rel_index
    # perform above sbj counting for object
    gen_sent_dict(sent_ctr, rel, rel_dict, rel_ctr, part_of_sp, 'V', stopwords, lmtzr)
  
    sent_ctr = sent_ctr + 1

# sort both subj_dict, and obj_dict by [0]
sorted_obj_dict = OrderedDict(sorted(obj_dict.items(), key=itemgetter(1), reverse=True))
sorted_subj_dict = OrderedDict(sorted(subj_dict.items(), key=itemgetter(1), reverse=True))
sorted_rel_dict = OrderedDict(sorted(rel_dict.items(), key=itemgetter(1), reverse=True))

ctr = 0
for r_key in sorted_rel_dict.keys():
    print str(sorted_rel_dict[r_key][0])
    if ctr > 50:
        break
    ctr = ctr + 1
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
for o_key in sorted_obj_dict.keys():
    for s_key in sorted_subj_dict.keys():
        for r_key in sorted_rel_dict.keys():
            for obj_sent_ind in sorted_obj_dict[o_key][1]:
                for subj_sent_ind in sorted_subj_dict[s_key][1]:
                    for rel_sent_ind in sorted_rel_dict[r_key][1]:
                        if obj_sent_ind == subj_sent_ind & obj_sent_ind == rel_sent_ind:
                     
#                            print 'Sent_num = ' + sent_num_list[str(obj_sent_ind)] + ' ' + str(subj_list[subj_sent_ind]) + ' ' + str(rel_list[subj_sent_ind]) + ' ' + str(obj_list[obj_sent_ind])
#                            print 'Sentence ' + str(obj_sent_ind) + ' ' + str(subj_list[subj_sent_ind]) + ' ' + str(rel_list[subj_sent_ind]) + ' ' + str(obj_list[obj_sent_ind])
                            print 'Index = ' + str(obj_sent_ind) + ' ' + sentence_list[str(obj_sent_ind)]
                            s_ctr = s_ctr + 1
                            break
                    if (obj_sent_ind == subj_sent_ind & obj_sent_ind == rel_sent_ind) | (s_ctr > ctr_lim):                    
                        break
                if (obj_sent_ind == subj_sent_ind & obj_sent_ind == rel_sent_ind) | (s_ctr > ctr_lim):                    
                    break
            if (s_ctr > ctr_lim):                    
                break
        if (s_ctr > ctr_lim):                    
            break
#                    print 'Sentence ' + str(sorted_obj_dict[o_key][0]) + ' ' + str(obj_list[obj_sent_ind])

    if (s_ctr > ctr_lim):                    
        break  


print str(s_ctr)
