'''check bit-exactity of the generated snapshot with the 7 May 2008 snapshot (modulo revision date).
for the grand merge only.'''
import os
def gimme(f,pf):
	data = open(os.path.join(pf,f)).read()
	return '\n'.join([x for x in data.split('\n') if not x.startswith('<tt>revised')])

# TODO: check that the file sets are identical
files = [x for x in os.listdir('.') if x.endswith('.html')]

for f in files:
	finalc = gimme(f,'..\\final-html')
  	localc = gimme(f,'.')
	if finalc != localc:
		print f,'DIFFERS!!'
	else:
		print f,'identical'
