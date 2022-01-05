# generate a table of contents from <h2> headers, and replace the <!-- h2toc --> comment with it
import re
h2re = re.compile('<h2>(.*)</h2>')
def gentoc(filename,name,visname=None):
    if visname==None:
	visname = filename
    f=open(filename)
    orig=f.read()
    f.close()

    headings = []
    changed = []

    c = 1
    where = None
    for line in orig.split('\n'):
        m = h2re.match(line)
        if '<!-- h2toc -->' in line:
            where = len(changed) # mark the pos where the toc must be generated
        if m:
            headings.append(m.groups()[0])
            line = '<a name="%s-%d"></a>'%(name,c) + line
            c += 1
        changed.append(line)

    if where == None:
        print 'no <!-- h2toc --> comment found in',filename,'- table of contents not generated'
        return

    toc = '<ul>\n'
    for i,subj in enumerate(headings):
        toc += '<li><a href="%s#%s-%d">%s</a></li>\n'%(visname,name,i+1,subj)
    toc += '</ul>'
    changed[where] = toc

    f = open(filename,'wb')
    f.write('\n'.join(changed))
    f.close()
