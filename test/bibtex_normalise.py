#!/usr/bin/env python
"""This script canonicalises Bibtex files, or at least attempts to.
No guarantee is made as to it's ability to do this, it was only every intended
to operate on the output of either bibtexparser or pybtex
"""

from __future__ import print_function
import fileinput

WAITING = 0
INSIDE = 1


def main():
    """Iterate over lines in input, outputing a canonical version"""
    status = WAITING
    entries = []
    for line in fileinput.input():
        if status == WAITING:
            if line[0] == '@':
                status = INSIDE
                print(line.rstrip())
        else:  # Inside an entry
            if line[0] == '}':
                # Always show entries in alphabetical order by key
                entries.sort(key=lambda x: x.lower())
                for entry in entries:
                    print(entry)
                status = WAITING
                print("}")
            else:
                # Replace surrounding " with {}
                first = line.find("\"")
                last = line.rfind("\"")
                if first != -1 and last != -1:
                    line = (line[0:first] + "{" +
                            line[first+1:last] + "}" + line[last+1:])
                # entry keys lowercase
                equals = line.find("=")
                # Equal spacing at start of lines
                line = line[0:equals].lower() + line[equals:]
                line = line.lstrip()
                line = "    " + line
                entries.append(line.rstrip())

if __name__ == '__main__':
    main()
