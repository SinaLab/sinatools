# This code was taken from Camel tools without any change

# -*- coding: utf-8 -*-


import re
from nlptools.morphology.charsets import UNICODE_PUNCT_SYMBOL_CHARSET
from nlptools.morphology.charsets import UNICODE_LETTER_MARK_NUMBER_CHARSET


_ALL_PUNCT = u''.join(UNICODE_PUNCT_SYMBOL_CHARSET)
_ALL_LETTER_MARK_NUMBER = u''.join(UNICODE_LETTER_MARK_NUMBER_CHARSET)
_TOKENIZE_RE = re.compile(r'[' + re.escape(_ALL_PUNCT) + r']|[' +
                          re.escape(_ALL_LETTER_MARK_NUMBER) + r']+')


def simple_word_tokenize(sentence):

    return _TOKENIZE_RE.findall(sentence)
