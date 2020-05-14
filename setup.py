from os.path import abspath, dirname, join

from setuptools import find_packages, setup

with open(join(abspath(dirname(__file__)), 'README.md'), encoding='utf-8') as fd:
    long_description = fd.read()

setup(
    name='pscraper-lib',
    version='2.0.0',
    author='Enea Kllomollari',
    author_email='eneakllomollari@gmail.com',
    description='PHEV Electric Vehicle Scraping Library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'beautifulsoup4>=4.8.0,<4.9.0',
        'requests>=2.22.0',
        'slackclient>=2.5.0',
        'PyHamcrest>=2.0.2',
        'flake8>=3.7.9',
        'flake8-import-order>=0.18.1',
        'flake8-print>=3.1.4',
        'flake8-builtins>=1.5.2',
        'flake8-bugbear>=20.1.4',
        'flake8-return>=1.1.1',
    ]
)
