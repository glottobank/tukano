tukano
======

Repository for computer-assisted reconstruction with Jena wordlist standard for Tukano language data.

News
====

I have now managed to conduct a first alignment analysis along with tokenization and the like for Tukano data. The results can soon be browsed via this weblink:

* http://tsv.lingpy.org/?css=database:show,&file=tukano

The tool which displays the results allows for online editing, provided the user has the password. Otherwise, editing is possible, but nothing will be stored in the database.
 

Steps I undertook are the following:

### Cleaning and IPA conversion

* replace spaces in input data with understroke _ (spaces are used as segment separator, cannot also be used as word separator)
* replace dashes (-) in data with some more general morpheme-boundary marker "◦" in order to prevent them from confusing the alignments. IN the future, I will probably switch to "Ø" or something similar as a gap-marker in alignments, but right now, "-" is the general gap marker, so "-" cannot be used to mark morpheme-bdoundaries and the like.
* modify nasalized words according to what was discussed (change voiced consonants to nasal counterparts)
* merge aspirated words by putting h to preceding consonant (shows some errors at the moment)
* merge [j] as a palatalization marker by putting it together with preceding consonant (can be improved, is not quite nice right now)

### Tokenization / phonological segmentation

The cleaned data wos segmentized phonologically using LingPy's basic functions. The results seem more or less OK, but few questions need to be solved. I have placed them under this link:

* https://github.com/glottobank/tukano/issues?q=Segmentation

### Alignment analysis

The current alignment analysis is by no means complete, but just an illustration of what is possible. In the near future, it is planned to include an alignment editor in the app, so it will then be possible to manually correct alignments.

## What are the next steps?

The next steps consist of data checking, and spurious error correction:

* checking the data and filing issues in the issue tracker, wherever things seem to be more systematic than spurious
* thinking about potential problems arising from specifics of the data in the future

The next concrete step will be to segmentize the proto-forms (otherwise, we can't do any nice analysis for comparison of reflexes and proto-forms). After this step, we make an initial analysis checking for potential borrowings, just to make sure enough reflexes are represented in all branches, and no really spurious cases might blurr our inferences. 


