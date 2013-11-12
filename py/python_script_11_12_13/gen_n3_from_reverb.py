#!/opt/local/bin/python

import os
import sys
import glob
#import nltk
#from nltk.corpus import wordnet
#from nltk.corpus import brown
import enchant


def remove_repeat_ttl(output_ttl):

  output_tmp = output_ttl + 'tmp'
  output_hand = open(output_ttl, 'r')
  output_tmp_hand = open(output_tmp, 'w')

  hash_out = {}
  wr_line_ar = []
  for output_line in output_hand:
    if (output_line[0] == ':'):
      if (output_line.replace('_','').replace(':','').replace(';','').strip().lower() in hash_out):
        for output_line in output_hand:
          if (output_line[0] == ':') & (output_line.replace('_','').replace(':','').replace(';','').strip().lower() not in hash_out):
            break
      hash_out[output_line.replace(':','').replace('_','').replace(';','').strip().lower()] = True

    output_tmp_hand.write(output_line.replace('.',''))
    
  output_hand.close()
  output_tmp_hand.close()

  os_str = 'cp -f ' + output_tmp + ' ' + output_ttl
  os.system(os_str)

def add_end_marks_ttl(output_ttl):

  output_tmp = output_ttl + 'tmp'
  output_hand = open(output_ttl, 'r')
  output_tmp_hand = open(output_tmp, 'w')

  hash_out = {}
  wr_line_ar = []
  for output_line in output_hand:
    if (output_line[0] == ':'):
      output_tmp_hand.write(output_line)
      for output_line in output_hand:
        cur_line = output_line
        for next_line in output_hand:
          if (next_line == '\n'):
            output_tmp_hand.write(cur_line.rstrip('\n') + '.\n\n')
            break
          else:
            output_tmp_hand.write(cur_line.rstrip('\n') + ';\n')
          cur_line = next_line
        break
    
  output_hand.close()
  output_tmp_hand.close()

  os_str = 'cp -f ' + output_tmp + ' ' + output_ttl
  os.system(os_str)

def add_morning_report_token(output_ttl):
  
  output_tmp = output_ttl + 'tmp'
  output_hand = open(output_ttl, 'r')
  output_tmp_hand = open(output_tmp, 'w')

  hash_out = {}
  wr_line_ar = []
  consume_line = True
  for output_line in output_hand:
    wr_line_ar = []
    if (output_line[0] == '\n'):
      consume_line = False
      continue
    else:
      wr_line_ar.append(output_line)
      for next_line in output_hand:
        if next_line[0] == '\n':
          consume_line = True
          break
        else:
          wr_line_ar.append(next_line)
          token_flag = False
          if 'token' in next_line:
            token_flag = True

    if (consume_line):
      output_tmp_hand.write('\n')
      wr_line_cnt = 0
      for wr_line in wr_line_ar:
#        if (wr_line_cnt == 1) & (token_flag == True):
        if (wr_line_cnt == 1):
#          output_tmp_hand.write('\trdf:type :MorningReportToken;\n')
          output_tmp_hand.write('\trdf:type :MORNING_REPORT_TOKEN;\n')
        output_tmp_hand.write(wr_line)
        wr_line_cnt = wr_line_cnt + 1
#      output_tmp_hand.write('\n')
      consume_line = False
    
  output_hand.close()
  output_tmp_hand.close()

  os_str = 'cp -f ' + output_tmp + ' ' + output_ttl
  os.system(os_str)
  

def organize_2token(output_hand, subj_ar, predicate_ar, r_subj_str, r_predicate_str):

  subj_label = ' '.join(subj_ar)
  predicate_label = ' '.join(predicate_ar)

  output_hand.write('\n')
  r_out_str1 = ':' + r_subj_str.upper() + '\n'
  output_hand.write(r_out_str1)
  r_out_str2 = '\trdfs:label \"' + subj_label.title() + '\"^^:string\n'
  output_hand.write(r_out_str2)
  r_out_str3 = '\trdfs:token \"' + subj_label.lower() + '\"^^:string\n'
  output_hand.write(r_out_str3)

  output_hand.write('\n')
  r_out_str1 = ':' + r_predicate_str.upper() + '\n'
  output_hand.write(r_out_str1)
  r_out_str2 = '\trdfs:label \"' + predicate_label.title() + '\"^^:string\n'
  output_hand.write(r_out_str2)
  r_out_str3 = '\trdfs:token \"' + predicate_label.lower() + '\"^^:string\n'
  output_hand.write(r_out_str3)
  output_hand.write('\n')

