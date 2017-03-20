#!/usr/bin/env python
import sys
fn = sys.argv[1]
inputf = open(fn, 'r')
outputf = open('noc_'+fn, 'w')

cmmode = False
lcmmode = False
emptylinemode = False

for line in inputf:
    line1 = line.strip()
    if line1 == "\\begin{comment}":
        cmmode = True
        continue
    if line1 == "\\end{comment}":
        cmmode = False
        #print 'comment block\n'
        continue
    if not line1.startswith('%') and cmmode is False:
        lcmmode = False
        if '%' in line1:
            print line1
        for ch in line1:
            if lcmmode is False and ch == '%':
                print 'in-line comment\n'
                break
            if lcmmode is True:
                lcmmode = False
            if ch == '\\':
                lcmmode = True
            outputf.write(ch)
        if line1 == '' and emptylinemode is True:
            pass
        else:
            outputf.write('\n')
        if line1 != '':
            emptylinemode = False
        else:
            emptylinemode = True

    else:
        pass
        #print 'one line comment\n'
