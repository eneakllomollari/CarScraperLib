import setuptools

setuptools.setup(
    name='CarScraperLib',
    version='0.0.1',
    author='Enea Kllomollari',
    author_email='ekllomollari@ucdavis.edu',
    description='PHEV Car Scraper Library',
    long_description='Car Scraper Library package to be shared different scraping projects',
    url='placeholder',
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'beautifulsoup4>=4.8.0',
        'branca>=0.3.1'
        'bs4>=0.0.1',
        'certifi>=2019.6.16',
        'chardet>=3.0.4',
        'folium>=0.10.0',
        'idna>=2.8',
        'Jinja2>=2.10.1',
        'MarkupSafe>=1.1.1',
        'numpy>=1.17.0',
        'pandas>=0.25.0',
        'python-dateutil>=2.8.0',
        'pytz>=2019.2',
        'requests>=2.22.0',
        'six>=1.12.0',
        'soupsieve>=1.9.3',
        'urllib3>=1.25.3',
        'xlrd>=1.2.0',
        'XlsxWriter>=1.1.9'
    ]
)
