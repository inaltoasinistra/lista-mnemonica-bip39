#!/usr/bin/env python
#
# Copyright (c) 2013 Pavol Rusnak
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

# Copy https://github.com/trezor/python-mnemonic/mnemonic into .
# Copy wordlists from: https://github.com/bitcoin/bips/tree/master/bip-0039/*.txt to wordlist/

from __future__ import print_function

import json
import random
import sys
import os
import unittest
from binascii import hexlify, unhexlify
from functools import reduce

from mnemonic import Mnemonic

class MnemonicTest(unittest.TestCase):

    itapath = '%s/%s.txt' % ('.', 'italian')

    def test_similarity(self):
        similar = (
            ('a', 'c'), ('a', 'e'), ('a', 'o'),
            ('b', 'd'), ('b', 'h'), ('b', 'p'), ('b', 'q'), ('b', 'r'),
            ('c', 'e'), ('c', 'g'), ('c', 'n'), ('c', 'o'), ('c', 'q'), ('c', 'u'),
            ('d', 'g'), ('d', 'h'), ('d', 'o'), ('d', 'p'), ('d', 'q'),
            ('e', 'f'), ('e', 'o'),
            ('f', 'i'), ('f', 'j'), ('f', 'l'), ('f', 'p'), ('f', 't'),
            ('g', 'j'), ('g', 'o'), ('g', 'p'), ('g', 'q'), ('g', 'y'),
            ('h', 'k'), ('h', 'l'), ('h', 'm'), ('h', 'n'), ('h', 'r'),
            ('i', 'j'), ('i', 'l'), ('i', 't'), ('i', 'y'),
            ('j', 'l'), ('j', 'p'), ('j', 'q'), ('j', 'y'),
            ('k', 'x'),
            ('l', 't'),
            ('m', 'n'), ('m', 'w'),
            ('n', 'u'), ('n', 'z'),
            ('o', 'p'), ('o', 'q'), ('o', 'u'), ('o', 'v'),
            ('p', 'q'), ('p', 'r'),
            ('q', 'y'),
            ('s', 'z'),
            ('u', 'v'), ('u', 'w'), ('u', 'y'),
            ('v', 'w'), ('v', 'y')
        )

        # fix len
        with open(self.itapath, 'r') as f:
            wl = [w.strip() for w in f.readlines()]

        wl += [str(x) for x in range(2048-len(wl))]

        # cut off the longest words
        wl.sort(key=lambda x: len(x))
        with open('%s/%s.txt' % ('./mnemonic/wordlist', 'test'), 'w') as f:
            f.writelines([x+'\n' for x in wl[:2048]])
        
        languages = ['test'] # Mnemonic.list_languages()

        fail = False
        for lang in languages:
            mnemo = Mnemonic(lang)

            for w1 in mnemo.wordlist:
                for w2 in mnemo.wordlist:
                    if len(w1) != len(w2):
                        continue

                    if w1 == w2:
                        continue

                    if w1 > w2:
                        # No need to print warning twice
                        continue

                    diff = []
                    for i in range(len(w1)):
                        if w1[i] != w2[i]:
                            if w1[i] < w2[i]:
                                pair = (w1[i], w2[i])
                            else:
                                pair = (w2[i], w1[i])

                            diff.append(pair)
                            # pairs.update((pair,))

                    if len(diff) == 1:
                        if list(diff)[0] in similar:
                            fail = True
                            print("Similar words (%s): %s, %s" % (lang, w1, w2))

        if fail:
            self.fail("Similar words found")

    def test_getinfo(self):
        with open(self.itapath, 'r') as f:
            wl = [w.strip() for w in f.readlines()]

        wl.sort(key=lambda x: len(x))
        print('Avg len: %.2f'%(sum([len(x) for x in wl[:2048]])/len(wl[:2048])))
        print('Words to exclude:',' '.join(wl[2048:][::-1]))

    def test_len_histogram(self):
        with open(self.itapath, 'r') as f:
            wl = [w.strip() for w in f.readlines()]

        h = {}
        for w in wl:
            c = h.get(len(w),0)
            h[len(w)] = c+1
        print()
        print('%10s%10s%10s'%('len(w)','freq(w)','cumul'))
        cumul = 0
        for k in sorted(h):
            cumul += h[k]
            print('%10d%10d%10d'%(k,h[k],cumul))

    def test_other_wordlist_comp(self):
        with open(self.itapath, 'r') as f:
            ws = set([w.strip() for w in f.readlines()])
        res = {}
        for fn in os.listdir('wordlist'):
            if fn[:-4] in ['spanish']:
                continue
            with open(os.path.join('wordlist',fn)) as f:
                foreign = set([x.strip() for x in f.readlines()])
            # Look for intersections
            res[fn] = ws & foreign
        # print stats
        for fn in res:
            if len(res[fn]):
                print(fn,len(res[fn]),res[fn])

        cumul = reduce(lambda x,y: x|y,res.values())
        if cumul:
            # suggest a compatible list
            with open('test-suggested-list.txt','w') as f:
                f.writelines(sorted([x+'\n' for x in ws if x not in cumul],key=lambda x: len(x)))
        self.assertFalse( cumul )
            
def __main__():
    unittest.main()
if __name__ == "__main__":
    __main__()
