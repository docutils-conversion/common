#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.3 $
:Date: $Date: 2001/09/13 02:21:13 $
:Copyright: This module has been placed in the public domain.

English-language mappings for language-dependent features of
reStructuredText.
"""

__docformat__ = 'reStructuredText'

__all__ = ['bibliographic_fields', 'author_separators', 'directives']


from dps import nodes


bibliographic_fields = {
      'title': nodes.title,
      'subtitle': nodes.subtitle,
      'author': nodes.author,
      'authors': nodes.authors,
      'organization': nodes.organization,
      'contact': nodes.contact,
      'version': nodes.version,
      'revision': nodes.revision,
      'status': nodes.status,
      'date': nodes.date,
      'copyright': nodes.copyright,
      'abstract': nodes.abstract}
"""Field name (lowcased) to node class name mapping for bibliographic fields
(field_list)."""

author_separators = [';', ',']
"""List of separator strings for the 'Authors' bibliographic field. Tried in
order."""

directives = {
      'restructuredtext-test-directive': 'restructuredtext-test-directive',
      'image': 'image',
      'figure': 'figure',
      'attention': 'attention',
      'caution': 'caution',
      'danger': 'danger',
      'error': 'error',
      'important': 'important',
      'note': 'note',
      'tip': 'tip',
      'warning': 'warning',}
"""English name to registered (in directives/__init__.py) directive name
mapping."""