def organize_3token(output_hand, subj_ar, predicate_ar, obj_ar, r_subj_str, r_predicate_str, r_obj_str):

  subj_pred_label = ' '.join(subj_ar) + ' ' + ' '.join(predicate_ar)
  subj_obj_label = ' '.join(subj_ar) + ' ' + ' '.join(obj_ar)
  subj_label = ' '.join(subj_ar)
  predicate_label = ' '.join(predicate_ar)
  obj_label = ' '.join(obj_ar)
  
  output_hand.write('\n')
 # r_out_str1 = ':' + r_subj_str + r_predicate_str + '\n'
  if r_predicate_str.upper() != '':
    r_out_str1 = ':' + r_subj_str.upper() + '_' + r_predicate_str.upper() + '\n'
  else:
    r_out_str1 = ':' + r_subj_str.upper() + '\n'
  output_hand.write(r_out_str1)
  r_out_str2 = '\trdfs:label \"' + subj_pred_label.title() + '\"^^:string\n'
  output_hand.write(r_out_str2)
  r_out_str3 = '\t:hasChild :' + r_subj_str + '\n'
  output_hand.write(r_out_str3)
  r_out_str3 = '\t:hasChild :' + r_predicate_str + '\n'
  output_hand.write(r_out_str3)

  output_hand.write('\n')
#  r_out_str1 = ':' + r_subj_str + r_obj_str + '\n'
  if r_obj_str.upper() != '':
    r_out_str1 = ':' + r_subj_str.upper() + '_' + r_obj_str.upper() + '\n'
  else:
    r_out_str1 = ':' + r_subj_str.upper() + '\n'
  output_hand.write(r_out_str1)
  r_out_str2 = '\trdfs:label \"' + subj_obj_label.title() + '\"^^:string\n'
  output_hand.write(r_out_str2)
  r_out_str3 = '\t:hasChild :' + r_subj_str + '\n'
  output_hand.write(r_out_str3)
  r_out_str3 = '\t:hasChild :' + r_obj_str + '\n'
  output_hand.write(r_out_str3)

  output_hand.write('\n')
#  r_out_str1 = ':' + r_subj_str + '\n'
  r_out_str1 = ':' + r_subj_str.upper() + '\n'
  output_hand.write(r_out_str1)
  r_out_str2 = '\trdfs:label \"' + subj_label.title() + '\"^^:string\n'
  output_hand.write(r_out_str2)
  r_out_str3 = '\trdfs:token \"' + subj_label.lower() + '\"^^:string\n'
  output_hand.write(r_out_str3)

  output_hand.write('\n')
#  r_out_str1 = ':' + r_predicate_str + '\n'
  r_out_str1 = ':' + r_predicate_str.upper() + '\n'
  output_hand.write(r_out_str1)
  r_out_str2 = '\trdfs:label \"' + predicate_label.title() + '\"^^:string\n'
  output_hand.write(r_out_str2)
  r_out_str3 = '\trdfs:token \"' + predicate_label.lower() + '\"^^:string\n'
  output_hand.write(r_out_str3)

  output_hand.write('\n')
#  r_out_str1 = ':' + r_obj_str + '\n'
  r_out_str1 = ':' + r_obj_str.upper() + '\n'
  output_hand.write(r_out_str1)
  r_out_str2 = '\trdfs:label \"' + obj_label.title() + '\"^^:string\n'
  output_hand.write(r_out_str2)
  r_out_str3 = '\trdfs:token \"' + obj_label.lower() + '\"^^:string\n'
  output_hand.write(r_out_str3)
  output_hand.write('\n')


def decompose_term(output_hand, term_ar, tf_idf_hash, token_hash):

  l_non_hash_ar = []
  c_non_hash_ar = []
  for term in term_ar:
    if (term in tf_idf_hash) | (term in token_hash):
      hash_term = term
    else:
      l_non_hash_ar.append(term)
#      c_non_hash_ar.append(term.title())
      c_non_hash_ar.append(term.upper())

  if (len(l_non_hash_ar) > 0) & (len(c_non_hash_ar) > 0):
#    r_out1 = ':' + ''.join(c_non_hash_ar) + '\n'
    r_out1 = ':' + '_'.join(c_non_hash_ar) + '\n'
    output_hand.write(r_out1)
    tmp_l_non_hash_str = ' '.join(l_non_hash_ar)
    r_out2 = '\trdfs:label ' + '\"' + tmp_l_non_hash_str.title() +  '\"^^:string\n'
    output_hand.write(r_out2)
    r_out3 = '\trdfs:token ' + '\"' + ' '.join(l_non_hash_ar) +  '\"^^:string\n\n'
    output_hand.write(r_out3)

  if hash_term.strip() != '':
