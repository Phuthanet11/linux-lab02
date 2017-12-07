import click,json,requests
from bs4 import BeautifulSoup
from PIL import Image
from StringIO import StringIO



def getJSON(html):
	data = {}
	data['poster'] = html.find(attrs={'class':'poster'}).find('img')['src']
	json_data = json.dumps(data)
	return json_data
	
def getHTML(url):
	response = requests.get(url)
	return BeautifulSoup(response.content,'html.parser')	
	
def getURL(input):
	try:
		if input[0] == 't' and input[1] == 't':
			html = getHTML('http://www.imdb.com/title/'+input+'/')
			
		else:
			html = getHTML('https://www.google.co.in/search?q='+input)
			for cite in html.findAll('cite'):
				if 'imdb.com/title/tt' in cite.text:
					html = getHTML('http://'+cite.text)
					break
		return getJSON(html)	
	except Exception as e:
		return 'Invalid input or Network Error!'
		


@click.command()
@click.option('--as-cowboy', '-c', is_flag=True, help='Greet as a cowboy.')
@click.argument('name', default='world', required=False)
def main(name, as_cowboy):
    r = json.loads(getURL(name))
    print(type(r))
    req = requests.get(r['poster'])
    img = Image.open(StringIO(req.content))
    img.show()
