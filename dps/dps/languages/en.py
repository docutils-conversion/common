#! /usr/bin/env python
# $Id: en.py,v 1.3 2001/09/07 02:12:28 goodger Exp $
# by David Goodger (dgoodger@bigfoot.com)

"""
This module contains English-language mappings for language-dependent
features.
"""

__all__ = ['parser', 'formatter']
__docformat__ = 'reStructuredText'


from dps import nodes


class Stuff:

    """Stores a bunch of stuff for dotted-attribute access."""

    def __init__(self, **keywordargs):
        self.__dict__.update(keywordargs)


parser = Stuff()
"""
Mappings for input parsers. Attributes:

- bibliofields: Field name (lowcased) to node class name mapping for
  bibliographic elements.
- authorseps: List of separator strings for 'Authors' fields, tried in order.
- interpreted: Interpreted text role name to node class name mapping.
- directives: Directive name to directive module name mapping.
"""

parser.bibliofields = {'title': nodes.title,
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

parser.authorseps = [';', ',']

parser.interpreted = {'package': nodes.package,
                      'module': nodes.module,
                      'class': nodes.inline_class,
                      'method': nodes.method,
                      'function': nodes.function,
                      'variable': nodes.variable,
                      'parameter': nodes.parameter,
                      'type': nodes.type,
                      'class attribute': nodes.class_attribute,
                      'classatt': nodes.class_attribute,
                      'instance attribute': nodes.instance_attribute,
                      'instanceatt': nodes.instance_attribute,
                      'module attribute': nodes.module_attribute,
                      'moduleatt': nodes.module_attribute,
                      'exception class': nodes.exception_class,
                      'exception': nodes.exception_class,
                      'warning class': nodes.warning_class,
                      'warning': nodes.warning_class,}

parser.directives = {}

formatter = Stuff()
"""
Mappings for output formatters. Attributes:

- bibliolabels: Bibliographic node class name to label text mapping.
"""

formatter.bibliolabels = {'title': 'Title',
                          'author': 'Author',
                          'authors': 'Authors',
                          'organization': 'Organization',
                          'contact': 'Contact',
                          'version': 'Version',
                          'revision': 'Revision',
                          'status': 'Status',
                          'date': 'Date',
                          'copyright': 'Copyright',}
