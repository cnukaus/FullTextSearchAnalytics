from bs4 import BeautifulSoup as BS
import urllib.request as urllib2
import re
import datetime

def calprice():
	pass
#(?<= {6})\d*\.?\d* regex
#( )\1+
#(?<=( )\1+)\d*\.?\d* regex
#curl -X POST --data '{"method":"xdag_get_block_info", "params":["dfKdPEdqac23INOdR/juDDY1LKFRePFk"], "id":1}' localhost:16005
def search(url):

	
	global result
	global dt
	#print ("search "+url)
	storeList=[]
	balanceList=[]
	try:
		
		html = urllib2.urlopen(url)
		soup = BS(html,'html.parser')
			#print (tag.next_element)
			#print (tag.nextsibling)
			#print (tag.nextsibling.nextsibling)
		
		flag=0

		for eliminate in soup.find_all('h4'):
			if eliminate.text=='Block as address':
				flag=flag+1

		if flag==0:
			return('',storeList)	#Block as transaction need to be removed


		for tag in soup.find_all('a', href=True):
			if tag['href'].startswith("/block/") == True:
			   storeList.append(tag['href'][7:]) #remove string head '/block/'


		for tag in soup.find_all("div"):
			
			tds = tag.find_all("td") # you get list
			#print('text:', tds[0].get_text()) # get element [0] from list
			#print('value:', tds[1].get_text())
			


			if tag.text=="Balance":
				balanceList.append(tag.find_next('span').text)
				result.append(url+","+tag.find_next('span').text,dt)
				f = open("result.csv", 'r+')
				f.write(url+","+tag.find_next('span').text,dt+'\n')
		#print (storeList)
		if len(balanceList)==0:
			balance=''
		else:
			balance=balanceList[0]
		#print ("bal:"+balance)
		return (balance, storeList)#.replace("<td>",u"余额:").replace("<a href=>\"/block","Addr:"))#nextsibling.text)
	except:
		return ('', storeList)			
	#soup.find("th", text="Balance").find_next_sibling("td").text
			#b.body.findAll(text=re.compile('Trump wins .+? uncertain future'))
	
	#result=soup.body.findAll(text=re.compile('Balance</th>.+?</td>'))
	#print (result.text)
	'''elem =soup.findAll('td', text = re.compile(ur'Fixed text:(.*)', re.DOTALL), attrs = {'class': 'pos'})#('a', {'title': 'title here'})
	# <th scope="row">Balance</th><td>0.950165999 
	elem[0].text'''

if __name__ == "__main__": ## If we are not importing this:
	f = open("addrlist.csv", 'r+')
	data = f.read()
	rows = data.split('\n')
	newrows=[]
	dt=datetime.datetime.today().strftime('%Y-%m-%d')
	result=[]

	for row in rows:
		readlist=[]  #G6jTFKRkFlKj67zIdOZJ4jMjuhCe6oOg  BLOCK as address, fails
		
		(prt1, readlist) = search("https://explorer.xdag.io/block/"+row)
		
		for NewItem in readlist:
			if NewItem not in newrows:
				newrows.append(NewItem)

	print (rows)
	for row in newrows:
		try:
			readlist=[]  #G6jTFKRkFlKj67zIdOZJ4jMjuhCe6oOg  BLOCK as address, fails
			
			(prt1, readlist) = search("https://explorer.xdag.io/block/"+row)

			for NewItem in readlist:
				if NewItem not in rows and NewItem not in newrows:
					rows.append(NewItem)
					print ("final:"+NewItem)
					f.write(NewItem+'\n')
		except:
			pass	
		#To make sure that you're data is written to disk, use file.flush() followed by os.fsync(file.fileno()).
		#(prt1, readlist) = search("https://explorer.xdag.io/block/"+row)
		


