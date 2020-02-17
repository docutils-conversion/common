#! /usr/bin/env python

# $Id: test_latex2e.py 6003 2009-06-27 20:44:09Z milde $
# Author: engelbert gruber <grubert@users.sourceforge.net>
# Copyright: This module has been placed in the public domain.

"""
Tests for manpage writer.
"""
from __future__ import absolute_import

if __name__ == '__main__':
    import __init__
from test_writers import DocutilsTestSupport


def suite():
    settings = {}
    s = DocutilsTestSupport.PublishTestSuite('manpage', suite_settings=settings)
    s.generateTests(totest)
    return s

indend_macros = r""".
.nr rst2man-indent-level 0
.
.de1 rstReportMargin
\\$1 \\n[an-margin]
level \\n[rst2man-indent-level]
level margin: \\n[rst2man-indent\\n[rst2man-indent-level]]
-
\\n[rst2man-indent0]
\\n[rst2man-indent1]
\\n[rst2man-indent2]
..
.de1 INDENT
.\" .rstReportMargin pre:
. RS \\$1
. nr rst2man-indent\\n[rst2man-indent-level] \\n[an-margin]
. nr rst2man-indent-level +1
.\" .rstReportMargin post:
..
.de UNINDENT
. RE
.\" indent \\n[an-margin]
.\" old: \\n[rst2man-indent\\n[rst2man-indent-level]]
.nr rst2man-indent-level -1
.\" new: \\n[rst2man-indent\\n[rst2man-indent-level]]
.in \\n[rst2man-indent\\n[rst2man-indent-level]]u
..
"""

totest = {}

totest['blank'] = [
        ["", 
        r""".\" Man page generated from reStructuredText.
.
.TH   "" "" ""
.SH NAME
 \- 
"""+indend_macros+
r""".\" Generated by docutils manpage writer.
.
"""],
        [r"""Hello, world.
=============

.. WARNING::
   This broke docutils-sphinx.

""",
        r""".\" Man page generated from reStructuredText.
.
.TH HELLO, WORLD.  "" "" ""
.SH NAME
Hello, world. \- 
"""+indend_macros+
r""".sp
\fBWARNING:\fP
.INDENT 0.0
.INDENT 3.5
This broke docutils\-sphinx.
.UNINDENT
.UNINDENT
.\" Generated by docutils manpage writer.
.
"""],
    ]

totest['simple'] = [
        ["""\
========        
 simple
========

---------------
 The way to go
---------------

:Author: someone@somewhere.net
:Date:   2009-08-05
:Copyright: public domain
:Version: 0.1
:Manual section: 1
:Manual group: text processing
:Arbitrary field: some text

SYNOPSIS
========

::

  K.I.S.S keep it simple.

DESCRIPTION
===========

General rule of life.

OPTIONS
=======

--config=<file>         Read configuration settings from <file>, if it exists.
--version, -V           Show this program's version number and exit.
--help, -h              Show this help message and exit.

OtHeR SECTION
=============

With mixed case.

.. Attention::

   Admonition with title

   * bullet list
   * bull and list

.. admonition:: homegrown 

   something important

. period at line start.

and . in a line and at line start
.in a paragraph
""", 
        r""".\" Man page generated from reStructuredText.
.
.TH SIMPLE 1 "2009-08-05" "0.1" "text processing"
.SH NAME
simple \- The way to go
"""+indend_macros+
r""".SH SYNOPSIS
.INDENT 0.0
.INDENT 3.5
.sp
.nf
.ft C
K.I.S.S keep it simple.
.ft P
.fi
.UNINDENT
.UNINDENT
.SH DESCRIPTION
.sp
General rule of life.
.SH OPTIONS
.INDENT 0.0
.TP
.BI \-\-config\fB= <file>
Read configuration settings from <file>, if it exists.
.TP
.B  \-\-version\fP,\fB  \-V
Show this program\(aqs version number and exit.
.TP
.B  \-\-help\fP,\fB  \-h
Show this help message and exit.
.UNINDENT
.SH OTHER SECTION
.sp
With mixed case.
.sp
\fBATTENTION!:\fP
.INDENT 0.0
.INDENT 3.5
Admonition with title
.INDENT 0.0
.IP \(bu 2
bullet list
.IP \(bu 2
bull and list
.UNINDENT
.UNINDENT
.UNINDENT
.INDENT 0.0
.INDENT 3.5
.IP "homegrown"
.sp
something important
.UNINDENT
.UNINDENT
.sp
\&. period at line start.
.sp
and . in a line and at line start
\&.in a paragraph
.SH AUTHOR
someone@somewhere.net

Arbitrary field: some text
.SH COPYRIGHT
public domain
.\" Generated by docutils manpage writer.
.
"""],
    ]

