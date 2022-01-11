import os

# import imp
import importlib

# import shutil

# test branch
import warnings
warnings.simplefilter('always')


# f2h = importlib.load_source('f2h','fqa2html.py')
# h2toc=importlib.load_source('h2toc','toc.py')
f2h = importlib.machinery.SourceFileLoader("f2h", "fqa2html.py").load_module()
h2toc = importlib.machinery.SourceFileLoader("h2toc", "toc.py").load_module()


def doit():
    fqa = [f for f in os.listdir(".") if f.endswith(".fqa")]
    for f in fqa:
        print(f, "...")
        f2h.doit(f[:-4])

    f2h.singlepage("fqa.html")

    tocs = {
        "defective.html": "defect",
        "linking.html": "link",
        "faq.html": "faq",
        "web-vs-fqa.html": "correction",
        "web-vs-c++.html": "misfeature",
    }
    for k, v in list(tocs.items()):
        h2toc.gentoc(k, v)


doit()
# RG: fqa.html still OK here with correct <p>
# After this <p> removed and incorrect, so tidy DOES change file?
# NONO: tidy itself is only used for checking but in tidy.py some
# incorrect contents.replace are done for <p> which leaves a single 
# </p> in the file preventing our goal of 0 tidy warnings.
# OKOK: contents.replace are needed otherwise tidy complains about <p>
# But one incorrect single </p> is left in both index.html and fqa.html
# NONO: tidy itself is incorrect for fqa.html
# It gives 244 warnings for fqa.html on all correct matching <p>s
# tidy gives line 35 column 1 - Warning: inserting implicit <p> for
# 33 <p>
# 34 <h2>Table of contents</h2>
# 35 </p>
# Looks like correct HTML
# Yossi is trying to shut up tidy by removing those <p>s but makes one
# mistake leaving one single </p> in index.html and fqa.html
# DONE: put the backtick immediately after </ul> in index.fqa and in 
# fqa2html.py
htidy = open("tidy.py", "rb")
exec(compile(htidy.read(), "tidy.py", "exec"))
htidy.close()

# RG: move html files to html dir
html = [f for f in os.listdir(".") if f.endswith(".html")]
cwd = os.getcwd() + "/"
if not os.path.isdir(cwd + "html"):
    os.mkdir(cwd + "html")
for f in html:
    os.rename(cwd + f, cwd + "html/" + f)
    # shutil.move(cwd + f, cwd + 'html/'+f)
