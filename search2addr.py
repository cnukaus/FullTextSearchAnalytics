from bs4 import BeautifulSoup as BS
import urllib.request as urllib2
import datetime
import re
import csv
import ReadGoogle
import configparser
import mysql.connector
from mysql.connector import Error
import queue
import os
import sys
from positioncalc import getbalance



# To add FirstTrans/LastTrans
# turn page
# re-insert duplicate again
# To add multi-thread for crawling networked adddresses


THRESHOLD=3000

def calcprice(filename,pricefile):
	
	
	pricedata=list(csv.reader(open(pricefile)))


	
	try:
		f = open(filename, 'r')
		data = f.read()
		rows = data.split('\n')

		totalCost=0
		totalQuantity=0

		for row in rows:
			try:
					if "input" in row:
							sign=1
					elif "output" in row:
							sign=-1
					else:
							sign=0

					quantity=''
					text= re.search("(?<=  )[\d.]+(?=  )",row).group()

					quantity=str(text).lstrip()
					date=re.search("\d{4}-\d{2}-\d{2}",row).group()
					#print ("result)"+text+","+date)
					for pricepoint in pricedata:
						index=-1
						if datetime.datetime.strptime(date,'%Y-%m-%d')>= datetime.datetime.strptime(pricepoint[1],'%d/%m/%Y'):
							index=pricedata.index(pricepoint)
						if index>-1 and datetime.datetime.strptime(date,'%Y-%m-%d') < datetime.datetime.strptime(pricedata[index+1][1],'%d/%m/%Y'):
							cost=sign*float(pricedata[index][0])*float(quantity)
							totalCost=totalCost+cost
							totalQuantity=totalQuantity+sign*float(quantity)
							#print ("cost "+str(cost))
			except Exception as msg_1013:
				print(msg_1013)




	except Exception as e:
			print(e)
	
	print ("Avg cost is %s, of %s Tokens"%(totalCost/totalQuantity,totalQuantity))



#(?<= {6})\d*\.?\d* regex

#( )\1+
#(?<=( )\1+)\d*\.?\d* regex
# +  +means as many preceding letter as possible
# d6453c7a2a7f83d9b8d51851de25a62081bec153
#curl -X POST --data '{"method":"xdag_get_block_info", "params":["dfKdPEdqac23INOdR/juDDY1LKFRePFk"], "id":1}' localhost:16005
def search(suffix,wallet):

	url=suffix+wallet
	global result
	global dt
	global db
	global THRESHOLD
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


		#print(soup.find('body').findChildren())
		try:
			for tag in soup.find_all('a', href=True):

				if tag['href'].startswith("/block/") == True and wallet not in tag['href'] and float(str(tag.parent.findNext('td').contents[0]))>THRESHOLD:
					#print("%s,%d"%(tag['href'][7:],float(str(tag.parent.findNext('td').contents[0]))))
					storeList.append(tag['href'][7:]) #remove string head '/block/'


		except Exception as err:
			print("error"+str(err))

		for tag in soup.find_all("div"):
			
			#tds = tag.find_all("td") early Aug18 # you get list
			#print('text:', tds[0].get_text()) # get element [0] from list
			#print('value:', tds[1].get_text())
			#print ("...."+tag.text+"....")
			


			if tag.text=="Balance":#tag.text.startswith("Balance"):
				bal=tag.find_next('span').text.replace(',','')
				balanceList.append(bal)
				
				#write_db(bal,wallet,dt,db,'xdag')
				
				#f = open("c:\\result.csv", 'r+')
				#f.write(url+","+bal,dt+'\n')
				#print (url+","+tag.find_next('span').text,dt+'\n')
		if len(balanceList)==0:
			balance=''
		else:
			balance=balanceList[0]
		print (wallet+" bal:" +str(balanceList))
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

def db_connect():
    
    config = configparser.ConfigParser()
    config.read(os.path.join(sys.path[0],'dbconfig.ini'))
    

    try:
        dbconn = mysql.connector.connect(host = config['mysqlDB']['host'],
                           user = config['mysqlDB']['user'],
                           passwd = config['mysqlDB']['password'],
                           db = config['mysqlDB']['database'])
        if dbconn.is_connected():
            print('Connected to MySQL database')
            return dbconn
    except Exception as err:
        print ("error"+str(err))

def write_db(conn,asset_type,address,balance,version,dt):
    query0 = "UPDATE balance_history set version=version+1 where asset_type=%s and address=%s "
    args0 =(asset_type,address)
    
    query = "INSERT INTO balance_history(asset_type,address,balance,version,create_time) " \
            "VALUES(%s,%s,%s,%s)"
    args = (asset_type, address,balance,version,dt)

 
    try:
        
 
        cursor = conn.cursor()
        cursor.execute(query0, args0)
        cursor.execute(query, args)
 
        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')
 
        conn.commit()
    except Error as error:
        print(error)
#id,create_time,asset_type,address,balance,version,detail
def get_info_db(sql,addr,version=0,date='1990-01-01'):
    # version=0 means latest
    
    if date>'1990-01-01':
        sql=sql+"select balance, create_time from balance_history where address='"+add+"'"
        sql=sql+" and date>"
    sql=sql+" order by CreateTime desc"
    try:
        dbconn = mysql.connector.connect(host='localhost',database='python_mysql',user='root',password='secret')
        if conn.is_connected():
            print('Connected to MySQL database')
            cursor = dbconn.cursor()
            cursor.execute(sql)
            results = cursor.fetchall
            for row in results:
                print (row[0])
            if count(queryresult)>=version:

                    queryresult[version]
    except Exception as err:
        print (err)


    pass
    return balance
