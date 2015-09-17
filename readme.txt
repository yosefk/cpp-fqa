
This is the source code for the C++ FQA published at

  http://yosefk.com/c++fqa/

software:

refresh.py - *.fqa -> *.html. master script doing it all.
fqa2html.py - converts .fqa files to .html files. does most of the work, but not all.
toc.py - module generating TOC from <h2> headings and a <!-- h2toc --> comment. modifies files inplace. follows fqa2html
tidy.py - makes the html w3c-compliant, and runs tidy to make sure it really is.
upload.py - uploads all *.html files generated from *.fqa files to yosefk.com/c++fqa. slow, but automatic.
linkimages.py - manual. generates html code for link faces (for linking.html).

data:

*.fqa - FQA sources.
*.html - final generated FQA web pages.
images are stored at the server.

syntax of *.fqa pages:

A paragraph is text between two blank lines:

 This is a paragraph.

 This is another
 paragraph.

Currently for say 2 blank lines the program barfs, sigh.

A FAQ entry looks like this:

 Question-paragraph (single line)

 FAQ: rest of paragraph

 maybe more paragraphs

 FQA: rest of paragraph

 maybe more paragraphs

 -END

The program creates a link to the C++ FAQ question at "FAQ:". In the original C++ FAQ, questions are linked to by number.
In the isocpp.org FAQ, questions have named links so if we switch to linking to isocpp.org we'd need to handle that difference.

Special syntax inside paragraph text:

 /whatever/ becomes <i>whatever</i> (italics)
 \/ becomes /, escaping the syntax above
 |whatever| becomes <tt>whatever</tt> ("teletype" font - used for code)
 [18.2 whatever] becomes a hyperlink to FQA answer 18.2.
 /[corr.3 (correction)]/ becomes a hyperlink to correction 3, in italics, with (correction) as the link text.
 [http://example.com whatever] becomes a hyperlink to example.com.
 `whatever` becomes whatever, unescaped - for instance `<` becomes <, unlike < which becomes &lt;.
   this is used for <ul>, <li>, <b> and <h2>.
 @
 paragraph
 @
   ...becomes <pre>paragraph</pre>. /whatever/ inside @...@ still becomes <i>whatever</i> so \/ must be used to spell /.

Now to the general page structure: there are two kinds of pages, FAQ-section-mirroring pages and "general" pages.
A FAQ-section-mirroring page has as its first paragraph something like this:

 Title sentence
 {'section': 40, 'faq-page': 'whatever.html'}
 Description sentences

The dictionary is used for question numbering and hyperlink generation.

A "general" page looks like this:

 Title sentence
 {}
 Description sentences

 Possibly more paragraphs

 `<!-- h2toc -->

 `<h2>`heading`</h2>`

 Paragraphs

 `<h2>`another heading`</h2>`

 More paragraphs

 ...

Here the "table of contents" - links at the top of the page - is generated from hand-coded <h2> headings
(unlike FAQ-section-mirroring pages where it's generated from question titles.)

