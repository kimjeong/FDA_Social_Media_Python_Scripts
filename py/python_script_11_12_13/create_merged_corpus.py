#!/usr/bin/python

fd = open('../data/Book1.csv', 'r')
base_name = '../data/corpus_1/cp1_'

cntr = 1
out_file_name = '../data/corpus_2/merged_corpus.txt'

fw = open(out_file_name, 'w')

for line in fd:
#    print line
    if line != '' and len(str(line)) > 10:
        fw.write(line)
        cntr = cntr + 1

fw.close()
fd.close()
