#!/usr/bin/env python
# -*- coding: utf-8 -*-

WORDLIST = 'mnemonic/wordlist/italian.txt'
NW = 2
ND = 3
NP = 5

# Possible orders for 2 words and 3 digits:
CM = 8

import random
import math
import os.path

assert os.path.exists(WORDLIST)
DIGITS = '0123456789'

with open(WORDLIST, 'r') as f:
    words = [x.strip() for x in f.readlines()]

def n_orders(nw, nd):
    '''nuober of possible orders'''
    return 8 if nw==2 and nd==3 else NotImplemented

def entropy():
    '''At least'''
    def log(n):
        return int(math.floor(math.log2(n)))
    return log( len(words) ** NW * len(DIGITS[1:]) ** ND * n_orders(NW, ND) )

def accept(passwd):
    for i in range(len(passwd)-1):
        if passwd[i] == DIGITS[0] and passwd[i+1] in DIGITS:
            return False
    return True

def gen():

    passwd = [random.choice(words) for _ in range(NW)]
    passwd.extend([random.choice(DIGITS) for _ in range(ND)])

    while True:
        random.shuffle(passwd)
        if accept(passwd):
            break

    for i in range(len(passwd)-1):
        def isword(w):
            return w not in DIGITS
        passwd[i] += '-' if isword(passwd[i]) and isword(passwd[i+1]) else ''
    return ''.join(passwd)

print('Entropy', '≥%d'%entropy())

for _ in range(NP):
    print(gen())
