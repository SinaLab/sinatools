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
    'pandas',
    'pyarabic'
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
            ('sinatools='
                'sinatools.cli:main'),
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
