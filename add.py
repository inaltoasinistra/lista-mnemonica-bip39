#!/usr/bin/env python

import sys
import os

def other_lists_info(wl):
    ws = set(wl)
    cumul = set()
    for fn in os.listdir('wordlist'):
        with open(os.path.join('wordlist',fn)) as f:
            foreign = set([x.strip() for x in f.readlines()])
        # Look for intersections
        i = ws & foreign
        print(fn,len(i))
        cumul.update(i)
    if cumul:
        with open('valid-no-intersect.txt','w') as f:
            f.writelines([x+'\n' for x in wl if x not in cumul])


if not sys.argv[1:]:
    words = [x.strip() for x in sys.stdin.read().split()]
else:
    words = [sys.argv[1]]
with open('%s/%s.txt' % ('./mnemonic/wordlist', 'italian'), 'r') as f:
    wl = [w.strip() for w in f.readlines()]

valid = []
for n in words:
    four = [x for x in wl+valid if x[:4]==n[:4]]
    if four:
        print('Word',n,'not valid:',four)
    else:
        valid.append(n)
        print('Word',n,'is valid, test similarity')

if valid:
    with open('valid.txt','w') as f:
        f.writelines([x+'\n' for x in valid])

    other_lists_info(valid)
