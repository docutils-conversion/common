<?xml version="1.0" encoding="ISO-8859-1"?>
<!--

XSLT stylesheet for transforming the XML from Restructured Text into
HTML suitable for a web page.

(c) Paul Wright  2001. You may modify and/or distribute the source for
this stylesheet under the same licence terms as Python itself.

-->

<xsl:stylesheet 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
  version="1.0"
  >

  <xsl:output method="html"/>

  <xsl:template match="/">
  	<HTML>
	<xsl:apply-templates/>
	</HTML>
  </xsl:template>

  <xsl:template match="/document">
  	<HEAD>
	<TITLE>
	<xsl:value-of select="title"/>
	</TITLE>
	</HEAD>
  	<BODY>
	<xsl:apply-templates/>
	<!-- After the main document, add the footnotes -->
	<HR/>
	<H2>Footnotes</H2>
	<xsl:for-each select="footnote">
		<xsl:apply-templates select="." mode="footer"/>
	</xsl:for-each>
	</BODY>
  </xsl:template>

  <!-- Top level heading -->
  <xsl:template match="/document/title">
  	<CENTER><H1>
	<xsl:apply-templates/>
	</H1></CENTER>
  </xsl:template>

	<xsl:template match="/document/author">
		<STRONG>Author:</STRONG>
		<xsl:apply-templates/>
		<BR/>
	</xsl:template>

	<xsl:template match="/document/contact">
		<STRONG>Contact:</STRONG>
		<xsl:apply-templates/>
		<BR/>
	</xsl:template>

	<xsl:template match="/document/date">
		<STRONG>Date:</STRONG>
		<xsl:apply-templates/>
		<BR/>
	</xsl:template>

  <xsl:template match="/document/section/title">
  	<H2>
	<xsl:apply-templates/>
	</H2>
  </xsl:template>

  <xsl:template match="/document/section/section/title">
  	<H3>
	<xsl:apply-templates/>
	</H3>
  </xsl:template>

  <xsl:template match="/document/section/section/section/title">
  	<H4>
	<xsl:apply-templates/>
	</H4>
  </xsl:template>

  <xsl:template match="paragraph">
  	<P>
	<xsl:apply-templates/>
	</P>
  </xsl:template>

  <xsl:template match="bullet_list">
  	<UL>
	<xsl:apply-templates/>
	</UL>
  </xsl:template>
  
  <xsl:template match="enumerated_list">
  	<OL>
	<xsl:apply-templates/>
	</OL>
  </xsl:template>

  <xsl:template match="list_item">
  	<LI>
	<xsl:apply-templates/>
	</LI>
  </xsl:template>

  <xsl:template match="literal_block">
  	<PRE>
	<xsl:value-of select="text()"/>
	</PRE>
  </xsl:template>

	<xsl:template name="htmLink">
		<xsl:param name="dest" select="UNDEFINED"/>
		<xsl:element name="A">
			<xsl:attribute name="HREF">
				<xsl:value-of select="$dest"/>
			</xsl:attribute>
			<xsl:apply-templates/>
		</xsl:element>
	</xsl:template>

	<xsl:template match="link">
		<!-- Straight link -->
		<xsl:if test="@refuri">
			<xsl:call-template name="htmLink">
				<xsl:with-param name="dest" select="@refuri"/>
			</xsl:call-template>
		</xsl:if>
		<xsl:if test="@refname">
			<xsl:param name="tname" select="@refname"/>
			<xsl:param name="tvalue" select="normalize-space(//target[@name=$tname])"/>
			<!-- Callout version of cross ref (most
			suitable for use on the web, I think) -->
			<xsl:if test="$tvalue">
				<xsl:call-template name="htmLink">
					<xsl:with-param name="dest" select="$tvalue"/>
				</xsl:call-template>
			</xsl:if>
			<!-- Internal cross reference -->
			<xsl:if test="not($tvalue)">
				<xsl:call-template name="htmLink">
					<xsl:with-param name="dest" select="concat('#',$tname)"/>
				</xsl:call-template>
			</xsl:if>
		</xsl:if>
	</xsl:template>

	<xsl:template match="footnote_reference">
		<!-- Add an anchor so we can come back here. -->
		<xsl:element name="A">
			<xsl:attribute name="NAME">
				<xsl:value-of select="concat('back_',
				@refname)"/>
			</xsl:attribute>
		</xsl:element>
		<!-- Link to footnote. -->
		<xsl:call-template name="htmLink">
			<xsl:with-param name="dest" select="concat('#',@refname)"/>
		</xsl:call-template>
	</xsl:template>

	<!-- If we're not at the bottom of the text, throw footnotes
	away -->
	<xsl:template match="footnote">
	</xsl:template>

	<!-- Use footer mode to get the footnotes at the bottom -->
	<xsl:template match="footnote" mode="footer">
		<xsl:apply-templates/>
	</xsl:template>

	<xsl:template match="footnote/label">
		<xsl:param name="refname"
		select="parent::*/attribute::name"/>
		<xsl:element name="A">
			<xsl:attribute name="NAME">
				<xsl:value-of select="$refname"/>
			</xsl:attribute>
		</xsl:element>
		<B>
		<xsl:element name="A">
			<xsl:attribute name="HREF">
				<xsl:value-of select="concat ('#back_',
					$refname)"/>
			</xsl:attribute>
			<xsl:value-of select="normalize-space(text())"/>
		</xsl:element>:</B>
	</xsl:template>
	

	<xsl:template match="section">
		<xsl:element name="A">
			<xsl:attribute name="NAME">
				<xsl:value-of select="@name"/>
			</xsl:attribute>
		</xsl:element>
		<xsl:apply-templates/>
	</xsl:template>

	<xsl:template match="target">
		<xsl:element name="A">
			<xsl:attribute name="NAME">
				<xsl:value-of select="@name"/>
			</xsl:attribute>
		</xsl:element>
	</xsl:template>

	<xsl:template match="emphasis">
		<EM><xsl:apply-templates/></EM>
	</xsl:template>

	<xsl:template match="strong">
		<STRONG><xsl:apply-templates/></STRONG>
	</xsl:template>


	<xsl:template match="field_list">
		<TABLE CELLPADDING='2'>
		<xsl:apply-templates/>
		</TABLE>
		<BR CLEAR="all"/>
	</xsl:template>

	<xsl:template match="field">
		<TR>
		<xsl:apply-templates/>
		</TR>
	</xsl:template>

	<xsl:template match="field_name">
		<TH>
		<xsl:apply-templates/>
		</TH>
	</xsl:template>

	<xsl:template match="field_body">
		<TD>
		<xsl:apply-templates/>
		</TD>
	</xsl:template>

	<xsl:template match="block_quote">
		<BLOCKQUOTE>
		<xsl:apply-templates/>
		</BLOCKQUOTE>
	</xsl:template>

	<xsl:template match="definition_list">
		<DL>
		<xsl:apply-templates/>
		</DL>
	</xsl:template>

	<xsl:template match="term">
		<DT>
		<xsl:apply-templates/>
		</DT>
	</xsl:template>

	<xsl:template match="definition">
		<DD>
		<xsl:apply-templates/>
		</DD>
	</xsl:template>

	<xsl:template match="literal">
		<samp>
		<xsl:value-of select="text()"/>
		</samp>
	</xsl:template>

	<xsl:template match="table">
		<TABLE BORDER='1' CELLPADDING='1'>
		<xsl:apply-templates/>
		</TABLE>
	</xsl:template>

	<xsl:template match="tgroup">
		<!-- XXX: What's this for? -->
		<xsl:apply-templates/>
	</xsl:template>

	<xsl:template match="thead">
		<xsl:apply-templates/>
	</xsl:template>
			
	<xsl:template match="row">
		<TR>
		<xsl:apply-templates/>
		</TR>
	</xsl:template>

	<xsl:template match="//thead/row/entry">
		<xsl:element name="TH">
			<xsl:if test="@morecols">
				<xsl:attribute name="COLSPAN">
					<xsl:value-of select="@morecols + 1"/>
				</xsl:attribute>
			</xsl:if>
			<xsl:if test="@morerows">
				<xsl:attribute name="ROWSPAN">
					<xsl:value-of select="@morerows + 1"/>
				</xsl:attribute>
			</xsl:if>
			<xsl:apply-templates/>
		</xsl:element>
	</xsl:template>			

	<xsl:template match="//tbody/row/entry">
		<xsl:element name="TD">
			<xsl:if test="@morecols">
				<xsl:attribute name="COLSPAN">
					<xsl:value-of select="@morecols + 1"/>
				</xsl:attribute>
			</xsl:if>
			<xsl:if test="@morerows">
				<xsl:attribute name="ROWSPAN">
					<xsl:value-of select="@morerows + 1"/>
				</xsl:attribute>
			</xsl:if>
			<xsl:apply-templates/>
		</xsl:element>
	</xsl:template>			

</xsl:stylesheet>


