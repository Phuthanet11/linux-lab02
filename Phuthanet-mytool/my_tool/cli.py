import click
import requests

from PIL import Image
from StringIO import StringIO
from bs4 import BeautifulSoup

@click.command()
@click.argument('src', nargs=-1)   
@click.argument('dst', nargs=1)
def main(src, dst):
	search=""	
	for fn in src:
        	search+='%s' % (fn)+" "
	search+='%s'%(dst)
	url_search="https://www.google.co.in/search?ei=8TkhWvTLKsH-vAS--4SYDg&q="+search+"  http://www.imdb.com".replace(" ","+")
	html=requests.get(url_search)
	b=BeautifulSoup(html.content,'html.parser')
	hint="https://"+b.find_all('div',{'class':'s'})[0].div.cite.text
	src=requests.get(hint)
	b=BeautifulSoup(src.content,'html.parser')
	photo=b.find_all('div',{'class':'poster'})[0].img['src']
	req=requests.get(photo)
	img=Image.open(StringIO(req.content))  
	img.show()
