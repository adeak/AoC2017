from itertools import product
from collections import Counter

def day04(inp):
    OKs = 0
    for phrase in inp.rstrip().split('\n'):
        words = phrase.split()
        if len(words) == len(set(words)):
            OKs += 1
    return OKs

def day04b(inp):
    OKs = 0
    for phrase in inp.rstrip().split('\n'):
        words = phrase.split()
        if len(words) == len(set(words)):
            if all(Counter(word1)!=Counter(word2) for word1,word2 in product(words,repeat=2) if word1!=word2):
                OKs += 1
    return OKs


