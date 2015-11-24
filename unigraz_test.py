#!/usr/bin/env python

g=set([x.strip() for x in open('unigraz-comp.txt').readlines()])
f=set([x.strip() for x in open('unigraz-comp-filtering.txt').readlines()])

if f-g:
    print(f-g)
