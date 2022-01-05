import os
#import imp
import importlib
#import shutil

#f2h = importlib.load_source('f2h','fqa2html.py')
#h2toc=importlib.load_source('h2toc','toc.py')
f2h = importlib.machinery.SourceFileLoader('f2h','fqa2html.py').load_module()
h2toc = importlib.machinery.SourceFileLoader('h2toc','toc.py').load_module()

def doit():
    fqa = [f for f in os.listdir('.') if f.endswith('.fqa')]
    for f in fqa:
        print(f,'...')
        f2h.doit(f[:-4])

    f2h.singlepage('fqa.html')

    tocs = {
        'defective.html':'defect',
        'linking.html':'link',
        'faq.html':'faq',
        'web-vs-fqa.html':'correction',
        'web-vs-c++.html':'misfeature',
    }
    for k,v in list(tocs.items()):
        h2toc.gentoc(k,v)
doit()
exec(compile(open('tidy.py', "rb").read(), 'tidy.py', 'exec'))

#RG: move html files to html dir
html = [f for f in os.listdir('.') if f.endswith('.html')]
cwd = os.getcwd() + '/'
if not os.path.isdir(cwd + 'html'):
    os.mkdir(cwd + 'html')
for f in html:
    os.rename(cwd + f, cwd + 'html/'+f)
    #shutil.move(cwd + f, cwd + 'html/'+f)
