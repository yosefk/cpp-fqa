#!/opt/python-2.3.5_mob/bin/python
# -*- coding: utf-8 -*-
'''convert a C++ FQA page to HTML'''
import sys
import re
import os

site = os.environ.get('FQA_SITE','') #'http://geocities.com/yossi_kreinin/'

# in October 2007, parashift.com disappeared from the DNS
faq_site = 'http://www.parashift.com/c++-faq-lite'
#faq_site = 'http://www.dietmar-kuehl.de/mirror/c++-faq'
#faq_site = 'http://www.ensta.fr/~diam/c++/online/c++-faq-lite'

style = '''
  <style type='text/css'>
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
  </style>
'''

import time
end_of_doc = '''
<hr>
<small class="part">Copyright \xc2\xa9 2007 <a href="http://yosefk.com">Yossi Kreinin</a><br>
<tt>revised %s</tt></small>
</body>
</html>'''%(time.strftime('%d %B %Y',time.localtime()))

re_link = re.compile('\\[http:([^ ]+) ([^\\]]+)\\]')
re_int = re.compile('\\[(\\d+)\\.(\\d+) ([^\\]]+)\\]')
re_corr = re.compile('\\[corr\\.(\\d+) ([^\\]]+)\\]')

num2sec = {
   6: 'picture',
   7: 'class',
   8: 'ref',
   9: 'inline',
   10: 'ctors',
   11: 'dtor',
   12: 'assign',
   13: 'operator',
   14: 'friend',
   15: 'io',
   16: 'heap',
   17: 'exceptions',
   18: 'const',
   19: 'inheritance-basics',
   20: 'inheritance-virtual',
   21: 'inheritance-proper',
   22: 'inheritance-abstract',
   23: 'inheritance-mother',
   25: 'inheritance-multiple',
   27: 'smalltalk',
   32: 'mixing',
   33: 'function',
   35: 'templates',
}

def main():
  if len(sys.argv)!=2:
    raise Exception('usage: %s <input C++ FQA text>'%sys.argv[0])
  run(sys.argv[1])

def run_to(arg,stream):
  try:
    oldout = sys.stdout
    sys.stdout = stream
    run(arg)
  finally:
    sys.stdout = oldout

def doit(arg):
  run_to(arg+'.fqa',open(arg+'.html','wb'))
  
