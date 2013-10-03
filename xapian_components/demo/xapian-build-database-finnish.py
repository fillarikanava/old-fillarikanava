#! /usr/bin/env python
# -*- coding: utf-8 -*- 
#
# Built upon example in 
# http://www.rkblog.rk.edu.pl/w/p/xapian-python/
#
#   9.2.2009 rk


import xapian
import string
import sys
import unicodedata
import re

if len(sys.argv) != 2:
    print "requires text data file name as argument!"
    exit (1)

MAX_PROB_TERM_LENGTH = 64

def p_alnum(c):
    return (c in string.ascii_letters or c in string.digits)

def p_notalnum(c):
    return not p_alnum(c)

def p_notplusminus(c):
    return c != '+' and c != '-'

def find_p(string, start, predicate):
    while start<len(string) and not predicate(string[start]):
        start += 1
    return start


database = xapian.WritableDatabase('test/', xapian.DB_CREATE_OR_OPEN)
stemmer = xapian.Stem("finnish")


DATA = open(sys.argv[1], 'r')

for line in DATA:

    para = re.sub(r'ä', 'a',line)
    para = re.sub(r'ö', 'o',para)

    doc = xapian.Document()
    doc.set_data(para)
    pos = 0
    i = 0
    while i < len(para):
	i = find_p(para, i, p_alnum)
	j = find_p(para, i, p_notalnum)
	k = find_p(para, j, p_notplusminus)
	if k == len(para) or not p_alnum(para[k]):
		j = k
	if (j - i) <= MAX_PROB_TERM_LENGTH and j > i:
		term = stemmer(string.lower(para[i:j]))
		doc.add_posting(term, pos)
		pos += 1
	i = j
    database.add_document(doc)
