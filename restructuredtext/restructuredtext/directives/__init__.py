#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.7 $
:Date: $Date: 2002/02/12 02:29:02 $
:Copyright: This module has been placed in the public domain.

This package contains directive implementation modules.

The interface for directive functions is as follows::

    def directivefn(match, type, data, state, statemachine, attributes)

Where:

- ``match`` is a regular expression match object which matched the first line
  of the directive. ``match.group(1)`` gives the directive name.
- ``type`` is the directive type or name.
- ``data`` contains the remainder of the first line of the directive after the
  "::".
- ``state`` is the state which called the directive function.
- ``statemachine`` is the state machine which controls the state which called
  the directive function.
- ``attributes`` is a dictionary of extra attributes which may be added to the
  element the directive produces. Currently, only an "alt" attribute is passed
  by substitution definitions (value: the substitution name), which may by
  used by an embedded image directive.
"""

__docformat__ = 'reStructuredText'

__all__ = ['directive']

_directive_registry = {
      'restructuredtext-test-directive': ('directivetest',
                                          'directive_test_function'),
      'image': ('images', 'image'),
      'figure': ('images', 'figure'),
      'attention': ('admonitions', 'attention'),
      'caution': ('admonitions', 'caution'),
      'danger': ('admonitions', 'danger'),
      'error': ('admonitions', 'error'),
      'important': ('admonitions', 'important'),
      'note': ('admonitions', 'note'),
      'tip': ('admonitions', 'tip'),
      'hint': ('admonitions', 'hint'),
      'warning': ('admonitions', 'warning'),
      'meta': ('html', 'meta'),
      'imagemap': ('html', 'imagemap'),}
"""Mapping of directive name to (module name, function name). The directive
'name' is canonical & must be lowercase; language-dependent names are defined
in the language package."""

_modules = {}
"""Cache of imported directive modules."""

_directives = {}
"""Cache of imported directive functions."""

def directive(directivename, languagemodule):
    normname = directivename.lower()
    if _directives.has_key(normname):
        return _directives[normname]
    try:
        canonicalname = languagemodule.directives[normname]
        modulename, functionname = _directive_registry[canonicalname]
    except KeyError:
        return None
    if _modules.has_key(modulename):
        module = _modules[modulename]
    else:
        try:
            module = __import__(modulename, globals(), locals())
        except ImportError:
            return None
    try:
        function = getattr(module, functionname)
    except AttributeError:
        return None
    return function