def run(arg):
  fqa = open(arg)
  fqa_page = arg.replace('.fqa','.html')

  # escape sequences with beginnings and endings, for example:
  # /xxx/ => <i>xxx</i>
  esc2mark = {
    '/':('<i>','</i>'),
    '|':('<tt>','</tt>'),
    '@':('<pre>','</pre>'),
  }
  # html entities
  plain2html = {
    '"':'&quot;',
    "'":'&#39;',
    '&':'&amp;',
    '<':'&lt;',
    '>':'&gt;',
  }

  def replace_html_ent(s):
    'see also str2html. this one is for titles'
    o = ''
    for x in s:
      o += plain2html.get(x) or x
    return o

  def replace_links(s):
    def rl(m):
      g=m.groups()
      return '`<a href="http:%s">%s</a>`'%(g[0],g[1])
    def ri(m):
      g=m.groups()
      snum=int(g[0])
      sec=num2sec[snum]
      num=int(g[1])
      cap=g[2]
      return '`<a href="%s%s.html#fqa-%d.%d">%s</a>`'%(site,sec,snum,num,cap)
    def rc(m):
      g=m.groups()
      num=int(g[0])
      cap=g[1]
      return '`<a class="corr" href="web-vs-fqa.html#correction-%d">%s</a>`'%(num,cap)
    s = re_link.sub(rl,s)
    s = re_int.sub(ri,s)
    s = re_corr.sub(rc,s)
    return s

  def str2html(p):
    '''convert a string to html (escaping and fqa markup)'''

    p = replace_links(p)
    
    op = ''
    i = 0
    esc2state = {}
    ek = esc2mark.keys()
    for k in ek:
      esc2state[k]=0
    pk = plain2html.keys()
    asis = False
    while i<len(p):
      c = p[i]
      if c == '`':
        asis = not asis
      elif not asis and c == '\\':
        i+=1
        if i<len(p):
          op += p[i]
      elif not asis and c in ek:
        op += esc2mark[c][esc2state[c]]
        esc2state[c] = 1-esc2state[c]
      elif not asis and c in pk:
        op += plain2html[c]
      else:
        op += c
      i+=1
        
    return op
    
  def read_paragraph():
    '''a paragraph is a bunch of non-blank lines'''

    p = ''
    line = fqa.readline()
    while line.strip() != '':
      p += line
      line = fqa.readline()
    if p.strip() == '':
      return None
    return str2html(p.strip())

  def print_paragraph(p):
    print '<p>'
    print p
    print '</p>'
    print

  # first line: page title
  title = fqa.readline()[:-1]

  def print_heading(faq_page):
    if faq_page:
      below_heading = '''<small class="part">Part of <a href="index.html">C++ FQA Lite</a>.
      To see the original answers, follow the </small><b class="FAQ"><a href="%s/%s">FAQ</a></b><small class="part"> links.</small><hr>'''%(faq_site,faq_page)
    elif 'Main page' not in title:
      below_heading = '''<small class="part">Part of <a href="index.html">C++ FQA Lite</a></small><hr>'''
    else:
      below_heading = ''
      
    title_titag = 'C++ FQA Lite: '+title
    title_h1tag = title
    if 'Main page' in title:
      title_titag = 'C++ Frequently Questioned Answers'
      title_h1tag = 'C++ FQA Lite: Main page'
    print '''<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
<html>
  <head>
  <title>%s</title>
  %s
  </head>
  <body>
  <h1>%s</h1>
  %s
  '''%(replace_html_ent(title_titag),style,replace_html_ent(title_h1tag),below_heading)

  # second line: attributes
  attrs = eval(fqa.readline())
  if len(attrs):
    section = attrs['section']
    faq_page = attrs['faq-page']
    print_heading(faq_page)
  else:
    print_heading(None)
    # this isn't a FAQ section - read and print all paragraphs
    while 1:
      p = read_paragraph()
      if p:
        print_paragraph(p)
      else:
        print end_of_doc
        return
  #print 'formatting C++ FQA page %s (FAQ page: %s, section number %d)'%(title,faq_page,section)

  # we get here if this is a FAQ section
  class Question:
    def __init__(self,title,faq,fqa):
      self.title = title # one paragraph
      self.faq = faq # list of paragraphs
      self.fqa = fqa # list of paragraphs

    def toc_line(self,num):
      return '<li><a href="%s#fqa-%d.%d">[%d.%d] %s</a></li>'%(fqa_page,section,num,section,num,self.title)

    def title_lines(self,num):
      return '''<a name="fqa-%(sec)d.%(num)d"></a>\n<h2>[%(sec)d.%(num)d] %(title)s</h2>\n'''%{'sec':section,'num':num,'title':self.title}

    def replace_faq(self,num):
      repstr = '<b class="FAQ"><a href="%s/%s#faq-%s.%s">FAQ:</a></b>\n'%(faq_site,faq_page,section,num)
      self.faq[0]=self.faq[0].replace('FAQ:',repstr)

    def replace_fqa(self):
      repstr = '<b class="FQA">FQA:</b>'
      self.fqa[0]=self.fqa[0].replace('FQA:',repstr)

  def read_question():
    '''format:

    what's up?

    FAQ: um. this, and
    this.

    and this.

    FQA: no, that, or maybe
    that, or...

    that.

    -END
    '''
    
    title = read_paragraph()
    if title == None:
      return None

    faqps = [read_paragraph()]
    while 'FQA:' not in faqps[-1]:
      if p.strip() == '':
        return None
      faqps.append(read_paragraph())

    fqaps = [faqps.pop()]
    while '-END' not in fqaps[-1]:
      fqaps.append(read_paragraph())

    fqaps.pop()
      
    return Question(title,faqps,fqaps)

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
  print '<ul>'
  for i,q in enumerate(qs):
    print q.toc_line(i+1)
  print '</ul>'

  # print the questions

  for i,q in enumerate(qs):
    n=i+1
    print
    print q.title_lines(n)

    q.replace_faq(n)
    for p in q.faq:
      print_paragraph(p)

    q.replace_fqa()
    for p in q.fqa:
      print_paragraph(p)

  # end
  print end_of_doc

