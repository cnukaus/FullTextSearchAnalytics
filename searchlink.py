from BeautifulSoup import BeautifulSoup as BS
import urllib2

def search(url):

	html = urllib2.urlopen(your_site_here)
	soup = BS(html)
	for tag in soup.find_all("b"):
		if tag.text=="Balance":
			print (tag.nextsibling.text)
	'''elem =soup.findAll('td', text = re.compile(ur'Fixed text:(.*)', re.DOTALL), attrs = {'class': 'pos'})#('a', {'title': 'title here'})
	# <th scope="row">Balance</th><td>0.950165999 
	elem[0].text'''


search("https://explorer.xdag.io/block/5+q4Gngmh4abfnPkrOyMoGLUhhRAiXBt")

f = open("addrlist.csv", 'r')
data = f.read()
rows = data.split('\n')

for row in rows:
	print (search(url))
