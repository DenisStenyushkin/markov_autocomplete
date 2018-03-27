#!/usr/bin/env python

""" Trains MarkovAutocompleteProvider's model and dumps it to a file """

from nltk.corpus import gutenberg
from MarkovAutocompleteProvider import MarkovAutocompleteProvider
from tokeniser import tokenize

def corpus():
    for file_name in gutenberg.fileids():
        print("Yielding text: {f}".format(f=file_name))
        yield gutenberg.raw(file_name)

provider = MarkovAutocompleteProvider()
provider.fit(corpus(), tokenize)
provider.save()
