#!/usr/bin/env python3
import os, subprocess

fqas = [f for f in os.listdir(".") if f.endswith(".fqa")]
htmls = [f[:-4] + ".html" for f in fqas] + ["fqa.html"]
files = htmls  # ['function.html']

# doesn't help with bitexact since we use a new fqa2html anyway.
# bitexactexc = [line.split()[0] for line in open('..\\post-me-list.txt').read().split('\n') if len(line)]
# print bitexactexc


def getoutput(cmd):
    """commands.getoutput doesn't work on Win32"""
    tmp = "_out_.txt"
    if os.system(cmd + " > " + tmp):
        raise Exception(cmd + " FAILED")
    f = open(tmp)
    r = f.read()
    f.close()
    return r


# NOTE_: we have cleaned up some of the html and now get no warnings from tidy
# on most of the files. web-vs-c++.html gives 20 warnings because of Russian characters.
# tidy does only error checking here which is a good thing because it will replace
# those characters and they will be unreadable:
# Character codes 128 to 159 (U+0080 to U+009F) are not allowed in HTML;
# even if they were, they would likely be unprintable control characters.
# Tidy assumed you wanted to refer to a character with the same byte value in the
# specified encoding and replaced that reference with the Unicode equivalent.
# See: tidy -f qqq.txt -o xxx.html web-vs-c++.html
# ALSO: web-vs-c++.fqa was UTF-8 with BOM which tidy also mangles. We have changed it
# to UTF-8 like all the other files.
def tidy(f):
    o = getoutput('tidy -e %s 2>&1 | grep "errors were found"' % (f))
    if " 0 errors were found" or "No warnings or errors were found" in o:
        print(f + ":", o[:-1])
    else:
        raise Exception("ERRORS FOUND IN %s: %s" % (f, o[:-1]))


for f in files:
    fd = open(f)
    contents = fd.read()
    fd.close()

    tidyisms = ["ul", "pre", "h2"]
    for t in tidyisms:
        contents = contents.replace("<p>\n<%s>" % t, "<%s>" % t)
        contents = contents.replace("</%s>\n</p>\n" % t, "</%s>\n" % t)

    fd = open(f, "w")
    fd.write(contents)
    fd.close()

    tidy(f)

# print "WARNING!! i'm not tidying post-me files for bitexact.py!! FIXME!!"
