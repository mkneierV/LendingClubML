from distutils.core import setup
from setuptools import find_packages
from os import path


here = path.abspath(path.dirname(__file__))

# Get the long description from README
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='lending_club_ml',
    packages = find_packages(exclude=['tests']),
    version='0.1.0',
    author='Michael Kneier',
    author_email='michaelkneier@gmail.com',
    url='http://github.com/mkneierV/LendingClubML',
    license=open('LICENSE.txt').read(),
    description="Package for interacting with Lending Club's REST API, and for building and implementing sophisticated investment strategies.",
    long_description=long_description,
    install_requires=[
        "requests >= 1.2.3",
        "beautifulsoup4 >= 4.1.3",
        "html5lib >= 0.95",
        "pybars >= 0.0.4",
        "httpretty >= 0.8.10",
        "pandas >= 0.16.0",
        "numpy >= 1.5.0",
        "scikit-learn >= 0.16.0"
    ],
    platforms='osx, posix, linux, windows',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Topic :: Office/Business :: Financial',
        'Topic :: Utilities'
    ],
    keywords=['lending club', 'investing', 'api', 'machine learning', 'programmatic investing']
)
