#! /usr/bin/env python
"""
:Authors: David Goodger, Ueli Schlaepfer
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.1 $
:Date: $Date: 2002/01/16 02:55:11 $
:Copyright: This module has been placed in the public domain.

Transforms related to the front matter of a document (information
found before the main text):

- `DocTitle`: Used to transform a lone top level section's title to
  the document title, and promote a remaining lone top-level section's
  title to the document subtitle.

- `DocInfo`: Used to transform a bibliographic field list into docinfo
  elements.
"""

__docformat__ = 'reStructuredText'

import re
from dps import nodes, utils
from dps.transforms import TransformError, Transform


class DocTitle(Transform):

    """
	In reStructuredText_, there is no way to specify a document title
	and subtitle explicitly. Instead, we can supply the document title
	(and possibly the subtitle as well) implicitly, and use this
	two-step transform to "raise" or "promote" the title(s) (and their
	corresponding section contents) to the document level.

	1. If the document contains a single top-level section as its
	   first non-comment element, the top-level section's title
	   becomes the document's title, and the top-level section's
	   contents become the document's immediate contents. The lone
	   top-level section header must be the first non-comment element
	   in the document.

	   For example, take this input text::

		   =================
			Top-Level Title
		   =================

		   A paragraph.

	   Once parsed, it looks like this::

		   <document>
			   <section name="top-level title">
				   <title>
					   Top-Level Title
				   <paragraph>
					   A paragraph.

	   After running the DocTitle transform, we have::

		   <document name="top-level title">
			   <title>
				   Top-Level Title
			   <paragraph>
				   A paragraph.

	2. If step 1 successfully determines the document title, we
	   continue by checking for a subtitle.

	   If the lone top-level section itself contains a single
	   second-level section as its first non-comment element, that
	   section's title is promoted to the document's subtitle, and
	   that section's contents become the document's immediate
	   contents. Given this input text::

		   =================
			Top-Level Title
		   =================

		   Second-Level Title
		   ~~~~~~~~~~~~~~~~~~

		   A paragraph.

	   After parsing and running the Section Promotion transform, the
	   result is::

		   <document name="top-level title">
			   <title>
				   Top-Level Title
			   <subtitle name="second-level title">
				   Second-Level Title
			   <paragraph>
				   A paragraph.

	   (Note that the implicit hyperlink target generated by the
	   "Second-Level Title" is preserved on the "subtitle" element
	   itself.)

	Any comment elements occurring before the document title or
	subtitle are accumulated and inserted as the first body elements
	after the title(s).
    """

    def transform(self, doctree):
        self.setup_transform(doctree)
        index = doctree.findnonclass((nodes.comment, nodes.system_warning))
        if self.checkpromotioncandidate(index):
            candidate = doctree[index]
        else:
            return
        doctree.attributes.update(candidate.attributes)
        doctree[:] = candidate[:1] + doctree[:index] + candidate[1:]
        # Check for a lone second-level section.
        index = doctree.findnonclass((nodes.comment, nodes.system_warning,
                                      nodes.title)) # new title
        if self.checkpromotioncandidate(index):
            candidate = doctree[index]
        else:
            return
        # Create a subtitle element based on the title element:
        subtitle = nodes.subtitle()
        subtitle.attributes.update(candidate[0].attributes)
        subtitle[:] = candidate[0][:]
        # Put the subtitle element into the doctree
        doctree[:] = doctree[:1] + [subtitle] + doctree[1:index] + candidate[1:]
        return

    def checkpromotioncandidate(self, index):
        """
		Return 1 iff the index'th child of node should be promoted.
        """
        if index is None or len(self.doctree) > (index + 1):
            return None
        if not isinstance(self.doctree[index], nodes.section): 
            return None
        return 1


