# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-11-14 06:39
# modified : 2014-11-14 06:39
"""
Script reintroduces SIO which was left out in compuatation before.
"""

__author__="Johann-Mattis List"
__date__="2014-11-14"

from lingpyd import *
from lingpyd.plugins.tukano import ipa2tokens

from lingpyd.plugins.burmish import Wordlist

converter = {
        "BAS":("Barasano"    , "bsn"),
        "DES":("Desano"      , "des"),
        "KAR":("Karapana"    , "cbc"),
        "KOR":("Koreguahe"   , "coe"),
        "KUB":("Kubeo"       , "cub"),
        "KUE":("Kueretu"     , "???"),
        "MAI":("Maihɨki"     , "ore"),
        "PIR":("Pirá-Tapuya" , "pir"),
        "PIS":("Pisamira"    , "???"),
        "SEK":("Sekoya"      , "sey"),
        "SIO":("Siona"       , "snn"),
        "TAN":("Tanimuka"    , "tnc"),
        "TUK":("Tukano"      , "tuo"),
        "TUY":("Tuyuka"      , "tue"),
        "WAN":("Wanano"      , "gvc"),
        "YAH":("Yahuna"      , "ynu"),
        "YUP":("Yupua"       , "???"),
        "YUR":("Yuruti"      , "yui"),
        "*PT":("Proto-Tukano",'???')
    }
wl1 = Wordlist('../triples/tukano.triples')
wl2 = Wordlist('../triples/tukano.bak-2014-11-14.triples')

# retrieve all entries for SIO via cogid
D1 = {}
header = sorted(wl2.header, key=lambda y:wl2.header[y])
for k in wl2:

    taxon = wl2[k,'taxon']
    D1[taxon,wl2[k,'cogid']] = dict(zip(header,wl2[k]))

# retrieve current etnries via cogid
D2 = {}
header = sorted(wl1.header, key=lambda y:wl1.header[y])
for k in wl1:

    taxon = wl1[k,'taxon']
    D2[taxon,wl1[k,'cogid']] = dict(zip(header,wl1[k]))

# get all cogids
cogids = sorted(wl2.get_etymdict(ref='cogid'), key=lambda x:int(x))

with open('tukano.patch.tsv', 'w') as f:

    idx = 1

    this_cogid = ''
    header = [y.upper() for y in sorted(wl1.header, key=lambda x:
        wl1.header[x])]

    f.write('ID'+'\t'+'\t'.join(header)+'\n')
    
    for cogid in cogids:

        for taxon in sorted(wl2.taxa):

            if (taxon,cogid) in D2 or (taxon,cogid) in D1:
                new_line = len(header) * ['-']

                for i in range(len(new_line)):
                    try:
                        new_line[i] = D2[(taxon,cogid)][header[i].lower()]
                    except KeyError:
                        try:
                            new_line[i] = D1[(taxon,cogid)][header[i].lower()]
                        except KeyError:
                            pass
                if len(new_line) > new_line.count('-'):
                    f.write(str(idx)+'\t'+'\t'.join(new_line)+'\n')
                    idx += 1
                    print(new_line)

        proto = len(header) * ['-']
        for i in range(len(proto)):
            try:
                proto[i] = D2[('*PT',cogid)][header[i].lower()]
            except KeyError:
                pass
        print(cogid)
        f.write(str(idx) + '\t' + '\t'.join(proto)+'\n')
        idx += 1
      
wl = Wordlist('tukano.patch.tsv')
wl.update('../../burmish/dbase/triples.sqlite3','tukano')
      
      
      
      
      
      
      
      
      
      
      
      