totest['table'] = [
        ["""\
        ====== =====
         head   and
        ====== =====
           1     2
          abc   so
        ====== =====
""", 
'''\
.\\" Man page generated from reStructuredText.
.
.TH   "" "" ""
.SH NAME
 \\- \n\
'''+indend_macros+
'''.INDENT 0.0
.INDENT 3.5
.TS
center;
|l|l|.
_
T{
head
T}\tT{
and
T}
_
T{
1
T}\tT{
2
T}
_
T{
abc
T}\tT{
so
T}
_
.TE
.UNINDENT
.UNINDENT
.\\" Generated by docutils manpage writer.
.
''']
]

totest['optiongroup'] = [
        ["""
optin group with dot as group item

$
   bla bla bla

#
   bla bla bla

.
   bla bla bla

[
   bla bla bla

]
   bla bla bla
""", 
        """\
.\\" Man page generated from reStructuredText.
.
.TH   "" "" ""
.SH NAME
 \\- \n\
"""+indend_macros+
"""optin group with dot as group item
.INDENT 0.0
.TP
.B $
bla bla bla
.UNINDENT
.INDENT 0.0
.TP
.B #
bla bla bla
.UNINDENT
.INDENT 0.0
.TP
.B \\&.
bla bla bla
.UNINDENT
.INDENT 0.0
.TP
.B [
bla bla bla
.UNINDENT
.INDENT 0.0
.TP
.B ]
bla bla bla
.UNINDENT
.\\" Generated by docutils manpage writer.
."""],
    ]

totest['definitionlist'] = [
        ["""
====================
Definition List Test
====================

:Abstract: Docinfo is required.

Section
=======

:term1:

    Description of Term 1 Description of Term 1 Description of Term 1
    Description of Term 1 Description of Term 1

    Description of Term 1 Description of Term 1 Description of Term 1
    Description of Term 1 Description of Term 1

""", 
'''\
.\\" Man page generated from reStructuredText.
.
.TH DEFINITION LIST TEST  "" "" ""
.SH NAME
Definition List Test \\- \n\
'''+indend_macros+
'''.SS Abstract
.sp
Docinfo is required.
.SH SECTION
.INDENT 0.0
.TP
.B term1
Description of Term 1 Description of Term 1 Description of Term 1
Description of Term 1 Description of Term 1
.sp
Description of Term 1 Description of Term 1 Description of Term 1
Description of Term 1 Description of Term 1
.UNINDENT
.\\" Generated by docutils manpage writer.
.'''],
    ]

totest['cmdlineoptions'] = [
        ["""optional arguments:
  -h, --help                 show this help
  --output FILE, -o FILE     output filename
  -i DEVICE, --input DEVICE  input device
""", 
        r""".\" Man page generated from reStructuredText.
.
.TH   "" "" ""
.SH NAME
 \- 
"""+indend_macros+
r""".INDENT 0.0
.TP
.B optional arguments:
.INDENT 7.0
.TP
.B  \-h\fP,\fB  \-\-help
show this help
.TP
.BI \-\-output \ FILE\fR,\fB \ \-o \ FILE
output filename
.TP
.BI \-i \ DEVICE\fR,\fB \ \-\-input \ DEVICE
input device
.UNINDENT
.UNINDENT
.\" Generated by docutils manpage writer.
.
"""],
    ]


if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