def readcsv():
# how to threading and loop until no new addr? while true: dedup a list, move detected to another list
	global THRESHOLD
	global db
	f = open(os.path.join(sys.path[0],"addrlist.csv"), 'r+')
	data = f.read()
	rows = data.split('\n')

	newrows=[]
	dt=datetime.datetime.now()#.strftime('%Y-%m-%d')
	result=[]
	q=queue.Queue()
	written=[]

	for row in rows:
		readlist=[]  #G6jTFKRkFlKj67zIdOZJ4jMjuhCe6oOg  BLOCK as address, fails
		
		(prt1, readlist) = search("https://explorer.xdag.io/block/",row)
		v0=getbalance(db,'xdag',row,0)
		if len(prt1)>0 and row not in written and (v0 is None or float(prt1)!=v0[0]): #either not in db, or value changed
					write_db(db,'xdag',row,float(prt1),0,dt)  
					written.append(row)
			
		for NewItem in readlist:
			if NewItem not in newrows:
				newrows.append(NewItem)

	
	print("newlist")
	print(newrows)
	
	for row in newrows:
		try:
			readlist=[]  #G6jTFKRkFlKj67zIdOZJ4jMjuhCe6oOg  BLOCK as address, fails
			
			(prt1, readlist) = search("https://explorer.xdag.io/block/",row)
			if len(prt1)>0:
				print("Gen2 bal:"+prt1+" "+row)
				if float(prt1)>THRESHOLD and row not in written:
					write_db(db,'xdag',row,float(prt1),0,dt)  
					written.append(row)

			print("DERIVED"+prt1+" "+row)

			
			for NewItem in list(set(readlist)):
				if NewItem not in rows and NewItem not in newrows:
					q.put(NewItem)
					rows.append(NewItem)
					f.write(NewItem+'\n')
			while not q.empty():
					try:
						pop=q.get(False)
						print("queue search "+pop)
						(prt1, readlist) = search("https://explorer.xdag.io/block/",pop)
						if len(prt1)>0 and float(prt1)>THRESHOLD and pop not in written:
								write_db(db,'xdag',pop,float(prt1),0,dt)
								written.append(pop)
								print("Gen4 bal:"+prt1+" "+pop)
						for gen4 in readlist:
								if gen4 not in rows and gen4 not in newrows:
									q.put(gen4)
									#print("queue added "+gen4)
								
								
					except Exception as Empty:
						print("queue err"+str(Empty))
						continue
					q.task_done()
		    #for job in iter(q.get(), None):
						
				


					
		except Exception as err:
			print ("newrows err"+str(err))	
		#To make sure that you're data is written to disk, use file.flush() followed by os.fsync(file.fileno()).
		#(prt1, readlist) = search("https://explorer.xdag.io/block/"+row)
def read1k():
	global THRESHOLD
	global db
	f = open(os.path.join(sys.path[0],"addrlist.csv"), 'r+')
	data = f.read()
	rows = data.split('\n')

	newrows=[]
	dt=datetime.datetime.now()#.strftime('%Y-%m-%d')
	result=[]
	q=queue.Queue()
	written=[]

	for row in rows:
		readlist=[]  #G6jTFKRkFlKj67zIdOZJ4jMjuhCe6oOg  BLOCK as address, fails
		
		(prt1, readlist) = search("https://explorer.xdag.io/block/",row)
		v0=getbalance(db,'xdag',row,0)
		if len(prt1)>0 and row not in written and (v0 is None or float(prt1)!=v0[0]): #either not in db, or value changed
					write_db(db,'xdag',row,float(prt1),0,dt)  
					written.append(row)
			

	
		
if __name__ == "__main__": ## If we are not importing this:
#	calcprice('dfk balance.txt','pricefile.csv')

	db=db_connect()
	#search("https://explorer.xdag.io/block/","YvcUHwI9iw2kGpXFwI9qAeUy+ni6D2+g")
	read1k()
	'''
	dt=datetime.datetime.now()
	rows = ['R2eJ1N88Zsu3u74qzo+IILkrTg9RkprK']
	newrows=[]
	dt=datetime.datetime.today().strftime('%Y-%m-%d')
	result=[]
	for row in rows:
		readlist=[]  #G6jTFKRkFlKj67zIdOZJ4jMjuhCe6oOg  BLOCK as address, fails
		
		(prt1, readlist) = search("https://explorer.xdag.io/block/",row)
		
		#print(row+","+prt1)
		for NewItem in readlist:
			if NewItem not in newrows:
				newrows.append(NewItem)

	#print (rows)
	for row in newrows:
		try:
			readlist=[]  #G6jTFKRkFlKj67zIdOZJ4jMjuhCe6oOg  BLOCK as address, fails
			
			(prt1, readlist) = search("https://explorer.xdag.io/block/",row)

			for NewItem in readlist:
				if NewItem not in rows and NewItem not in newrows:
					rows.append(NewItem)
					print ("final:"+NewItem)
					f.write(NewItem+'\n')
		except:
			pass	'''

	


