from bs4 import BeautifulSoup as BS
import urllib.request as urllib2
import re

def search(url):

	html = urllib2.urlopen(url)
	soup = BS(html)
	print (url)
		#print (tag.next_element)
		#print (tag.next_element.next_element)
		#print (tag.nextsibling)
		#print (tag.nextsibling.nextsibling)
	for tag in soup.find_all("th"):
		
		tds = tag.find_all("td") # you get list
		#print('text:', tds[0].get_text()) # get element [0] from list
		#print('value:', tds[1].get_text())
		


		if tag.text=="Balance":
			print (tag.find_next("td"))#nextsibling.text)
	soup.find("th", text="Balance").find_next_sibling("td").text
			#b.body.findAll(text=re.compile('Trump wins .+? uncertain future'))
	
	#result=soup.body.findAll(text=re.compile('Balance</th>.+?</td>'))
	#print (result.text)
	'''elem =soup.findAll('td', text = re.compile(ur'Fixed text:(.*)', re.DOTALL), attrs = {'class': 'pos'})#('a', {'title': 'title here'})
	# <th scope="row">Balance</th><td>0.950165999 
	elem[0].text'''


search("https://explorer.xdag.io/block/5+q")
print ("searching")
f = open("addrlist.csv", 'r')
data = f.read()
rows = data.split('\n')

for row in rows:
	search("https://explorer.xdag.io/block/"+row)