#    r_out1 = ':' + hash_term.title() + '\n'
    r_out1 = ':' + hash_term.upper() + '\n'
    output_hand.write(r_out1)
    r_out2 = '\trdfs:label ' + '\"' + hash_term.strip().title() +  '\"^^:string\n'
    output_hand.write(r_out2)
    r_out3 = '\trdfs:token ' + '\"' + hash_term.strip() +  '\"^^:string\n\n'
    output_hand.write(r_out3)

def gen_ttl_entry(output_hand, subj_ar, predicate_ar, obj_ar, tf_idf_hash, token_hash, num_childs):

  r_subj_str = ''
  l_subj_str = ''
  subj_match = False
  for subj in subj_ar:
    if (subj in tf_idf_hash) | (subj in token_hash):
      subj_match = True
    r_subj_str = r_subj_str + subj.title().strip()
#    l_subj_str = l_subj_str + subj.strip()
  l_subj_str = ' '.join(subj_ar)

  r_predicate_str = ''
  l_predicate_str = ''
  predicate_match = False
  for predicate in predicate_ar:
    if (predicate in tf_idf_hash) | (predicate in token_hash):
      predicate_match = True
    r_predicate_str = r_predicate_str + predicate.title().strip()
#    l_predicate_str = l_predicate_str + predicate.strip()
  l_predicate_str = ' '.join(predicate_ar)

  r_obj_str = ''
  l_obj_str = ''
  obj_match = False
  for obj in obj_ar:
    if (obj in tf_idf_hash) | (obj in token_hash):
      obj_match = True
    r_obj_str = r_obj_str + obj.title().strip()
    l_obj_str = l_obj_str + obj.strip()
  l_obj_str = ' '.join(obj_ar)
    
  if(subj_match): 
    decompose_term(output_hand, subj_ar, tf_idf_hash, token_hash)
  elif(predicate_match):
    decompose_term(output_hand, predicate_ar, tf_idf_hash, token_hash)
  elif(obj_match):
    decompose_term(output_hand, obj_ar, tf_idf_hash, token_hash)


  if(num_childs == 2):
#    r_out1 = ':' + r_subj_str + r_predicate_str + r_obj_str + '\n'
    if (r_predicate_str.upper() != '') & (r_obj_str.upper() != ''):
      r_out1 = ':' + r_subj_str.upper() + '_' + r_predicate_str.upper() + '_' + r_obj_str.upper() + '\n'
    elif (r_predicate_str.upper() != ''):
      r_out1 = ':' + r_subj_str.upper() + '_' + r_predicate_str.upper() + '\n'
    else:
      r_out1 = ':' + r_subj_str.upper() + '\n'
    output_hand.write(r_out1)
    r_out2 = '\trdfs:label ' + '\"' + l_subj_str.title() + ' ' + l_predicate_str.title() + ' ' + l_obj_str.title() + '\"^^:string\n'
    output_hand.write(r_out2)
    r_out3 = '\t:hasChild :' + r_subj_str + r_predicate_str + ', :' + r_subj_str + r_obj_str + '\n'
    output_hand.write(r_out3)
    if(subj_match | predicate_match | obj_match):
      organize_3token(output_hand, subj_ar, predicate_ar, obj_ar, r_subj_str, r_predicate_str, r_obj_str)
  elif(num_childs == 1):
#    r_out1 = ':' + r_subj_str + r_predicate_str + r_obj_str + '\n'
    if (r_predicate_str.upper() != '') & (r_obj_str.upper() != ''):
      r_out1 = ':' + r_subj_str.upper() + '_' + r_predicate_str.upper() + '_' + r_obj_str.upper() + '\n'
    elif (r_predicate_str.upper() != ''):
      r_out1 = ':' + r_subj_str.upper() + '_' + r_predicate_str.upper() + '\n'
    else:
      r_out1 = ':' + r_subj_str.upper() + '\n'
    output_hand.write(r_out1)
    if l_obj_str.strip() != '':
      r_out2 = '\trdfs:label ' + '\"' + l_subj_str.title() + ' ' + l_predicate_str.title() + ' ' + l_obj_str.title() + '\"^^:string\n'
      output_hand.write(r_out2)
      r_out3 = '\trdfs:token ' + '\"' + l_subj_str + ' ' + l_predicate_str + ' ' + l_obj_str + '\"^^:string\n\n'
      output_hand.write(r_out3)
    else:
      r_out2 = '\trdfs:label ' + '\"' + l_subj_str.title() + ' ' + l_predicate_str.title() + '\"^^:string\n'
      output_hand.write(r_out2)
      r_out3 = '\trdfs:token ' + '\"' + l_subj_str + ' ' + l_predicate_str +  '\"^^:string\n\n'
      output_hand.write(r_out3)
    if(subj_match | predicate_match | obj_match):
      organize_2token(output_hand, subj_ar, predicate_ar, r_subj_str, r_predicate_str)
