#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.1 $
:Date: $Date: 2001/09/01 16:59:56 $
:Copyright: This module has been placed in the public domain.

Tests for states.py.
"""

import RSTTestSupport

def suite():
    s = RSTTestSupport.ParserTestSuite(id=__file__)
    s.generateTests(totest)
    return s

totest = {}

totest['footnotes'] = [
["""\
.. [footnote] This is a footnote.
""",
"""\
<document>
    <footnote name="footnote">
        <label>
            footnote
        </label>
        <paragraph>
            This is a footnote.
        </paragraph>
    </footnote>
</document>
"""],
["""\
.. [footnote] This is a footnote
   on multiple lines.
""",
"""\
<document>
    <footnote name="footnote">
        <label>
            footnote
        </label>
        <paragraph>
            This is a footnote
            on multiple lines.
        </paragraph>
    </footnote>
</document>
"""],
["""\
.. [footnote1] This is a footnote
     on multiple lines with more space.

.. [footnote2] This is a footnote
  on multiple lines with less space.
""",
"""\
<document>
    <footnote name="footnote1">
        <label>
            footnote1
        </label>
        <paragraph>
            This is a footnote
            on multiple lines with more space.
        </paragraph>
    </footnote>
    <footnote name="footnote2">
        <label>
            footnote2
        </label>
        <paragraph>
            This is a footnote
            on multiple lines with less space.
        </paragraph>
    </footnote>
</document>
"""],
["""\
.. [footnote]
   This is a footnote on multiple lines
   whose block starts on line 2.
""",
"""\
<document>
    <footnote name="footnote">
        <label>
            footnote
        </label>
        <paragraph>
            This is a footnote on multiple lines
            whose block starts on line 2.
        </paragraph>
    </footnote>
</document>
"""],
["""\
.. [footnote]

That was an empty footnote.
""",
"""\
<document>
    <footnote name="footnote">
        <label>
            footnote
        </label>
    </footnote>
    <paragraph>
        That was an empty footnote.
    </paragraph>
</document>
"""],
["""\
.. [footnote]
No blank line.
""",
"""\
<document>
    <footnote name="footnote">
        <label>
            footnote
        </label>
    </footnote>
    <system_warning level="1">
        <paragraph>
            Unindent without blank line at line 2.
        </paragraph>
    </system_warning>
    <paragraph>
        No blank line.
    </paragraph>
</document>
"""],
["""\
.. [foot label with spaces] this isn't a footnote

.. [*footlabelwithmarkup*] this isn't a footnote
""",
"""\
<document>
    <comment>
        [foot label with spaces] this isn't a footnote
    </comment>
    <comment>
        [*footlabelwithmarkup*] this isn't a footnote
    </comment>
</document>
"""],
]

totest['auto_numbered_footnotes'] = [
["""\
[#]_ is the first auto-numbered footnote reference.
[#]_ is the second auto-numbered footnote reference.

.. [#] Auto-numbered footnote 1.
.. [#] Auto-numbered footnote 2.
.. [#] Auto-numbered footnote 3.

[#]_ is the third auto-numbered footnote reference.
""",
"""\
<document>
    <paragraph>
        <footnote_reference auto="1"/>
         is the first auto-numbered footnote reference.
        <footnote_reference auto="1"/>
         is the second auto-numbered footnote reference.
    </paragraph>
    <footnote>
        <paragraph>
            Auto-numbered footnote 1.
        </paragraph>
    </footnote>
    <footnote>
        <paragraph>
            Auto-numbered footnote 2.
        </paragraph>
    </footnote>
    <footnote>
        <paragraph>
            Auto-numbered footnote 3.
        </paragraph>
    </footnote>
    <paragraph>
        <footnote_reference auto="1"/>
         is the third auto-numbered footnote reference.
    </paragraph>
</document>
"""],
["""\
[#third]_ is a reference to the third auto-numbered footnote.

.. [#first] First auto-numbered footnote.
.. [#second] Second auto-numbered footnote.
.. [#third] Third auto-numbered footnote.

[#second]_ is a reference to the second auto-numbered footnote.
[#first]_ is a reference to the first auto-numbered footnote.
[#third]_ is another reference to the third auto-numbered footnote.

Here are some internal cross-references to the implicit targets
generated by the footnotes: first_, second_, third_.
""",
"""\
<document>
    <paragraph>
        <footnote_reference auto="1" refname="third"/>
         is a reference to the third auto-numbered footnote.
    </paragraph>
    <footnote name="first">
        <paragraph>
            First auto-numbered footnote.
        </paragraph>
    </footnote>
    <footnote name="second">
        <paragraph>
            Second auto-numbered footnote.
        </paragraph>
    </footnote>
    <footnote name="third">
        <paragraph>
            Third auto-numbered footnote.
        </paragraph>
    </footnote>
    <paragraph>
        <footnote_reference auto="1" refname="second"/>
         is a reference to the second auto-numbered footnote.
        <footnote_reference auto="1" refname="first"/>
         is a reference to the first auto-numbered footnote.
        <footnote_reference auto="1" refname="third"/>
         is another reference to the third auto-numbered footnote.
    </paragraph>
    <paragraph>
        Here are some internal cross-references to the implicit targets
        generated by the footnotes: 
        <link refname="first">
            first
        </link>
        , 
        <link refname="second">
            second
        </link>
        , 
        <link refname="third">
            third
        </link>
        .
    </paragraph>
</document>
"""],
["""\
Mixed anonymous and labelled auto-numbered footnotes:

[#four]_ should be 4, [#]_ should be 1,
[#]_ should be 3, [#]_ is one too many,
[#two]_ should be 2, and [#six]_ doesn't exist.

.. [#] Auto-numbered footnote 1.
.. [#two] Auto-numbered footnote 2.
.. [#] Auto-numbered footnote 3.
.. [#four] Auto-numbered footnote 4.
.. [#five] Auto-numbered footnote 5.
.. [#five] Auto-numbered footnote 5 again (duplicate).
""",
"""\
<document>
    <paragraph>
        Mixed anonymous and labelled auto-numbered footnotes:
    </paragraph>
    <paragraph>
        <footnote_reference auto="1" refname="four"/>
         should be 4, 
        <footnote_reference auto="1"/>
         should be 1,
        <footnote_reference auto="1"/>
         should be 3, 
        <footnote_reference auto="1"/>
         is one too many,
        <footnote_reference auto="1" refname="two"/>
         should be 2, and 
        <footnote_reference auto="1" refname="six"/>
         doesn't exist.
    </paragraph>
    <footnote>
        <paragraph>
            Auto-numbered footnote 1.
        </paragraph>
    </footnote>
    <footnote name="two">
        <paragraph>
            Auto-numbered footnote 2.
        </paragraph>
    </footnote>
    <footnote>
        <paragraph>
            Auto-numbered footnote 3.
        </paragraph>
    </footnote>
    <footnote name="four">
        <paragraph>
            Auto-numbered footnote 4.
        </paragraph>
    </footnote>
    <footnote dupname="five">
        <paragraph>
            Auto-numbered footnote 5.
        </paragraph>
    </footnote>
    <footnote dupname="five">
        <system_warning level="0">
            <paragraph>
                Duplicate implicit link name: "five"
            </paragraph>
        </system_warning>
        <paragraph>
            Auto-numbered footnote 5 again (duplicate).
        </paragraph>
    </footnote>
</document>
"""],
]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
