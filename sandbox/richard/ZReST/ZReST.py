# 
# $Id$
#
''' ReStructuredText Product for Zope

This Product stores two texts - a "source" text in ReStructureText format,
and a HTML "formatted" version of that text.

'''
import docutils.core, docutils.io

from Globals import InitializeClass, DTMLFile
from OFS.SimpleItem import Item
from OFS.PropertyManager import PropertyManager
from OFS.History import Historical, html_diff
from Acquisition import Implicit
from Persistence import Persistent
from AccessControl import ClassSecurityInfo
from AccessControl import ModuleSecurityInfo
from DateTime.DateTime import DateTime
modulesecurity = ModuleSecurityInfo()

modulesecurity.declareProtected('View management screens',
    'manage_addZReSTForm')
manage_addZReSTForm = DTMLFile('dtml/manage_addZReSTForm', globals())

modulesecurity.declareProtected('Add Z Roundups', 'manage_addZReST')
def manage_addZReST(self, id, title='', file='', REQUEST=None):
    """Add a ZReST product """
    # validate the instance_home
    self._setObject(id, ZReST(id, title))
    self._getOb(id).manage_upload(file)
    if REQUEST:
        return self.manage_main(self, REQUEST)

class Warnings:
    def __init__(self):
        self.messages = []
    def write(self, message):
        self.messages.append(message)