#    r_out3 = '\t:hasChild :' + r_subj_str + r_predicate_str + '.\n'
#    output_hand.write(r_out3)
  else:
    if (r_subj_str != '') & (r_predicate_str != ''):
#      r_out1 = ':' + r_subj_str + r_predicate_str + r_obj_str + '\n'
      r_out1 = ':' + r_subj_str.upper() + '_' + r_predicate_str.upper() + '_' + r_obj_str.upper + '\n'
      output_hand.write(r_out1)
      if l_obj_str == '':
        r_out2 = '\trdfs:label ' + '\"' + l_subj_str.title() + ' ' + l_predicate_str.title() + '\"^^:string\n'
        output_hand.write(r_out2)
        r_out3 = '\trdfs:token ' + '\"' + l_subj_str + ' ' + l_predicate_str +  '\"^^:string\n\n'
        output_hand.write(r_out3)
      else:
        r_out2 = '\trdfs:label ' + '\"' + l_subj_str.title() + ' ' + l_predicate_str.title() + ' ' + l_obj_str.title() + '\"^^:string\n'
        output_hand.write(r_out2)
        r_out3 = '\trdfs:token ' + '\"' + l_subj_str + ' ' + l_predicate_str + ' ' + l_obj_str + '\"^^:string\n\n'
        output_hand.write(r_out3)

  
  output_hand.write('\n')

  return

def get_stuck_pipe_token(file_hand, token_hash):

  for file_line in file_hand:
    if 'rdfs:token' in file_line:
      try:
        line_sp = file_line.split('\"')
        token_hash[line_sp[1]] = True
      except:
        continue

def remove_repeats_tf_idf(tf_idf_hash, token_hash):

  for key in tf_idf_hash.keys():
    if key in token_hash:
      tf_idf_hash.pop(key)
  

def gen_term_ar(pos_sp, reverb_line_sp, pos_hash, term_index, start_index, end_index, closed_hash, dict):

  term_sp = reverb_line_sp[term_index].split(' ')
  term_cnt = 0
  eng_cnt = 0
  term_ar = []
  pos_index = range((int(reverb_line_sp[start_index])),(int(reverb_line_sp[end_index])))

  for term in term_sp:
    term_cnt = term_cnt + 1
# check if English term, else continue

    try:
      if not dict.check(term.strip()):
        continue
    except:
      continue
# get start_index -> end_index-1 in reverb_line_sp, if in pos_hash, append term to subj_ar, else continue
#    print str(pos_index[term_cnt-1])
    try:
      if (pos_hash[pos_sp[pos_index[term_cnt-1]]] == 'true') & (term.strip() not in closed_hash):
#      if pos_hash[pos_sp[pos_index[term_cnt-1]]] == 'true':
#        term_ar.append(term.strip().replace('\'','\\\''))
        term_ar.append(term.strip().replace('\'',''))
      else:
        continue
    except:
      continue
    eng_cnt = eng_cnt + 1
# calculate number of English term/total number of terms
  term_ratio = float(eng_cnt/term_cnt)
# if term_ratio is > English_word_perc, keep the terms in subj_ar, else reject
  if term_ratio > English_word_perc:
    return term_ar, term_ratio
  else:
    return [], term_ratio

if __name__ == '__main__':

  if len(sys.argv) != 9:
    print 'Usage: gen_ttl_from_reverb.py reverb_output.txt output.ttl pos_map.txt tf_idf.txt stuck_pipe.ttl closed_verbs.txt correct_perc English_word_perc'
    sys.exit(1)

  reverb_output = sys.argv[1]
  output_ttl = sys.argv[2]
  pos_map = sys.argv[3]
  tf_idf_file = sys.argv[4]
  stuck_pipe_file = sys.argv[5]
  closed_verb_file = sys.argv[6]
  correct_perc = float(sys.argv[7])
  English_word_perc = float(sys.argv[8])

  output_hand = open(output_ttl, 'w')
  pos_map_hand = open(pos_map, 'r')
  reverb_out_hand = open(reverb_output, 'r')
  closed_verb_hand = open(closed_verb_file, 'r')

  output_hand.write('\n\n')
  dict = enchant.Dict('en_US')
