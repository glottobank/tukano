# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-10-16 13:08
# modified : 2014-10-16 13:08
"""
Convert current triple store into an sqlite database.
"""

__author__="Johann-Mattis List"
__date__="2014-10-16"

from lingpyd.plugins.burmish import Wordlist

wl = Wordlist('../triples/tukano.triples')

wl.update('../triples/triples.sqlite3', 'tukano')

