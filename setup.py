from os.path import abspath, dirname, join

from setuptools import find_packages, setup

with open(join(abspath(dirname(__file__)), 'README.md'), encoding='utf-8') as fd:
    long_description = fd.read()

setup(
    name='pscraper-lib',
    version='2.0',
    author='Enea Kllomollari',
    author_email='ekllomollari@ucdavis.edu',
    description='PHEV Car Scraper Library for electric vehicles',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'beautifulsoup4>=4.8.0',
        'requests>=2.22.0',
        'flake8>=3.7.9',
        'slackclient>=2.5.0',
        'PyHamcrest>=2.0.2'
    ]
)
