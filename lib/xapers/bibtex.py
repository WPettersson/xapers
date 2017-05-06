"""
This file is part of xapers.

Xapers is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

Xapers is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
for more details.

You should have received a copy of the GNU General Public License
along with notmuch.  If not, see <http://www.gnu.org/licenses/>.

Copyright 2012-2016
Jameson Rollins <jrollins@finestructure.net>
"""

import json
import bibtexparser


def clean_bib_string(string):
    for char in ['{', '}']:
        string = string.replace(char, '')
    return string

##################################################


class BibtexError(Exception):
    """Base class for Xapers bibtex exceptions."""
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

##################################################


class Bibtex():
    """Represents a bibtex database.

    """
    # http://www.bibtex.org/Format/
    def __init__(self, bibdata):
        self.keys = bibdata.entries_dict.keys()
        print(self.keys)
        self.entries = bibdata.entries_dict.values()
        print(self.entries)
        self.index = -1
        self.max = len(self.entries)

    @classmethod
    def from_file(cls, bibfile):
        with open(bibfile) as f:
            bibdata = bibtexparser.load(f)
        print(bibdata)
        print(bibdata.entries)
        return cls(bibdata)

    @classmethod
    def from_string(cls, bibstring):
        return cls(bibtexparser.loads(bibstring))

    def __getitem__(self, index):
        key = self.keys[index]
        entry = self.entries[index]
        return Bibentry(key, entry)

    def __iter__(self):
        return self

    def __len__(self):
        return self.max

    def next(self):
        self.index = self.index + 1
        if self.index == self.max:
            raise StopIteration
        return self[self.index]

##################################################


class Bibentry():
    """Represents an individual entry in a bibtex database.

    """
    def __init__(self, key, entry):
        self.key = key
        self.entry = entry

    def __getitem__(self, item):
        return self.entry[item]

    def get_authors(self):
        """Return a list of authors."""
        return self.entry['author'].split(' and ')

    def get_fields(self):
        """Return a dict of fields."""
        bibfields = self.entry
        # entry.fields is actually already a dict, but we want to
        # clean the strings first
        fields = {}
        for field in bibfields:
            fields[field] = unicode(clean_bib_string(bibfields[field]))
        return fields

    def set_file(self, path):
        # FIXME: what's the REAL proper format for this
        self.entry['file'] = ':%s:%s' % (path, 'pdf')

    def get_file(self):
        """Returns file path if file field exists.

        Expects either single path string or Mendeley/Jabref format.

        """
        try:
            parsed = self.entry['file'].split(':')
            if len(parsed) > 1:
                return parsed[1]
            else:
                return parsed[0]
        except KeyError:
            return None
        except IndexError:
            return None

    def _entry2db(self):
        db = bibtexparser.BibDatabase()
        db.entries = [self.entry]
        return db

    def as_string(self):
        """Return entry as formatted bibtex string."""
        return bibtexparser.dumps(self._entry2db())

    def to_file(self, path):
        """Write entry bibtex to file."""
        with open(path, 'w') as f:
            bibtexparser.dump(self._entry2db(), f)

##################################################


def data2bib(data, key, type='article'):
    """Convert a python dict into a Bibentry object."""
    return Bibentry(key, data).as_string()


def json2bib(jsonstring, key, type='article'):
    """Convert a json string into a Bibentry object."""
    if not json:
        return
    data = json.loads(jsonstring)
    return Bibentry(key, data).as_string()
