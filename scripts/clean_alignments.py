# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-11-11 14:26
# modified : 2014-11-11 14:26
"""
Clean up stuff according to issues.
"""

__author__="Johann-Mattis List"
__date__="2014-11-11"

from lingpyd import *
from lingpyd.plugins.tukano import ipa2tokens

from lingpyd.plugins.burmish import Wordlist
wl = Wordlist('../triples/tukano.triples')


# add protoform as real language
protos = {}

# get all cognate ids and extract the relevant proto-form
for k in wl:

    cogid = wl[k,'cogid']
    pform = wl[k,'proto']
    if cogid in protos:
        pass
    else:
        protos[cogid] = pform
with open('tukano.tsv', 'w') as f:
    idx = 1
    this_cogid = ''
    header = [y.upper() for y in sorted(wl.header, key=lambda x:wl.header[x],
        )]
    f.write('ID' + '\t'+'\t'.join(header)+'\n')
    for k in wl:
        
        cogid = wl[k,'cogid']
        if this_cogid != cogid:
            
            new_line = len(header) * ['-']
            new_line[wl.header['cogid']] = cogid
            new_line[wl.header['doculect']] = '*PTK'
            new_line[wl.header['ipa']] = protos[cogid]
            tk = ipa2tokens(protos[cogid], expand_nasals = False)
            tk = ' '.join(tk[1:])
            new_line[wl.header['tokens']] = tk #' '.join(ipa2tokens(protos[cogid]))
            new_line[wl.header['alignment']] = tk
            new_line[wl.header['modified']] = 'TRUE'
            new_line[wl.header['concept']] = wl[k,'concept'] 

            f.write('\n#\n'+str(idx)+ '\t'+'\t'.join(new_line)+'\n')
            idx += 1
            this_cogid = cogid
        else:
            f.write(str(idx)+'\t'+'\t'.join(wl[k]) + '\n')
            idx += 1

wl = Wordlist('tukano.tsv')
wl.output('tsv', filename='tukano2', subset=True, cols =[h for h in
    sorted(wl.header) if h not in 'proto'], formatter='concept,doculect')

wl = Wordlist('tukano2.tsv')
mymodel = rc('sca')

# check for glottal stops important for issue #4
count = 1
alms = []
for k in wl:
    
    tokens = wl[k,'tokens']
    ipa = wl[k,'ipa']
    try:
        classes = tokens2class(tokens, mymodel)
    except:
        classes = tokens2class([t for t in tokens if t],mymodel)
    if 'ʔ' in tokens:

        idx = tokens.index('ʔ')
        if idx-1 != -1:
            pre = classes[idx-1]
        else:
            pre = '?'
        if idx+1 < len(classes):
            post = classes[idx+1]
        else:
            post = '?'
        
        # got for clean cases, search for v x v cases
        if pre in mymodel.vowels and post in mymodel.vowels:
            pass
        else:
            if pre in 'KCTPSMWRNJ':
                ntokens = tokens[:idx-1] + [tokens[idx-1]+tokens[idx]]+tokens[idx+1:]
                print(k,'PRE:', tokens, ntokens)
            elif post in 'KCTPSMRWNJ':
                ntokens = tokens[:idx] + [tokens[idx]+tokens[idx+1]] + tokens[idx+2:]
                print(k,'POST:', tokens, ntokens)
            else:
                ntokens = tokens
                input(tokens)
            wl[k][wl.header['tokens']] = ntokens

            # next step, store this for the alignments
            
            alms += [wl[k,'cogid']]

    elif 'ʔ' in ipa:
        print('!',k,ipa, wl[k,'tokens'])

wl._clean_cache()
# search for geminates and disentangle them
count = 1
for k in wl:

    tks = wl[k,'tokens']
    ntk = []
    for x in tks:
        if len(x) == 2:
            if x[0] == x[1]:
                ntk += [x[0],x[1]]
            elif x[0] in rc('vowels') and x[1] in rc('vowels'):
                ntk += [x[0],x[1]]
            else:
                ntk += [x]
        else:
            ntk += [x]
    wl[k][wl.header['tokens']] = ntk
wl._clean_cache()
for k in wl:
    
    # get tokens a second time
    tks = wl[k,'tokens']
    if tks[0] == '~j' or tks[0] == '~h':
        
        ntk = []
        while tks:
            nt = tks.pop(0)
            if nt == '~j':
                ntk += ['ɲ']
            elif nt == '~h':
                ntk += ['h']
            elif nt == 'b':
                ntk += ['m']
            elif nt == 'a':
                ntk += ['ã']
            elif nt == 'i':
                ntk += ['ĩ']
            elif nt == 'u':
                ntk += ['ũ']
            elif nt == 'ɨ':
                ntk += ['ɨ̃']
            elif nt == 'o':
                ntk += ['õ']
            elif nt == 'e':
                ntk += ['ẽ']
            else:
                ntk += [nt]
        wl[k][wl.header['tokens']] = ntk
        print(' '.join(ntk))
    elif '~' in ' '.join(tks):
        print(tks)

wl._clean_cache()

# now compare with alignments and extract those cases where we have differences
wl._clean_cache()
count = 1
modified = {}
for k in wl:

    tks = wl[k,'tokens']
    alm = wl[k,'alignment']
    alm_strip = ' '.join([x for x in alm if x not in '-()'])
    
    tks_strip = ' '.join(tks)

    if alm_strip != tks_strip:
        print(count, alm_strip, tks_strip)
        count += 1

        wl[k][wl.header['alignment']] = tks
        modified[k] = 'TRUE'
    else:
        modified[k] = 'FALSE'
    
    wl[k][wl.header['doculect']]
wl.add_entries('modified', modified, lambda x: x, force=True)

wl._clean_cache()


wl.update('/home/mattis/projects/scripts/burmish/dbase/triples.sqlite3', 'tukano')