# read in pos hash map
  pos_hash = {}
  for pos_line in pos_map_hand:
    pos_line_sp = pos_line.split(' ')
    try:
      pos_hash[pos_line_sp[0].strip()] = pos_line_sp[1].strip()
    except:
      continue

# close pos_map_hand
  pos_map_hand.close()

# read in closed hash map
  closed_hash = {}
  for closed_line in closed_verb_hand:
    try:
      closed_hash[closed_line.strip()] = True
    except:
      continue

# close closed_verb_hand
  closed_verb_hand.close()

# place tf_idf terms in hash
  tf_idf_hash = {}
  tf_idf_hand = open(tf_idf_file, 'r')
  for line in tf_idf_hand:
    tf_idf_sp = line.split(' ')
    try:
      tf_idf_hash[tf_idf_sp[0].lower().strip()] = True
    except:
      continue
  tf_idf_hand.close()
  
# get all the tokens from stuck_pipe file
  token_hash = {}
  stuck_pipe_hand = open(stuck_pipe_file, 'r')
  get_stuck_pipe_token(stuck_pipe_hand, token_hash)
  stuck_pipe_hand.close()

  remove_repeats_tf_idf(tf_idf_hash, token_hash)

# for every line in the reverb output
  for reverb_line in reverb_out_hand:

# split by tabs, array is zero based, and [n] means nth element in array
    reverb_line_sp = reverb_line.split('\t')

#    print(str(reverb_line_sp))
# check if [11] is < correct_perc continue
    if(float(reverb_line_sp[11]) < correct_perc):
      continue

# split the pos by space
    pos_sp = reverb_line_sp[13].split(' ')

# for subj split [15] by space, and for every term in [15]
# get [5] -> [6]-1 in [13], if in pos_hash, use [15], append to subj_ar
    subj_ar, subj_ratio = gen_term_ar(pos_sp, reverb_line_sp, pos_hash, 15, 5, 6, closed_hash, dict)

# for predicate split [16] by space, and for every term in [16]
# get [7] -> [8]-1 in [13], if in pos_hash use [16], append to predicate_ar
    predicate_ar, predicate_ratio = gen_term_ar(pos_sp, reverb_line_sp, pos_hash, 16, 7, 8, closed_hash, dict)
#    for pred in predicate_ar:
#      if 'be' in pred:
#        predicate_ratio = 0.0

# for obj split [17] by space, and for every term in [17]
# get [9] -> [10]-1 in [13], if in pos_hash use [17], append to obj_ar
#    print reverb_line_sp[9] + ' ' + reverb_line_sp[10]
    obj_ar, obj_ratio = gen_term_ar(pos_sp, reverb_line_sp, pos_hash, 17, 9, 10, closed_hash, dict)

#    print str(subj_ar) +'\n'
#    print str(predicate_ar) +'\n'
#    print str(obj_ar) +'\n'

# if subj_ratio > English_word_perc && predicate_ratio > English_word_perc && obj_ratio > English_word_perc, append ttl w/ 2 childs
    if ((subj_ratio > English_word_perc) & (predicate_ratio > English_word_perc) & (obj_ratio > English_word_perc)):
      gen_ttl_entry(output_hand, subj_ar, predicate_ar, obj_ar, tf_idf_hash, token_hash, 2)

# if subj_ratio > English_word_perc && predicate_ratio > English_word_perc && obj_ratio < English_word_perc, append ttl w/ 1 childs
    elif((subj_ratio > English_word_perc) & (predicate_ratio > English_word_perc) & (obj_ratio < English_word_perc)):
      gen_ttl_entry(output_hand, subj_ar, predicate_ar, obj_ar, tf_idf_hash, token_hash, 1)

# if subj_ratio > English_word_perc && predicate_ratio < English_word_perc, append ttl w/ 0 childs
    elif ((subj_ratio > English_word_perc) & (predicate_ratio < English_word_perc)):
      gen_ttl_entry(output_hand, subj_ar, predicate_ar, obj_ar, tf_idf_hash, token_hash, 0)


# close reverb_output, output_ttl
  reverb_out_hand.close()
  output_hand.close()


  remove_repeat_ttl(output_ttl)
  add_end_marks_ttl(output_ttl)
  add_morning_report_token(output_ttl)
