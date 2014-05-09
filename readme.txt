
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
