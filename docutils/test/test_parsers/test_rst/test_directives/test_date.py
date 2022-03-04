#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for the misc.py "date" directive.
"""

if __name__ == '__main__':
    import __init__
from test_parsers import DocutilsTestSupport
import time

from docutils.io import locale_encoding


def suite():
    s = DocutilsTestSupport.ParserTestSuite()
    s.generateTests(totest)
    return s


totest = {}

totest['date'] = [
["""\
.. |date| date::

Today's date is |date|.
""",
"""\
<document source="test data">
    <substitution_definition names="date">
        %s
    <paragraph>
        Today's date is \n\
        <substitution_reference refname="date">
            date
        .
""" % time.strftime('%Y-%m-%d')],
["""\
.. |date| date:: %a, %d %b %Y
""",
"""\
<document source="test data">
    <substitution_definition names="date">
        %s
""" % time.strftime('%a, %d %b %Y')],
["""\
.. date::
""",
"""\
<document source="test data">
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            Invalid context: the "date" directive can only be used within a substitution definition.
        <literal_block xml:space="preserve">
            .. date::
"""],
]

# some locales return non-ASCII characters for names of days or months
if locale_encoding in ['utf8', 'utf-8', 'latin-1']:
    totest['decode date'] = [
    ["""\
.. |date| date:: t\xc3glich
""",
    """\
<document source="test data">
    <substitution_definition names="date">
        t\xc3glich
"""],
    ]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
