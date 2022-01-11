import ftplib
import os

fqas = [f for f in os.listdir('.') if f.endswith('.fqa')]
htmls = [f[:-4] + '.html' for f in fqas] + ['fqa.html']
print(htmls)

files = htmls#['index.html']#['defective.html','mixing.html']#htmls

os.system('zip fqa.zip %s'%' '.join(files))

print('upload and unzip fqa.zip')
import sys
sys.exit()
