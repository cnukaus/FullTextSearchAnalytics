from bs4 import BeautifulSoup as BS
import urllib.request as urllib2
import re

def search(url):

	html = urllib2.urlopen(url)
	soup = BS(html)
		#print (tag.next_element)
		#print (tag.nextsibling)
		#print (tag.nextsibling.nextsibling)
	for tag in soup.find_all("th"):
		
		tds = tag.find_all("td") # you get list
		#print('text:', tds[0].get_text()) # get element [0] from list
		#print('value:', tds[1].get_text())
		


		if tag.text=="Balance" and tag.find_next("td") is not None:
			print (tag.find_next("td").get_text().replace("<td>",u"Balance"))#.replace("<td>",u"余额:").replace("<a href=>\"/block","Addr:"))#nextsibling.text)
			#.replace("<td>","Balance:").replace("<a href=>\"/block","Addr:")
	#soup.find("th", text="Balance").find_next_sibling("td").text
			#b.body.findAll(text=re.compile('Trump wins .+? uncertain future'))
	
	#result=soup.body.findAll(text=re.compile('Balance</th>.+?</td>'))
	#print (result.text)
	'''elem =soup.findAll('td', text = re.compile(ur'Fixed text:(.*)', re.DOTALL), attrs = {'class': 'pos'})#('a', {'title': 'title here'})
	# <th scope="row">Balance</th><td>0.950165999 
	elem[0].text'''

if __name__ == "__main__": ## If we are not importing this:
	print ("searching")
	f = open("addrlist.csv", 'r')
	data = f.read()
	rows = data.split('\n')

	for row in rows:
		search("https://explorer.xdag.io/block/"+row)
