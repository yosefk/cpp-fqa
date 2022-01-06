#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""convert a C++ FQA page to HTML"""
import sys
import re
import os

site = os.environ.get("FQA_SITE", "")  #'http://geocities.com/yossi_kreinin/'

# in October 2007, parashift.com disappeared from the DNS
faq_site = "http://www.parashift.com/c++-faq-lite"
# faq_site = 'http://www.dietmar-kuehl.de/mirror/c++-faq'
# faq_site = 'http://www.ensta.fr/~diam/c++/online/c++-faq-lite'

style = """<style type='text/css'>
<!--
body { font-family: arial; color: black; background: white }
h2   { color: black; background-color: #ddeeff }
h1   { color: black; background-color: #ddeeff }
h5   { background-color: #eeeeee }
pre  { background-color: #eeeeee }
.part{ color: gray }
.FQA { background-color: blue; color: gold }
.FAQ { background-color: gold; color: blue }
.corr{ color: red }
-->
</style>"""

import time
import datetime

ga = open("ga.js").read()
end_of_doc = """
<hr>
<small class="part">Copyright &copy; 2007-%d <a href="http://yosefk.com">Yossi Kreinin</a><br>
<tt>revised %s</tt></small>
%s
</body>
</html>""" % (
    datetime.datetime.now().year,
    time.strftime("%d %B %Y", time.localtime()),
    ga,
)

re_link = re.compile("\\[http:([^ ]+) ([^\\]]+)\\]")
re_int = re.compile("\\[(\\d+)\\.(\\d+) ([^\\]]+)\\]")
re_corr = re.compile("\\[corr\\.(\\d+) ([^\\]]+)\\]")

num2sec = {
    6: "picture",
    7: "class",
    8: "ref",
    9: "inline",
    10: "ctors",
    11: "dtor",
    12: "assign",
    13: "operator",
    14: "friend",
    15: "io",
    16: "heap",
    17: "exceptions",
    18: "const",
    19: "inheritance-basics",
    20: "inheritance-virtual",
    21: "inheritance-proper",
    22: "inheritance-abstract",
    23: "inheritance-mother",
    25: "inheritance-multiple",
    27: "smalltalk",
    32: "mixing",
    33: "function",
    35: "templates",
}


def main():
    if len(sys.argv) != 2:
        raise Exception("usage: %s <input C++ FQA text>" % sys.argv[0])
    run(sys.argv[1])


def run_to(arg, stream, sp=False):
    try:
        oldout = sys.stdout
        sys.stdout = stream
        run(arg, sp)
    finally:
        sys.stdout = oldout


def doit(arg):
    run_to(arg + ".fqa", open(arg + ".html", "w"))


