from os.path import join, abspath, dirname

from setuptools import setup, find_packages

with open(join(abspath(dirname(__file__)), 'README.md'), encoding='utf-8') as fd:
    long_description = fd.read()

setup(
    name='pscraper-lib',
    version='1.0',
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
        'beautifulsoup4>=4.8.0,<4.9.0',
        'folium>=0.10.0,<0.11.0',
        'pandas>=1.0.0,<1.1.0',
        'requests>=2.22.0,<2.23.0',
        'xlrd>=1.2.0,<1.3.0',
        'XlsxWriter>=1.1.9,<1.2.0',
        'PyYaml>=5.1.2,<5.2.0',
        'flake8>=3.7.9,<3.8.0',
        'slackclient>=2.5.0,<2.6.0',
        'address-parser>=1.0.0,<1.1.0',
        'pyslack>=0.5.0,<0.6.0'
    ]
)
