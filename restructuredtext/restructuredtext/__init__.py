#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.8 $
:Date: $Date: 2002/01/16 06:19:04 $
:Copyright: This module has been placed in the public domain.

This is ``the dps.parsers.restructuredtext`` package. It exports a single
class, `Parser`.

Usage
=====

1. Create a parser::

       parser = dps.parsers.restructuredtext.Parser()

   Several optional arguments may be passed to modify the parser's behavior.
   Please see `dps.parsers.model.Parser` for details.

2. Gather input (a multi-line string), by reading a file or the standard
   input::

       input = sys.stdin.read()

3. Run the parser, generating a `dps.nodes.document` tree::

       document = parser.parse(input)

Parser Overview
===============

The reStructuredText parser is implemented as a state machine, examining its
input one line at a time. To understand how the parser works, please first
become familiar with the `dps.statemachine` module, then see the
`states` module.
"""

import dps.parsers.model
import dps.statemachine
import states

__all__ = ['Parser']


class Parser(dps.parsers.model.Parser):

    """The reStructuredText parser."""

    def __init__(self, *args, **keywordargs):
        dps.parsers.model.Parser.__init__(self, *args, **keywordargs)
        self.statemachine = states.RSTStateMachine(
              stateclasses=states.stateclasses, initialstate='Body',
              languagecode=self.languagecode, debug=self.debug)

    def parse(self, inputstring):
        """Parse `inputstring` and return a `dps.nodes.document` tree."""
        self.setup_parse(inputstring)
        inputlines = dps.statemachine.string2lines(self.inputstring,
                                                   convertwhitespace=1)
        document = self.statemachine.run(inputlines,
                                         warninglevel=self.warninglevel,
                                         errorlevel=self.errorlevel)
        return document
