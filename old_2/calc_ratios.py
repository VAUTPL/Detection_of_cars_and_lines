#! /bin/hbpython
f1 = open('stat.tsv', 'r')
f2 = open('stat2.tsv', 'w')
for line in f1:
    f2.write('%s\t%f\n' % (line, ))
