#!/usr/bin/env python
# -*- coding: utf-8 -*-

WORDLIST = 'temp.txt'
NW = 2
ND = 3

NP = 5

import random
import math
import os.path

assert os.path.exists(WORDLIST)
DIGITS = '0123456789'

with open(WORDLIST, 'r') as f:
    words = [x.strip() for x in f.readlines()]

def n_orders(x, y):
    '''Take the total number of permutations
    and cut off the permutations of x and y inside their sets'''
    return math.factorial(x + y) // math.factorial(x) // math.factorial(y)

def entropy():
    '''At least'''
    def log(n):
        return int(math.floor(math.log2(n)))
    # Remove the entropy lost for accept() funciont
    prob_nth_position = ND / (NW+ND)  # Probability to have a digit in the n^th position
    prob_digit_0 = (1 / len(DIGITS))  # Probability that the first digit is a 0
    invalid_prob = prob_nth_position * prob_digit_0 * prob_nth_position
    #              digit 1st pos     + it is 0      + digit in the 2nd position
    return log( len(words) ** NW * len(DIGITS) ** ND * n_orders(NW, ND) * (1 - invalid_prob) )

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

print('Entropy', entropy())

for _ in range(NP):
    print(gen())
