# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-02-10 14:36
# modified : 2015-02-10 14:36
"""
<++>
"""

__author__="Johann-Mattis List"
__date__="2015-02-10"

from lingpyd import *
from lingpyd.plugins.lpserver.lexibase import LexiBase

tuk = LexiBase('tukano', dbase='triples.sqlite3',
    url="http://tsv.lingpy.org/triples/triples.sqlite3")


tuk.add_entries('context', 'alignment', lambda x: prosodic_string([y for y in x
    if y != '-']))

tuk.create('tukano')

burm = LexiBase('burmish', dbase='triples.sqlite3')
burm.add_entries('context', 'alignment', lambda x: prosodic_string([y for y in
    x if y != '-']))
burm.create('burmish')






