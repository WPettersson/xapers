#!/usr/bin/env python

from distutils.core import setup
from distutils.util import convert_path

version_path = convert_path('lib/xapers/version.py')
version_namespace = {}
with open(version_path) as version_file:
    exec(version_file.read(), version_namespace)

setup(
    name = 'xapers',
    version = version_namespace['__version__'],
    description = 'Xapian article indexing system.',
    author = 'Jameson Rollins',
    author_email = 'jrollins@finestructure.net',
    url = '',

    package_dir = {'': 'lib'},
    packages = [
        'xapers',
        'xapers.parsers',
        'xapers.sources',
        'xapers.nci',
        ],
    scripts = ['bin/xapers'],

    requires = [
        'xapian',
        'pybtex',
        'urwid'
        ],
    )