class DocInfo(Transform):

    """
	This transform is specific to the reStructuredText_ markup syntax;
	see "Bibliographic Fields" in the `reStructuredText Markup
	Specification`_ for a high-level description. This transform
	should be run *after* the `DocTitle` transform.

	Given a field list as the first non-comment element after the
	document title and subtitle (if present), registered bibliographic
	field names are transformed to the corresponding DTD elements,
	becoming child elements of the "docinfo" element.

	For example, given this document fragment after parsing::

		<document>
			<title>
				Document Title
			<field_list>
				<field>
					<field_name>
						Author
					<field_body>
						<paragraph>
							Kilgore Trout
				<field>
					<field_name>
						Status
					<field_body>
						<paragraph>
							$RCSfile: frontmatter.py,v $
			...

	After running the bibliographic field list transform, the
	resulting document tree would look like this::

		<document>
			<title>
				Document Title
			<docinfo>
				<author>
					Kilgore Trout
				<status>
					frontmatter.py
			...

	The "Status" field contained an expanded RCS keyword, which is
	normally (but optionally) cleaned up by the transform. The sole
	contents of the field body must be a paragraph containing an
	expanded RCS keyword of the form "$keyword: expansion text $". Any
	RCS keyword can be processed in any bibliographic field. The
	dollar signs and leading RCS keyword name are removed. Extra
	processing is done for the following RCS keywords:

	- "RCSfile" expands to the name of the file in the RCS or CVS
	  repository, which is the name of the source file with a ",v"
	  suffix appended. The transform will remove the ",v" suffix.

	- "Date" expands to the format "YYYY/MM/DD hh:mm:ss" (in the UTC
	  time zone). The RCS Keywords transform will extract just the
	  date itself and transform it to an ISO 8601 format date, as in
	  "2000-12-31".

	  (Since the source file for this text is itself stored under CVS,
	  we can't show an example of the "Date" RCS keyword because we
	  can't prevent any RCS keywords used in this explanation from
	  being expanded. Only the "RCSfile" keyword is stable; its
	  expansion text changes only if the file name changes.)
    """

    def transform(self, doctree):
        self.setup_transform(doctree)
        index = doctree.findnonclass((nodes.title, nodes.subtitle,
                                      nodes.comment, nodes.system_warning))
        if index is None:
            return
        candidate = doctree[index]
        if isinstance(candidate, nodes.field_list):
            biblioindex = doctree.findnonclass((nodes.title, nodes.subtitle))
            nodelist, remainder = self.extractbibliographic(candidate)
            if remainder:
                doctree[index] = remainder
            else:
                del doctree[index]
            doctree[biblioindex:biblioindex] = nodelist
        return

    def extractbibliographic(self, field_list):
        docinfo = nodes.docinfo()
        remainder = []
        bibliofields = self.language.bibliographic_fields
        abstract = None
        for field in field_list:
            try:
                name = field[0][0].astext()
                normedname = utils.normname(name)
                if not (len(field) == 2 and bibliofields.has_key(normedname)
                        and self.checkemptybibliofield(field, name)):
                    raise TransformError
                biblioclass = bibliofields[normedname]
                if issubclass(biblioclass, nodes.TextElement):
                    if not self.checkcompoundbibliofield(field, name):
                        raise TransformError
                    self.filterrcskeywords(field[1][0])
                    docinfo.append(biblioclass('', '', *field[1][0]))
                else:                   # multiple body elements possible
                    if issubclass(biblioclass, nodes.authors):
                        self.extractauthors(field, name, docinfo)
                    elif issubclass(biblioclass, nodes.abstract):
                        if abstract:
                            field[-1] += self.doctree.reporter.error(
                                  'There can only be one abstract.')
                            raise TransformError
                        abstract = nodes.abstract('', *field[1].children)
                    else:
                        docinfo.append(biblioclass('', *field[1].children))
            except TransformError:
                remainder.append(field)
                continue
        if abstract:
            docinfo.append(abstract)
        if len(docinfo) == 0:
            return [], field_list
        if remainder:
            field_list[:] = remainder
        else:
            field_list = None
        return [docinfo], field_list

    def checkemptybibliofield(self, field, name):
        if len(field[1]) < 1:
            field[-1] += self.doctree.reporter.error(
                  'Cannot extract empty bibliographic field "%s".' % name)
            return None
        return 1

    def checkcompoundbibliofield(self, field, name):
        if len(field[1]) > 1:
            field[-1] += self.doctree.reporter.error(
                  'Cannot extract compound bibliographic field "%s".' % name)
            return None
        if not isinstance(field[1][0], nodes.paragraph):
            field[-1] += self.doctree.reporter.error(
                  'Cannot extract bibliographic field "%s" containing anything '
                  'other than a single paragraph.'
                  % name)
            return None
        return 1

    rcskeywordsubstitutions = [
          (re.compile(r'\$' r'Date: (\d\d\d\d)/(\d\d)/(\d\d) [\d:]+ \$$',
                      re.IGNORECASE), r'\1-\2-\3'),
          (re.compile(r'\$' r'RCSfile: (.+),v \$$',
                      re.IGNORECASE), r'\1'),
          (re.compile(r'\$[a-zA-Z]+: (.+) \$$'), r'\1'),]

    def filterrcskeywords(self, paragraph):
        if len(paragraph) == 1 and isinstance(paragraph[0], nodes.Text):
            textnode = paragraph[0]
            for pattern, substitution in self.rcskeywordsubstitutions:
                match = pattern.match(textnode.data)
                if match:
                    textnode.data = pattern.sub(substitution, textnode.data)
                    return

    def extractauthors(self, field, name, docinfo):
        try:
            if len(field[1]) == 1:
                if isinstance(field[1][0], nodes.paragraph):
                    authors = self.authorsfrom1paragraph(field)
                elif isinstance(field[1][0], nodes.bullet_list):
                    authors = self.authorsfrombulletlist(field)
                else:
                    raise TransformError
            else:
                authors = self.authorsfromparagraphs(field)
            authornodes = [nodes.author('', '', *author)
                           for author in authors if author]
            docinfo.append(nodes.authors('', *authornodes))
        except TransformError:
            field[-1] += self.doctree.reporter.error(
                  'Bibliographic field "%s" incompatible with extraction: '
                  'it must contain either a single paragraph (with authors '
                  'separated by one of "%s"), multiple paragraphs (one per '
                  'author), or a bullet list with one paragraph (one author) '
                  'per item.'
                  % (name, ''.join(self.language.author_separators)))
            raise

    def authorsfrom1paragraph(self, field):
        text = field[1][0].astext().strip()
        if not text:
            raise TransformError
        for authorsep in self.language.author_separators:
            authornames = text.split(authorsep)
            if len(authornames) > 1:
                break
        authornames = [author.strip() for author in authornames]
        authors = [[nodes.Text(author)] for author in authornames]
        return authors

    def authorsfrombulletlist(self, field):
        authors = []
        for item in field[1][0]:
            if len(item) != 1 or not isinstance(item[0], nodes.paragraph):
                raise TransformError
            authors.append(item[0].children)
        if not authors:
            raise TransformError
        return authors

    def authorsfromparagraphs(self, field):
        for item in field[1]:
            if not isinstance(item, nodes.paragraph):
                raise TransformError
        authors = [item.children for item in field[1]]
        return authors
