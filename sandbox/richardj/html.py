import cStringIO, cgi, sys, urllib
import dps.utils
try:
    from restructuredtext import Parser
except ImportError:
    from dps.parsers.restructuredtext import Parser

class DumbHTMLFormatter:
    def __init__(self, document):
        self.out = cStringIO.StringIO()
        self.w = self.out.write
        self.section = 0
        self.closers = []
        self.document = document

    def format(self, node=None):
        if node is None:
            node = self.document
        for entry in node:
            if entry.tagname == '#text':
                meth = self.format__text
            else:
                meth = getattr(self, 'format_'+entry.tagname)
            meth(entry)
        return self.out.getvalue()

    def format_section(self, node):
        self.w('<a name="%s"></a>'%urllib.quote(node.attributes['name']))
        self.section += 1
        if node.children: self.format(node)
        self.section -= 1

    def format_title(self, node):
        self.w('<h%d>'%self.section)
        if node.children: self.format(node)
        self.w('</h%d>'%self.section)

    def format_paragraph(self, node):
        self.w('<p>')
        if node.children: self.format(node)
        self.w('</p>')

    def format_bullet_list(self, node):
        ''' +------+----------------------+
            | "- " | list item            |
            +------| (body elements)+     |
                   +----------------------+
        '''
        # TODO: handle attributes
        self.w('<ul>')
        if node.children: self.format(node)
        self.w('</ul>')

    def format_enumerated_list(self, node):
        ''' +-------+----------------------+
            | "1. " | list item            |
            +-------| (body elements)+     |
                    +----------------------+
        '''
        # TODO: handle attributes
        self.w('<ol>')
        if node.children: self.format(node)
        self.w('</ol>')

    def format_list_item(self, node):
        self.w('<li>')
        if node.children: self.format(node)

    def format_definition_list(self, node):
        self.w('<dl>')
        if node.children: self.format(node)
        self.w('</dl>')

    def format_definition_list_item(self, node):
        '''  +---------------------------+
             | term [ " : " classifier ] |
             +--+------------------------+--+
                | definition                |
                | (body elements)+          |
                +---------------------------+
        '''
        self.w('<dt>')
        if node.children: self.format(node)

    def format_term(self, node):
        self.w('<span class="term">')
        if node.children:self.format(node)
        self.w('</span>')

    def format_classifier(self, node):
        self.w('<span class="classifier">')
        if node.children: self.format(node)
        self.w('</span>')

    def format_definition(self, node):
        self.w('</dt><dd>')
        if node.children: self.format(node)
        self.w('</dd>')

    def format_literal(self, node):
        self.w('<tt>')
        if node.children: self.format(node)
        self.w('</tt>')

    def format_reference(self, node):
        attrs = node.attributes
        doc = self.document
        ok = 1
        if attrs.has_key('refuri'):
            self.w('<a href="%s">'%attrs['refuri'])
        elif doc.explicit_targets.has_key(attrs['refname']):
            # an external reference has been defined
            ref = doc.explicit_targets[attrs['refname']]
            self.w('<a href="%s">'%ref.attributes['refuri'])
        elif doc.implicit_targets.has_key(attrs['refname']):
            # internal reference
            name = attrs['refname']
            self.w('<a href="#%s">'%urllib.quote(name))
        else:
            ok = 0
            self.w('<span class="html_formatter-ERROR">target "%s" '
                'undefined</span>'%attrs['refname'])
        if node.children: self.format(node)
        if ok:
            self.w('</a>')

    def format_literal_block(self, node):
        self.w('<pre>')
        if node.children: self.format(node)
        self.w('</pre>')

    def format_emphasis(self, node):
        self.w('<em>')
        if node.children: self.format(node)
        self.w('</em>')

    def format_strong(self, node):
        self.w('<strong>')
        if node.children: self.format(node)
        self.w('</strong>')

    def format_block_quote(self, node):
        self.w('<blockquote>')
        if node.children: self.format(node)
        self.w('</blockquote>')

    def format_doctest_block(self, node):
        self.w('<pre>')
        if node.children: self.format(node)
        self.w('</pre>')

    def format_system_message(self, node):
        self.w('<span class="system_message-%s">'%node.attributes['type'])
        if node.children: self.format(node)
        self.w('</span>')

    def format__text(self, node):
        self.w(cgi.escape(node.data))

    def format_comment(self, node):
        self.w('<!--')
        if node.children: self.format(node)
        self.w('-->')

    def format_field_list(self, node):
        if node.children: self.format(node)

    def format_field(self, node):
        '''  +------------------------------+------------+
             | ":" name (" " argument)* ":" | field body |
             +-------+----------------------+            |
                     | (body elements)+                  |
                     +-----------------------------------+
        '''
        self.w('<dt>')
        if node.children: self.format(node)

    def format_field_name(self, node):
        self.w('<span class="field_name">')
        if node.children:self.format(node)
        self.w('</span>')

    def format_field_argument(self, node):
        self.w('<span class="field_argument">')
        if node.children: self.format(node)
        self.w('</span>')

    def format_field_body(self, node):
        self.w('</dt><dd>')
        if node.children: self.format(node)
        self.w('</dd>')

    def format_target(self, node):
        '''Do nothing
        '''
        pass

# TODO:

# Option List:
#       option_list, option_list_item, option, short_option,
#       long_option, vms_option, option_argument, description.
#       
#   +--------------------------------+-------------+
#   | "-" letter [" " argument] "  " | description |
#   +-------+------------------------+             |
#           | (body elements)+                     |
#           +--------------------------------------+
#
# Tables:
#       table, tgroup, colspec, thead, tbody, row, entry.
#      
#   +------------------------+------------+----------+----------+
#   | Header row, column 1   | Header 2   | Header 3 | Header 4 |
#   | (header rows optional) |            |          |          |
#   +========================+============+==========+==========+
#   | body row 1, column 1   | column 2   | column 3 | column 4 |
#   +------------------------+------------+----------+----------+
#   | body row 2             | Cells may span columns.          |
#   +------------------------+------------+---------------------+
#   | body row 3             | Cells may  | - Table cells       |
#   +------------------------+ span rows. | - contain           |
#   | body row 4             |            | - body elements.    |
#   +------------------------+------------+---------------------+
#
# Bibliographic Fields:
#       docinfo, author, authors, organization, contact, version,
#       status, date, copyright, abstract.
#
# Footnotes:
#       footnote, label.
#
#    +-------+-------------------------+
#    | ".. " | "[" label "]" footnote  |
#    +-------+                         |
#            | (body elements)+        |
#            +-------------------------+
#
# 


def main(filename, debug=0):
    parser = Parser()
    input = open(filename).read()
    document = dps.utils.newdocument()
    parser.parse(input, document)
    if debug == 1:
        print document.pformat()
    else:
        formatter = DumbHTMLFormatter(document)
        print formatter.format()

if __name__ == '__main__':
    if len(sys.argv) > 2:
        main(sys.argv[1], debug=1)
    else:
        main(sys.argv[1])

