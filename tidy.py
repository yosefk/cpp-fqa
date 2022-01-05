#!/usr/bin/env python3
import os,subprocess

fqas = [f for f in os.listdir('.') if f.endswith('.fqa')]
htmls = [f[:-4] + '.html' for f in fqas] + ['fqa.html']
files = htmls#['function.html']

#doesn't help with bitexact since we use a new fqa2html anyway.
#bitexactexc = [line.split()[0] for line in open('..\\post-me-list.txt').read().split('\n') if len(line)]
#print bitexactexc

def getoutput(cmd):
  '''commands.getoutput doesn't work on Win32'''
  tmp='_out_.txt'
  if os.system(cmd+' > '+tmp):
    raise Exception(cmd + ' FAILED')
  f=open(tmp)
  r=f.read()
  f.close()
  return r

def tidy(f):
  o=getoutput('tidy -e %s 2>&1 | grep "errors were found"'%(f))
  if ' 0 errors were found' or 'No warnings or errors were found' in o:
    print(f+':',o[:-1])
  else:
    raise Exception('ERRORS FOUND IN %s: %s'%(f,o[:-1]))
  

for f in files:
  fd=open(f)
  contents = fd.read()
  fd.close()

  tidyisms = ['ul','pre','h2']
  for t in tidyisms:
    contents = contents.replace('<p>\n<%s>'%t,'<%s>'%t)
    contents = contents.replace('</%s>\n</p>\n'%t,'</%s>\n'%t)
  
  fd=open(f,'w')
  fd.write(contents)
  fd.close()

  tidy(f)

#print "WARNING!! i'm not tidying post-me files for bitexact.py!! FIXME!!"