def run(arg, sp=False):
    fqa = open(arg)
    fqa_page = arg.replace(".fqa", ".html")

    # escape sequences with beginnings and endings, for example:
    # /xxx/ => <i>xxx</i>
    esc2mark = {
        "/": ("<i>", "</i>"),
        "|": ("<tt>", "</tt>"),
        "@": ("<pre>", "</pre>"),
    }
    # html entities
    plain2html = {
        '"': "&quot;",
        "'": "&#39;",
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
    }

    def replace_html_ent(s):
        "see also str2html. this one is for titles"
        o = ""
        for x in s:
            o += plain2html.get(x) or x
        return o

    def replace_links(s):
        def rl(m):
            g = m.groups()
            return '`<a href="http:%s">%s</a>`' % (g[0], g[1])

        def ri(m):
            g = m.groups()
            snum = int(g[0])
            sec = num2sec[snum]
            num = int(g[1])
            cap = g[2]
            if sp:
                sec = sp
            else:
                sec += ".html"
            return '`<a href="%s%s#fqa-%d.%d">%s</a>`' % (site, sec, snum, num, cap)

        def rc(m):
            g = m.groups()
            num = int(g[0])
            cap = g[1]
            if sp:
                sec = sp
            else:
                sec = "web-vs-fqa.html"
            return '`<a class="corr" href="%s#correction-%d">%s</a>`' % (sec, num, cap)

        s = re_link.sub(rl, s)
        s = re_int.sub(ri, s)
        s = re_corr.sub(rc, s)
        return s

    def str2html(p):
        """convert a string to html (escaping and fqa markup)"""

        p = replace_links(p)

        op = ""
        i = 0
        esc2state = {}
        ek = list(esc2mark.keys())
        for k in ek:
            esc2state[k] = 0
        pk = list(plain2html.keys())
        asis = False
        while i < len(p):
            c = p[i]
            if c == "`":
                asis = not asis
            elif not asis and c == "\\":
                i += 1
                if i < len(p):
                    op += p[i]
            elif not asis and c in ek:
                op += esc2mark[c][esc2state[c]]
                esc2state[c] = 1 - esc2state[c]
            elif not asis and c in pk:
                op += plain2html[c]
            else:
                op += c
            i += 1

        return op

    def read_paragraph():
        """a paragraph is a bunch of non-blank lines"""

        p = ""
        line = fqa.readline()
        while line.strip() != "":
            p += line
            line = fqa.readline()
        if p.strip() == "":
            return None
        return str2html(p.strip())

    def print_paragraph(p):
        print("<p>")
        print(p)
        print("</p>")
        print()

    # first line: page title
    title = fqa.readline()[:-1]

    def print_heading(faq_page):
        if sp:
            print("""<h1>%s</h1>""" % replace_html_ent(title))
            return
        if faq_page:
            below_heading = """<small class="part">Part of <a href="index.html">C++ FQA Lite</a>.
      To see the original answers, follow the </small><b class="FAQ"><a href="%s/%s">FAQ</a></b><small class="part"> links.</small><hr>""" % (
                faq_site,
                faq_page,
            )
        elif "Main page" not in title:
            below_heading = """<small class="part">Part of <a href="index.html">C++ FQA Lite</a></small><hr>"""
        else:
            below_heading = ""

        title_titag = "C++ FQA Lite: " + title
        title_h1tag = title
        if "Main page" in title:
            title_titag = "C++ Frequently Questioned Answers"
            title_h1tag = "C++ FQA Lite: Main page"
        print(
            """<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
<title>%s</title>
%s
</head>
<body>
<h1>%s</h1>
%s
  """
            % (
                replace_html_ent(title_titag),
                style,
                replace_html_ent(title_h1tag),
                below_heading,
            )
        )

    # second line: attributes
    attrs = eval(fqa.readline())
    if len(attrs):
        section = attrs["section"]
        faq_page = attrs["faq-page"]
        print_heading(faq_page)
    else:
        print_heading(None)
        # this isn't a FAQ section - read and print all paragraphs
        while 1:
            p = read_paragraph()
            if p:
                print_paragraph(p)
            else:
                if not sp:
                    print(end_of_doc)
                return
    # print 'formatting C++ FQA page %s (FAQ page: %s, section number %d)'%(title,faq_page,section)

    # we get here if this is a FAQ section
    class Question:
        def __init__(self, title, faq, fqa):
            self.title = title  # one paragraph
            self.faq = faq  # list of paragraphs
            self.fqa = fqa  # list of paragraphs

        def toc_line(self, num):
            page = fqa_page
            if sp:
                page = sp
            return '<li><a href="%s#fqa-%d.%d">[%d.%d] %s</a></li>' % (
                page,
                section,
                num,
                section,
                num,
                self.title,
            )

        def title_lines(self, num):
            return (
                """<a name="fqa-%(sec)d.%(num)d"></a>\n<h2>[%(sec)d.%(num)d] %(title)s</h2>\n"""
                % {"sec": section, "num": num, "title": self.title}
            )

        def replace_faq(self, num):
            repstr = '<b class="FAQ"><a href="%s/%s#faq-%s.%s">FAQ:</a></b>\n' % (
                faq_site,
                faq_page,
                section,
                num,
            )
            self.faq[0] = self.faq[0].replace("FAQ:", repstr)

        def replace_fqa(self):
            repstr = '<b class="FQA">FQA:</b>'
            self.fqa[0] = self.fqa[0].replace("FQA:", repstr)

    def read_question():
        """format:

        what's up?

        FAQ: um. this, and
        this.

        and this.

        FQA: no, that, or maybe
        that, or...

        that.

        -END
        """

        title = read_paragraph()
        if title == None:
            return None

        faqps = [read_paragraph()]
        while "FQA:" not in faqps[-1]:
            if p.strip() == "":
                return None
            faqps.append(read_paragraph())

        fqaps = [faqps.pop()]
        while "-END" not in fqaps[-1]:
            fqaps.append(read_paragraph())

        fqaps.pop()

        return Question(title, faqps, fqaps)

    # next paragraph is a generic page description
    p = read_paragraph()
    print_paragraph(p)

    # other paragraphs are questions
    q = read_question()
    qs = []
    while q:
        qs.append(q)
        q = read_question()

    # generate a table of contents
    print("<ul>")
    for i, q in enumerate(qs):
        print(q.toc_line(i + 1))
    print("</ul>")

    # print the questions

    for i, q in enumerate(qs):
        n = i + 1
        print()
        print(q.title_lines(n))

        q.replace_faq(n)
        for p in q.faq:
            print_paragraph(p)

        q.replace_fqa()
        for p in q.fqa:
            print_paragraph(p)

    # end
    if not sp:
        print(end_of_doc)


secindex = [
    ("picture", "Big Picture Issues"),
    ("class", "Classes and objects"),
    ("inline", "Inline functions"),
    ("ref", "References"),
    ("ctors", "Constructors"),
    ("dtor", "Destructors"),
    ("assign", "Assignment operators"),
    ("operator", "Operator overloading"),
    ("friend", "Friends"),
    ("io", "Input/output via <tt>&lt;iostream&gt;</tt> and <tt>&lt;cstdio&gt;</tt>"),
    ("heap", "Freestore management"),
    ("exceptions", "Exceptions"),
    ("const", "Const correctness"),
    ("inheritance-basics", "Inheritance - basics"),
    ("inheritance-virtual", "Inheritance - <tt>virtual</tt> functions"),
    ("inheritance-proper", "Inheritance - proper inheritance and substitutability"),
    ("inheritance-abstract", "Inheritance - abstract base classes"),
    ("inheritance-mother", "Inheritance - what your mother never told you"),
    ("inheritance-multiple", "Inheritance - multiple and <tt>virtual</tt> inheritance"),
    ("mixing", "How to mix C and C++"),
    ("function", "Pointers to member functions"),
    ("templates", "Templates"),
]

