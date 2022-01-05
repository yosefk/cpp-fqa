import os
import imp
f2h = imp.load_source('f2h','fqa2html.py')
h2toc=imp.load_source('h2toc','toc.py')
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
