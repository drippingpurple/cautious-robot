from setuptools import setup, find_packages
from codecs import open
from os import path
import re

here = path.abspath(path.dirname(__file__))

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('scraper_linkedin_test/__init__.py').read(),
    re.M
    ).group(1)

setup(
    name='scraper_linkedin_test',
    packages=['scraper_linkedin_test'],
    version=version,
    description='Targeted data scrape from Linkedin',
    author='Harrison Wold',
    install_requires=[package.split("\n")[0] for package in open('requirements.txt', 'r').readlines()]
    #  author email
    #  url
    #  download url
    #  keywords
    #  classifiers
    )