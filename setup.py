from distutils.core import setup

setup(
    name='lending_club_ml',
    version='1.0.0',
    author='Michael Kneier',
    author_email='michaeljkneier@gmail.com',
    packages=['lending_club_ml', 'lending_club_ml.tests'],
    url='http://github.com/mkneierV/LendingClubML',
    license=open('LICENSE.txt').read(),
    description='An library for Lending Club that lets you us ML models to pick notes to invest in',
    long_description=open('README.rst').read(),
    install_requires=[
        "requests >= 1.2.3",
        "beautifulsoup4 >= 4.1.3",
        "html5lib >= 0.95",
        "pybars >= 0.0.4"
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
        'Environment :: Console',
        'Topic :: Office/Business :: Financial',
        'Topic :: Utilities'
    ],
    keywords='lending_club_ml investing api lending club'
)
