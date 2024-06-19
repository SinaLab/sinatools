# -*- coding: utf-8 -*-
# We acknoledge that this file  charsets.py is imported from Camel tools citation. url
#

import unicodedata

from six import unichr


UNICODE_PUNCT_CHARSET = frozenset(
    [unichr(x) for x in range(65536) if unicodedata.category(
        unichr(x))[0] == 'P'])
UNICODE_SYMBOL_CHARSET = frozenset(
    [unichr(x) for x in range(65536) if unicodedata.category(
        unichr(x))[0] == 'S'])
UNICODE_PUNCT_SYMBOL_CHARSET = UNICODE_PUNCT_CHARSET | UNICODE_SYMBOL_CHARSET

UNICODE_LETTER_CHARSET = frozenset(
    [unichr(x) for x in range(65536) if unicodedata.category(
        unichr(x))[0] == 'L'])
UNICODE_MARK_CHARSET = frozenset(
    [unichr(x) for x in range(65536) if unicodedata.category(
        unichr(x))[0] == 'M'])
UNICODE_NUMBER_CHARSET = frozenset(
    [unichr(x) for x in range(65536) if unicodedata.category(
        unichr(x))[0] == 'N'])
UNICODE_LETTER_MARK_NUMBER_CHARSET = (UNICODE_LETTER_CHARSET |
                                      UNICODE_MARK_CHARSET |
                                      UNICODE_NUMBER_CHARSET)

AR_LETTERS_CHARSET = frozenset(u'\u0621\u0622\u0623\u0624\u0625\u0626\u0627'
                               u'\u0628\u0629\u062a\u062b\u062c\u062d\u062e'
                               u'\u062f\u0630\u0631\u0632\u0633\u0634\u0635'
                               u'\u0636\u0637\u0638\u0639\u063a\u0640\u0641'
                               u'\u0642\u0643\u0644\u0645\u0646\u0647\u0648'
                               u'\u0649\u064a\u0671\u067e\u0686\u06a4\u06af')
AR_DIAC_CHARSET = frozenset(u'\u064b\u064c\u064d\u064e\u064f\u0650\u0651\u0652'
                            u'\u0670\u0640')
AR_CHARSET = AR_LETTERS_CHARSET | AR_DIAC_CHARSET

BW_LETTERS_CHARSET = frozenset(u'$&\'*<>ADEGHJPSTVYZ_bdfghjklmnpqrstvwxyz{|}')
BW_DIAC_CHARSET = frozenset(u'FKN`aiou~_')
BW_CHARSET = BW_LETTERS_CHARSET | BW_DIAC_CHARSET

SAFEBW_LETTERS_CHARSET = frozenset(u'ABCDEGHIJLMOPQSTVWYZ_bcdefghjklmnpqrstvwx'
                                   u'yz')
SAFEBW_DIAC_CHARSET = frozenset(u'FKNaeiou~_')
SAFEBW_CHARSET = SAFEBW_LETTERS_CHARSET | SAFEBW_DIAC_CHARSET

XMLBW_LETTERS_CHARSET = frozenset(u'$\'*ABDEGHIJOPSTWYZ_bdfghjklmnpqrstvwxyz{|'
                                  u'}')
XMLBW_DIAC_CHARSET = frozenset(u'FKN`aiou~_')
XMLBW_CHARSET = XMLBW_LETTERS_CHARSET | XMLBW_DIAC_CHARSET

HSB_LETTERS_CHARSET = frozenset(u'\'ADHST_bcdfghjklmnpqrstvwxyz'
                                u'\u00c2\u00c4\u00e1\u00f0\u00fd\u0100\u0102'
                                u'\u010e\u0127\u0161\u0175\u0177\u03b3\u03b8'
                                u'\u03c2')
HSB_DIAC_CHARSET = frozenset(u'.aiu~\u00c4\u00e1\u00e3\u0129\u0169_')
HSB_CHARSET = HSB_LETTERS_CHARSET | HSB_DIAC_CHARSET
