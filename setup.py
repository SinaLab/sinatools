#!/usr/bin/env python

"""The setup script."""
import os 
from setuptools import setup, find_packages
VERSION_FILE = os.path.join(os.path.dirname(__file__),
                            'nlptools',
                            'VERSION')
with open(VERSION_FILE, encoding='utf-8') as version_fp:
    VERSION = version_fp.read().strip()
with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'six',
    'farasapy',
    'tqdm',
    'requests',
    'regex',
    'pathlib',
    'torch==1.13.0',
    'transformers==4.24.0',
    'torchtext==0.14.0',
    'torchvision==0.14.0',
    'seqeval==1.2.2',
    'natsort==7.1.1' #,
    #'arabiner'
]


setup_requirements = [
    "pytest-runner",
]

test_requirements = [
    "pytest>=3",
]


setup(
    entry_points={
        'console_scripts':[
            ('install_env='
             'nlptools.install_env:main'),
            ('sina_arStrip='
             'nlptools.CLI.utils.arStrip:main'),
            ('sina_jaccard_similarity='
             'nlptools.CLI.utils.jaccard:main'),
            ('sina_implication='
             'nlptools.CLI.utils.implication:main'),
            ('sina_sentence_tokenize='
             'nlptools.CLI.utils.sentence_tokenizer:main'),
            ('sina_transliterate='
             'nlptools.CLI.utils.text_transliteration:main'),
            ('sina_morph_analyze='
             'nlptools.CLI.morphology.morph_analyzer:main'),
            ('sina_alma_multi_word='
             'nlptools.CLI.morphology.ALMA_multi_word:main'),
            ('arabi_ner='
             'nlptools.CLI.arabiner.bin.infer:main'),
            ('sina_remove_punctuation='
              'nlptools.CLI.utils.remove_Punc:main'),
            ('sina_remove_latin='
             'nlptools.CLI.utils.latin_remove:main'),
            ('sina_salma='
             'nlptools.CLI.salma.salma_tools:main'),
            ('sina_corpus_tokenizer='
             'nlptools.CLI.utils.corpus_tokenizer:main'),
            ('sina_appdatadir='
             'nlptools.CLI.DataDownload.get_appdatadir:main'),
            ('sina_download_files='
             'nlptools.CLI.DataDownload.download_files:main'),
            ('arabi_ner2='
             'nlptools.CLI.arabiner.bin.infer2:main')
        ],
    },
    data_files=[('nlptools', ['nlptools/environment.yml'])],
    package_data={'nlptools': ['data/*.pickle', 'environment.yml']},
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='nlptools',
    name='SinaTools',
    packages=find_packages(include=['nlptools', 'nlptools.*']),
	setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/SinaLab/nlptools',
    version=VERSION,
    zip_safe=False,
)
