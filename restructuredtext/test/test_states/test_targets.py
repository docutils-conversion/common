#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.6 $
:Date: $Date: 2001/10/30 05:04:33 $
:Copyright: This module has been placed in the public domain.

Tests for states.py.
"""

import RSTTestSupport

def suite():
    s = RSTTestSupport.ParserTestSuite()
    s.generateTests(totest)
    return s

totest = {}

totest['targets'] = [
["""\
.. _target:

(Internal hyperlink target.)
""",
"""\
<document>
    <target name="target">
    <paragraph>
        (Internal hyperlink target.)
"""],
["""\
External hyperlink targets:

.. _one-liner: http://structuredtext.sourceforge.net

.. _starts-on-this-line: http://
                         structuredtext.
                         sourceforge.net

.. _entirely-below:
   http://structuredtext.
   sourceforge.net

.. _not-indirect: uri\_
""",
"""\
<document>
    <paragraph>
        External hyperlink targets:
    <target name="one-liner" refuri="http://structuredtext.sourceforge.net">
    <target name="starts-on-this-line" refuri="http://structuredtext.sourceforge.net">
    <target name="entirely-below" refuri="http://structuredtext.sourceforge.net">
    <target name="not-indirect" refuri="uri_">
"""],
["""\
Indirect hyperlink targets:

.. _target1: reference_

.. _target2: `phrase-link reference`_
""",
"""\
<document>
    <paragraph>
        Indirect hyperlink targets:
    <target name="target1" refname="reference">
    <target name="target2" refname="phrase-link reference">
"""],
["""\
.. _target: Not a proper hyperlink target
""",
"""\
<document>
    <system_warning level="1">
        <paragraph>
            Hyperlink target at line 1 contains whitespace. Perhaps a footnote was intended?
        <literal_block>
            .. _target: Not a proper hyperlink target
"""],
["""\
.. _a long target name:

.. _`a target name: including a colon (quoted)`:

.. _a target name\: including a colon (escaped):
""",
"""\
<document>
    <target name="a long target name">
    <target name="a target name: including a colon (quoted)">
    <target name="a target name: including a colon (escaped)">
"""],
["""\
External hyperlink:

.. _target: http://www.python.org/
""",
"""\
<document>
    <paragraph>
        External hyperlink:
    <target name="target" refuri="http://www.python.org/">
"""],
["""\
Duplicate external targets (different URIs):

.. _target: first

.. _target: second
""",
"""\
<document>
    <paragraph>
        Duplicate external targets (different URIs):
    <target dupname="target" refuri="first">
    <system_warning level="1">
        <paragraph>
            Duplicate external target name: "target"
    <target name="target" refuri="second">
"""],
["""\
Duplicate external targets (same URIs):

.. _target: first

.. _target: first
""",
"""\
<document>
    <paragraph>
        Duplicate external targets (same URIs):
    <target dupname="target" refuri="first">
    <system_warning level="0">
        <paragraph>
            Duplicate external target name: "target"
    <target name="target" refuri="first">
"""],
["""\
Duplicate implicit targets.

Title
=====

Paragraph.

Title
=====

Paragraph.
""",
"""\
<document>
    <paragraph>
        Duplicate implicit targets.
    <section dupname="title">
        <title>
            Title
        <paragraph>
            Paragraph.
    <section dupname="title">
        <title>
            Title
        <system_warning level="0">
            <paragraph>
                Duplicate implicit target name: "title"
        <paragraph>
            Paragraph.
"""],
["""\
Duplicate implicit/explicit targets.

Title
=====

.. _title:

Paragraph.
""",
"""\
<document>
    <paragraph>
        Duplicate implicit/explicit targets.
    <section dupname="title">
        <title>
            Title
        <system_warning level="0">
            <paragraph>
                Duplicate implicit target name: "title"
        <target name="title">
        <paragraph>
            Paragraph.
"""],
["""\
Duplicate explicit targets.

.. _title:

First.

.. _title:

Second.

.. _title:

Third.
""",
"""\
<document>
    <paragraph>
        Duplicate explicit targets.
    <target dupname="title">
    <paragraph>
        First.
    <system_warning level="1">
        <paragraph>
            Duplicate explicit target name: "title"
    <target dupname="title">
    <paragraph>
        Second.
    <system_warning level="1">
        <paragraph>
            Duplicate explicit target name: "title"
    <target dupname="title">
    <paragraph>
        Third.
"""],
["""\
Duplicate targets:

Target
======

Implicit section header target.

.. [target] Implicit footnote target.

.. _target:

Explicit internal target.

.. _target: Explicit_external_target
""",
"""\
<document>
    <paragraph>
        Duplicate targets:
    <section dupname="target">
        <title>
            Target
        <paragraph>
            Implicit section header target.
        <footnote dupname="target">
            <label>
                target
            <system_warning level="0">
                <paragraph>
                    Duplicate implicit target name: "target"
            <paragraph>
                Implicit footnote target.
        <system_warning level="0">
            <paragraph>
                Duplicate implicit target name: "target"
        <target dupname="target">
        <paragraph>
            Explicit internal target.
        <system_warning level="1">
            <paragraph>
                Duplicate external target name: "target"
        <target name="target" refuri="Explicit_external_target">
"""],
]

totest['anonymous_targets'] = [
["""\
Anonymous external hyperlink target:

.. __: http://w3c.org/
""",
"""\
<document>
    <paragraph>
        Anonymous external hyperlink target:
    <target anonymous="1" refuri="http://w3c.org/">
"""],
["""\
Anonymous external hyperlink target:

__ http://w3c.org/
""",
"""\
<document>
    <paragraph>
        Anonymous external hyperlink target:
    <target anonymous="1" refuri="http://w3c.org/">
"""],
["""\
Anonymous indirect hyperlink target:

.. __: reference_
""",
"""\
<document>
    <paragraph>
        Anonymous indirect hyperlink target:
    <target anonymous="1" refname="reference">
"""],
["""\
Anonymous indirect hyperlink targets:

__ reference_
__ `a very long
   reference`_
""",
"""\
<document>
    <paragraph>
        Anonymous indirect hyperlink targets:
    <target anonymous="1" refname="reference">
    <target anonymous="1" refname="a very long reference">
"""],
["""\
Mixed anonymous & named indirect hyperlink targets:

__ reference_
.. __: reference_
__ reference_
.. _target1: reference_
no blank line

.. _target2: reference_
__ reference_
.. __: reference_
__ reference_
no blank line
""",
"""\
<document>
    <paragraph>
        Mixed anonymous & named indirect hyperlink targets:
    <target anonymous="1" refname="reference">
    <target anonymous="1" refname="reference">
    <target anonymous="1" refname="reference">
    <target name="target1" refname="reference">
    <system_warning level="1">
        <paragraph>
            Unindent without blank line at line 4.
    <paragraph>
        no blank line
    <target name="target2" refname="reference">
    <target anonymous="1" refname="reference">
    <target anonymous="1" refname="reference">
    <target anonymous="1" refname="reference">
    <system_warning level="1">
        <paragraph>
            Unindent without blank line at line 10.
    <paragraph>
        no blank line
"""],
]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
