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

#######################################
# NOTE_: we have cleaned up some of the html and now get no warnings from tidy
# on most of the files. web-vs-c++.html gives 20 warnings because of Russian characters.
# tidy does only error checking here which is a good thing because it will replace
# those characters and they will be unreadable:
# Character codes 128 to 159 (U+0080 to U+009F) are not allowed in HTML;
# even if they were, they would likely be unprintable control characters.
# Tidy assumed you wanted to refer to a character with the same byte value in the
# specified encoding and replaced that reference with the Unicode equivalent.
# See: tidy -f qqq.txt -o xxx.html web-vs-c++.html
# NOTE_: web-vs-c++.fqa was UTF-8 with BOM which tidy also mangles. We have changed it
# to UTF-8 like all the other files.
# NOTE_: use -utf8 to leave char codes >= 128
# DONE: we are getting a clean bill of health now from tidy:
# friend.html: No warnings or errors were found.
# why.html: No warnings or errors were found.
# inheritance-multiple.html: No warnings or errors were found.
# function.html: No warnings or errors were found.
# inheritance-basics.html: No warnings or errors were found.
# io.html: No warnings or errors were found.
# defective.html: No warnings or errors were found.
# web-vs-c++.html: No warnings or errors were found.
# const.html: No warnings or errors were found.
# templates.html: No warnings or errors were found.
# index.html: No warnings or errors were found.
# class.html: No warnings or errors were found.
# mixing.html: No warnings or errors were found.
# changelog.html: No warnings or errors were found.
# picture.html: No warnings or errors were found.
# ref.html: No warnings or errors were found.
# inheritance-virtual.html: No warnings or errors were found.
# exceptions.html: No warnings or errors were found.
# inheritance-abstract.html: No warnings or errors were found.
# ctors.html: No warnings or errors were found.
# inheritance-mother.html: No warnings or errors were found.
# faq.html: No warnings or errors were found.
# heap.html: No warnings or errors were found.
# disclaimers.html: No warnings or errors were found.
# dtor.html: No warnings or errors were found.
# inline.html: No warnings or errors were found.
# web-vs-fqa.html: No warnings or errors were found.
# linking.html: No warnings or errors were found.
# inheritance-proper.html: No warnings or errors were found.
# assign.html: No warnings or errors were found.
# operator.html: No warnings or errors were found.
# fqa.html: No warnings or errors were found.
#######################################
def tidy(f):
    o = getoutput('tidy -e -utf8 %s 2>&1 | grep "errors were found"' % (f))
    if " 0 errors were found" or "No warnings or errors were found" in o:
        print(f + ":", o[:-1])
    else:
        raise Exception("ERRORS FOUND IN %s: %s" % (f, o[:-1]))


# RG: this fucks up correct <p>
for f in files:
    fd = open(f)
    contents = fd.read()
    fd.close()

    tidyisms = ["ul", "pre", "h2"]
    for t in tidyisms:
        # RG: fucks up and leaves one trailing </p> in index.html and fqa.html
        contents = contents.replace("<p>\n<%s>" % t, "<%s>" % t)
        contents = contents.replace("</%s>\n</p>\n" % t, "</%s>\n" % t)

    fd = open(f, "w")
    fd.write(contents)
    fd.close()

    tidy(f)

# print "WARNING!! i'm not tidying post-me files for bitexact.py!! FIXME!!"