singlepageindex = """C++ Frequently Questioned Answers
{}
This is a single page version of [http://yosefk.com/c++fqa C++ FQA Lite]. C++ is a general-purpose programming language, not necessarily suitable for your special purpose. [6.18 FQA] stands for "frequently
questioned answers". This FQA is called
"lite" because it questions the answers found in `<a href="http://www.parashift.com/c++-faq-lite/index.html">C++ FAQ Lite</a>`.

The single page version does not include most "metadata" sections such as [http://yosefk.com/c++fqa/faq.html the FQA FAQ].

`<h2>Table of contents</h2>`

`<ul>
<li><a href="%(sp)s#fqa-defective">Defective C++</a> - a list of major language defects
<li>C++ Q&A, structured similarly to C++ FAQ Lite, with links to the original FAQ answers
<ul>
<li><a href="%(sp)s#fqa-picture">Big Picture Issues</a></li>
<li><a href="%(sp)s#fqa-class">Classes and objects</a></li>
<li><a href="%(sp)s#fqa-inline">Inline functions</a></li>
<li><a href="%(sp)s#fqa-ref">References</a></li>
<li><a href="%(sp)s#fqa-ctors">Constructors</a></li>
<li><a href="%(sp)s#fqa-dtor">Destructors</a></li>
<li><a href="%(sp)s#fqa-assign">Assignment operators</a></li>
<li><a href="%(sp)s#fqa-operator">Operator overloading</a></li>
<li><a href="%(sp)s#fqa-friend">Friends</a></li>
<li><a href="%(sp)s#fqa-io">Input/output via <tt>&lt;iostream&gt;</tt> and <tt>&lt;cstdio&gt;</tt></a></li>
<li><a href="%(sp)s#fqa-heap">Freestore management</a></li>
<li><a href="%(sp)s#fqa-exceptions">Exceptions</a></li>
<li><a href="%(sp)s#fqa-const">Const correctness</a></li>
<li><a href="%(sp)s#fqa-inheritance-basics">Inheritance - basics</a></li>
<li><a href="%(sp)s#fqa-inheritance-virtual">Inheritance - <tt>virtual</tt> functions</a></li>
<li><a href="%(sp)s#fqa-inheritance-proper">Inheritance - proper inheritance and substitutability</a></li>
<li><a href="%(sp)s#fqa-inheritance-abstract">Inheritance - abstract base classes</a></li>
<li><a href="%(sp)s#fqa-inheritance-mother">Inheritance - what your mother never told you</a></li>
<li><a href="%(sp)s#fqa-inheritance-multiple">Inheritance - multiple and <tt>virtual</tt> inheritance</a></li>
<li><a href="%(sp)s#fqa-mixing">How to mix C and C++</a></li>
<li><a href="%(sp)s#fqa-function">Pointers to member functions</a></li>
<li><a href="%(sp)s#fqa-templates">Templates</a></li>
</ul>
</li>
<li><a href="%(sp)s#fqa-web-vs-fqa">`FQA errors`</a> found by readers</li>
</ul>
`
"""


def singlepage(outname):
    """generate a single HTML page with: intro & index, Defective C++, Q&A sections, and FQA errors."""
    outf = open(outname, "w")
    print(
        """<!DOCTYPE html>  
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
<title>C++ Frequently Questioned Answers</title>
%s
</head>
<body>
"""
        % style,
        file=outf,
    )

    tmpfile = "sp-index.tmp.fqa"
    tf = open(tmpfile, "w")
    tf.write(singlepageindex % {"sp": outname})
    tf.close()
    run_to(tmpfile, outf, sp=outname)
    os.remove(tmpfile)

    def sec_ancor(secfname):
        print('<a name="fqa-%s"></a>' % secfname[:-4], file=outf)

    import imp

    h2toc = imp.load_source("h2toc", "toc.py")

    def sec_with_toc(filename, name):
        sec_ancor(filename)
        tmpfile = "sec-with-toc.tmp.html"
        tmp = open(tmpfile, "w")
        run_to(filename, tmp, sp=outname)
        tmp.close()
        h2toc.gentoc(tmpfile, name, outname)
        outf.write(open(tmpfile).read())
        os.remove(tmpfile)

    sec_with_toc("defective.fqa", "defect")
    for sec, title in secindex:
        sec_ancor(sec + ".fqa")
        run_to(sec + ".fqa", outf, sp=outname)
    sec_with_toc("web-vs-fqa.fqa", "correction")
    print(end_of_doc, file=outf)
    outf.close()
