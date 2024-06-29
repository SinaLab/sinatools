#!/usr/bin/env python

"""The setup script."""
import os 
from setuptools import setup, find_packages
VERSION_FILE = os.path.join(os.path.dirname(__file__),
                            'sinatools',
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
             'sinatools.install_env:main'),
            ('sina_arStrip='
             'sinatools.CLI.utils.arStrip:main'),
            ('sina_jaccard_similarity='
             'sinatools.CLI.utils.jaccard:main'),
            ('sina_implication='
             'sinatools.CLI.utils.implication:main'),
            ('sina_sentence_tokenize='
             'sinatools.CLI.utils.sentence_tokenizer:main'),
            ('sina_transliterate='
             'sinatools.CLI.utils.text_transliteration:main'),
            ('sina_morph_analyze='
             'sinatools.CLI.morphology.morph_analyzer:main'),
            ('sina_alma_multi_word='
             'sinatools.CLI.morphology.ALMA_multi_word:main'),
            ('arabi_ner='
             'sinatools.CLI.arabiner.bin.infer:main'),
            ('sina_remove_punctuation='
              'sinatools.CLI.utils.remove_Punc:main'),
            ('sina_remove_latin='
             'sinatools.CLI.utils.latin_remove:main'),
            ('sina_salma='
             'sinatools.CLI.salma.salma_tools:main'),
            ('sina_corpus_tokenizer='
             'sinatools.CLI.utils.corpus_tokenizer:main'),
            ('sina_appdatadir='
             'sinatools.CLI.DataDownload.get_appdatadir:main'),
            ('sina_download_files='
             'sinatools.CLI.DataDownload.download_files:main'),
            ('arabi_ner2='
             'sinatools.CLI.arabiner.bin.infer2:main')
        ],
    },
    data_files=[('sinatools', ['sinatools/environment.yml'])],
    package_data={'sinatools': ['data/*.pickle', 'environment.yml']},
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='sinatools',
    name='SinaTools',
    packages=find_packages(include=['sinatools', 'sinatools.*']),
	setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/SinaLab/sinatools',
    version=VERSION,
    zip_safe=False,
)
