# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-10-16 12:19
# modified : 2014-10-16 12:19
"""
Initial script to check the Tukano data and modify and segmentize the entries.
"""

__author__="Johann-Mattis List"
__date__="2014-10-16"

import unicodedata as ucd
from lingpyd import *
from lingpyd.plugins.tukano import ipa2tokens

# load wordlist file
wl = Wordlist('../tsv/tukano_2014-10-16.tsv')


def makeIpa(seq):
    """
    function nasalizes a sequence according to certain rules:
    * "make all vowels following ~ to be nasalized"
    * "make all voiced sounds to become nasal sounds 
       b > m, d > n, g > ŋ , r > r̃ > , j > ɲ >,  w > w̃, 
    """

    # convert spaces to morphem boundary markers 
    seq = seq.replace(' ','_')
    seq = seq.replace('-','◦')

    breaks = '_◦'
    
    nmap = {
            "b" : "m",
            "d" : "n",
            "g" : "ŋ",
            "r" : "r̃",
            "j" : "ɲ",
            "w" : "w̃",
            "o" : "õ",
            "a" : "ã",
            "u" : "ũ",
            "e" : "ẽ",
            "ɨ" : "ɨ̃",
            "i" : "ĩ"
            }

    # set up set of basic vowels
    vowels = list('aeiouɨ')+[nmap[x] for x in 'aeiouɨ']

    # tokenize data
    tokens = ipa2tokens(seq, merge_vowels=False, merge_identical_symbols=True,
            semi_diacritics='∫hj', expand_nasals=False)
    
    # make lambda function that doesn't fail
    convert = lambda x: nmap[x] if x in nmap else x
    
    # iterate over all tokens:
    tchain = [t for t in tokens]
    nasal_environment = False
    out = []
    while tchain:
        
        # get next element
        char = tchain.pop(0)
        
        # determine nasal environment or not
        if nasal_environment:
            
            if char in nmap:
                out += [nmap[char]]

            elif char in breaks:
                nasal_environment = False
                out += [char]

            elif char == '~':
                nasal_environment = True
            else:
                out += [char]
        else:
            if char == '~':
                nasal_environment = True
            else:
                out += [char]

    return ' '.join(out)


# we assume that the above-outlined procedure works more or less, so we convert
# the data now to tokens
wl.add_entries('tokens', 'ipa', lambda x: makeIpa(x))


# check for unrecognized items
visited = []
count = 1
for k in wl:
    classes = tokens2class(wl[k,'tokens'], rc('sca'))
    for a,b in zip(classes,wl[k,'tokens']):
        if a == '0' and (a,b) not in visited:
            print(count,a,b, len(b))
            count += 1
            visited += [(a,b)]
input('go on?')
# temporary output
wl.output('tsv', filename='.tmp')

# load as alignment
alm = Alignments('.tmp.tsv')

alm.align(method='library')

alm.output('triples', filename='../triples/tukano')

        

