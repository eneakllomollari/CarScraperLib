import setuptools

setuptools.setup(
    name='CarScraperLib',
    version='1.0',
    author='Enea Kllomollari',
    author_email='ekllomollari@ucdavis.edu',
    description='PHEV Car Scraper Library',
    long_description='Car Scraper Library package to be shared different scraping projects',
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'beautifulsoup4>=4.8.0',
        'bs4>=0.0.1'
        'folium>=0.10.0',
        'pandas>=0.25.0',
        'requests>=2.22.0',
        'xlrd>=1.2.0',
        'XlsxWriter>=1.1.9',
        'PyYaml>=5.1.2'
    ]
)