class ZReST(Item, PropertyManager, Historical, Implicit, Persistent):
    '''An instance of this class provides an interface between Zope and
       ReStructuredText for one text.
    '''
    meta_type =  'ReStructuredText Document'
    security = ClassSecurityInfo()

    def __init__(self, id, title):
        self.id = id
        self.title = title
        self.stylesheet = 'default.css'
        self.report_level = '2'
        self.source = self.formatted = ''

    # define the properties that define this object
    _properties = (
        {'id':'stylesheet', 'type': 'string', 'mode': 'w',
            'default': 'default.css'},
        {'id':'report_level', 'type': 'string', 'mode': 'w', 'default': '2'},
    )
    property_extensible_schema__ = 0

    # define the tabs for the management interface
    manage_options= ( {'label': 'Edit', 'action':'manage_main'},
                      {'label': 'View', 'action':'index_html'},
                      {'label': 'Source', 'action':'source_txt'},
                    ) \
        + PropertyManager.manage_options \
        + Historical.manage_options \
        + Item.manage_options

    # access to the source text and formatted text
    security.declareProtected('View', 'index_html')
    def index_html(self, REQUEST=None):
        ''' Getting the formatted text
        '''
        REQUEST.RESPONSE.setHeader('content-type', 'text/html')
        return self.formatted
    security.declareProtected('View', 'source_txt')
    def source_txt(self, REQUEST=None):
        ''' Getting the source text
        '''
        REQUEST.RESPONSE.setHeader('content-type', 'text/plain')
        return self.source

    # edit form, which is also the primary interface
    security.declareProtected('Edit ReStructuredText', 'manage_editForm')
    manage_main = DTMLFile('dtml/manage_editForm', globals())

    # edit action
    security.declareProtected('Edit ReStructuredText', 'manage_edit')
    def manage_edit(self, data, title, SUBMIT='Change',dtpref_cols='50',
                    dtpref_rows='20', REQUEST=None):
        '''Alias index_html to roundup's index
        '''
        self.title=str(title)
        if self._size_changes.has_key(SUBMIT):
            return self._er(data,title,SUBMIT,dtpref_cols,dtpref_rows,REQUEST)
        if data != self.source:
            self.source = data
            self.render()

        if REQUEST:
            message="Saved changes."
            return self.manage_main(self, REQUEST, manage_tabs_message=message)

    # handle edit window size changes
    _size_changes = {
        'Bigger': (5,5),
        'Smaller': (-5,-5),
        'Narrower': (0,-5),
        'Wider': (0,5),
        'Taller': (5,0),
        'Shorter': (-5,0),
    }
    def _er(self,data,title,SUBMIT,dtpref_cols,dtpref_rows,REQUEST):
        dr,dc = self._size_changes[SUBMIT]
        rows=max(1,int(dtpref_rows)+dr)
        cols=max(40,int(dtpref_cols)+dc)
        e=(DateTime('GMT') + 365).rfc822()
        resp=REQUEST['RESPONSE']
        resp.setCookie('dtpref_rows',str(rows),path='/',expires=e)
        resp.setCookie('dtpref_cols',str(cols),path='/',expires=e)
        return self.manage_main(
            self,REQUEST,title=title,__str__=self.quotedHTML(data),
            dtpref_cols=cols,dtpref_rows=rows)
    security.declarePrivate('quotedHTML')
    def quotedHTML(self,
                   text=None,
                   character_entities=(
                       (('&'), '&amp;'),
                       (("<"), '&lt;' ),
                       ((">"), '&gt;' ),
                       (('"'), '&quot;'))): #"
        if text is None: text=self.read_raw()
        for re,name in character_entities:
            if text.find(re) >= 0: text=name.join(text.split(re))
        return text


    # handle uploads too
    security.declareProtected('Edit ReStructuredText', 'manage_upload')
    def manage_upload(self, file='', REQUEST=None):
        ''' Replaces the current source with the upload.
        '''
        if isinstance(file, type('')):
            self.source = file
        else:
            self.source = file.read()
        self.render()

        if REQUEST:
            message="Saved changes."
            return self.manage_main(self, REQUEST, manage_tabs_message=message)

    security.declarePrivate('render')
    def render(self):
        ''' Render the source to HTML
        '''
        # format with strings
        pub = docutils.core.Publisher()
        pub.set_reader('restructuredtext', None, 'restructuredtext')
        pub.set_writer('html')

        # go with the defaults
        pub.set_options()

        # this is needed, but doesn't seem to do anything
        pub.options._destination = ''

        # use the stylesheet chosen by the user
        pub.options.stylesheet = self.stylesheet

        # set the reporting level to something sane
        pub.options.report_level = int(self.report_level)

        # don't break if we get errors
        pub.options.halt_level = 6

        # remember warnings
        pub.options.warning_stream = Warnings()

        # input
        pub.source = docutils.io.StringInput(pub.options)
        pub.source.source = self.source

        # output - not that it's needed
        pub.destination = docutils.io.StringOutput(pub.options)

        # parse!
        document = pub.reader.read(pub.source, pub.parser, pub.options)
        self.warnings = ''.join(pub.options.warning_stream.messages)

        # do the format
        self.formatted = pub.writer.write(document, pub.destination)


    security.declareProtected('Edit ReStructuredText', 'PUT', 'manage_FTPput')
    def PUT(self, REQUEST, RESPONSE):
        ''' Handle HTTP PUT requests
        '''
        data = REQUEST.get('BODY', '')
        if data != self.source:
            if data.startswith('.. '):
                data = data.splitlines()
                new = []
                for i in range(len(data)):
                    line = data[i]
                    if not line.startswith('.. '):
                        break
                    if line.startswith('.. stylesheet='):
                        self.stylesheet = line.split('=')[1]
                    elif line.startswith('.. report_level='):
                        self.report_level = line.split('=')[1]
                    else:
                        pass # ignore
                data = '\n'.join(new) + '\n'.join(data[i:])
            self.source = data
            self.render()
        RESPONSE.setStatus(204)
        return RESPONSE        

    manage_FTPput = PUT

    def manage_FTPget(self):
        ''' Get source for FTP download
        '''
        self.REQUEST.RESPONSE.setHeader('Content-Type', 'text/plain')
        s = [
            '.. This is a ReStructuredText Document. Initial comment lines '
                '(".. ") will be stripped.',
            '.. stylesheet='+self.stylesheet,
            '.. report_level='+self.report_level
        ]
        if self.warnings:
            s.append('.. ')
            s.append('.. ' + '\n.. '.join(self.warnings.splitlines()))
        s.append('.. ')
        return '\n'.join(s) + '\n' + self.source

    def __str__(self):
        ''' Stringfy .. return the source
        '''
        return self.quotedHTML(self.source)

    def PrincipiaSearchSource(self):
        ''' Support for searching - the document's contents are searched.
        '''
        return self.source

    def manage_historyCompare(self, rev1, rev2, REQUEST,
                              historyComparisonResults=''):
        return ZReST.inheritedAttribute('manage_historyCompare')(
            self, rev1, rev2, REQUEST,
            historyComparisonResults=html_diff(rev1.source, rev2.source))

InitializeClass(ZReST)
modulesecurity.apply(globals())


#
# $Log$
# Revision 1.2  2002/08/15 04:36:56  richard
# FTP interface and Reporter message snaffling
#
# Revision 1.1  2002/08/14 05:15:37  richard
# Zope ReStructuredText Product
#
#
#
# vim: set filetype=python ts=4 sw=4 et si
