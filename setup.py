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

requirements = [
    'six',
    'farasapy',
    'tqdm',
    'requests',
    # 'regex',
    'pathlib',
    # 'torch==2.5.1',
    'transformers==4.47.1',
    'torchvision==0.20.1',
    'seqeval==1.2.2',
    'natsort==7.1.1',
    'pandas'
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
            ('arStrip='
                'sinatools.CLI.utils.arStrip:main'),
            ('jaccard_similarity='
                'sinatools.CLI.utils.jaccard:main'),
            ('implication='
                'sinatools.CLI.utils.implication:main'),
            ('sentence_tokenizer='
                'sinatools.CLI.utils.sentence_tokenizer:main'),
            ('transliterate='
                'sinatools.CLI.utils.text_transliteration:main'),
            ('morphology_analyzer='
                'sinatools.CLI.morphology.morph_analyzer:main'),
            ('alma_multi_word='
                'sinatools.CLI.morphology.ALMA_multi_word:main'),
            ('entity_extractor='
                'sinatools.CLI.ner.entity_extractor:main'),
            ('remove_punctuation='
                'sinatools.CLI.utils.remove_punctuation:main'),
            ('remove_latin='
                'sinatools.CLI.utils.remove_latin:main'),
            ('wsd='
                'sinatools.CLI.wsd.disambiguator:main'),
            ('corpus_tokenizer='
                'sinatools.CLI.utils.corpus_tokenizer:main'),
            ('appdatadir='
                'sinatools.CLI.DataDownload.get_appdatadir:main'),
            ('download_files='
                'sinatools.CLI.DataDownload.download_files:main'),
            ('corpus_entity_extractor='
                'sinatools.CLI.ner.corpus_entity_extractor:main'),
            ('text_dublication_detector='
                'sinatools.CLI.utils.text_dublication_detector:main'),     
            ('evaluate_synonyms='
                'sinatools.CLI.synonyms.evaluate_synonyms:main'),  
            ('extend_synonyms='
                'sinatools.CLI.synonyms.extend_synonyms:main'),                    
            ('semantic_relatedness='
                'sinatools.CLI.semantic_relatedness.compute_relatedness:main'),
            ('relation_extractor='
                'sinatools.CLI.relations.relation_extractor:main'),
        ],
    },
    data_files=[('sinatools', ['sinatools/environment.yml'])],
    package_data={'sinatools': ['data/*.pickle', 'environment.yml']},
    install_requires=requirements,
    license="MIT license",
    description='Open-source Python toolkit for Arabic Natural Understanding, allowing people to integrate it in their system workflow.',
    long_description = readme + "\n",
    long_description_content_type='text/markdown',
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
