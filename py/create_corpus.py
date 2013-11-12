#!/usr/bin/python

fd = open('../data/Book1.csv', 'r')
base_name = '../data/corpus_1/cp1_'

cntr = 1
for line in fd:
#    print line
    out_file_name = base_name + str(cntr) + '.txt'
    if line != '' and len(str(line)) > 10:
        fw = open(out_file_name, 'w')
        fw.write(line)
        fw.close()
        cntr = cntr + 1

fd.close()
