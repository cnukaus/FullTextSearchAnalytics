import mysql.connector
from mysql.connector import Error
import configparser


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


def db_connect(config):
    #https://stackoverflow.com/questions/42906665/import-my-database-connection-with-python
    

    try:
        
        dbconn = mysql.connector.connect(host = config['mysqlDB']['host'],
                           database = config['mysqlDB']['database'],user = config['mysqlDB']['user'],
                           password = config['mysqlDB']['password']
                           )

        
        if dbconn.is_connected():
            print('Connected to MySQL database')
            return dbconn
        
    
    except mysql.connector.Error as e:
        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Passwort // Username")
        elif e.errno == errorcode.ER_BAD_DB_ERROR:
            print("DataBase does not exist")
        else:
            print(e)
        #print ("dberr"+str(err))
    
    
def returnTopX(conn,asset,num,version=0):
	sql="select balance, create_time from balance_history where asset_type='"+asset+"'"
	if date>'1990-01-01':
		
		sql=sql+" and date>"
	sql=sql+" order by create_time desc"
	try:
		
	    cursor = dbconn.cursor()
	    cursor.execute(sql)

	    result=[cursor.fetchone() for i in range(cursor.rowcount) if i<2]
        
	    if result is not None:
	    	return result[version]
	    	
	    else:
	    	return None
	
	except Exception as err:
		print (str(err))

	return listTop[wallet,balance]

def getbalance(conn,asset,addr,version=0,date='1990-01-01'):
	# version=0 means latest
	sql="select balance, create_time from balance_history where address='"+addr+"'and asset_type='"+asset+"' and version="+str(version)+""
	if date>'1990-01-01':
		
		sql=sql+" and date>"
	sql=sql+" order by version,create_Time desc"
	try:
		
	    cursor = conn.cursor()
	    cursor.execute(sql)
	    result=cursor.fetchone()
	    #result=[cursor.fetchone() for i in range(cursor.rowcount)]
        
	    if result is not None:
	    	return result
	    	
	    else:
	    	return None
	
	except Exception as err:
		print (str(err))


'''
created table ranking on CherryServer
CREATE TABLE BalanceHistory
(
    Recordid INT(11) PRIMARY KEY NOT NULL auto_increment COMMENT 'UniqueID',
    CurrencyID INT(11) COMMENT '',
    Currency VARCHAR(20) COMMENT 'Name',
    Address VARCHAR(100),
    Version INT(11),
    CreateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '',
    Balance float(24,6),
    Source VARCHAR(35) comment 'data source'
);
'''

def changedetect(PctChangedOld,PctChangedRetain): 
#?minor change is not a change? Regular inteval shouldnt be 1st priority for writing to disk, as we want to know big change ASAP
	saveCurrent_toStack()
	compare_result=compareIfChange(pctThreshold,stack,LastPersisted,1000)
	
	if compare_result['avgValueGone']/compare_result['OldValueGone'] < PctChangeOld \
	or compare_result['avgValueRetained']/compare_result['OldValueofRetained'] < PctChangedRetain :# when is a siginifcant change? avg 5%?
		persist("reduced hold")

def compareIfChange(conn,asset,pctThreshold,listTop,listPrev,totalCap=0): # ?need to detect when ranking changed? streamline??
	'''
	1 gone, 2 new, Max, Min, Avg
	'''
	listRetained=list(set(listPrev).intersection(listTop))
	listGone=list(set(listPrev)-set(listRetained))
	listNew=list(set(listTop)-set(listRetained))

	GoneTotalsize=0
	GonesizeHistory=0
	NewTotalsize=0
	RetainedTotalsize=0
	RetainedsizeHistory=0

	gone_count=0 # maybe balance not in DB so count for avg would be different
	g2_count=0
	new_count=0
	retain_count=0
	try:
		for listitem in listGone:
			#PYTHON how to evaluate a function so None can be processed in arithmatic
			print("item:"+str(listitem))
			v0=getbalance(conn,'xdag',listitem,0)
			if v0 is None:
				pass
			else:
				gone_count+=1
				GoneTotalsize+=v0[0]

			v1=getbalance(conn,'xdag',listitem,1)
			if v1 is None:
				pass
			else:
				print(v1)
				g2_count+=1
				GonesizeHistory+=v1[0] # However board moving could be due to new bought more, old no sale
		for listitem in listNew: # NEW ITEM MAY NOT BE IN DATABASE
			if asset=='xdag':
				print("xdag")
				(prt1, readlist) = search("https://explorer.xdag.io/block/",listitem)
					
				if len(prt1)>0:
					new_count+=1
					NewTotalsize+=float(prt1)
		for listitem in listRetained:
			print("itemRetain:"+str(listitem))
			v0=getbalance(conn,'xdag',listitem,0)
			if v0 is None:
				pass
			else:
				retain_count+=1
				RetainedTotalsize+=v0[0]

			v1=getbalance(conn,'xdag',listitem,1)
			if v1 is None:
				pass
			else:
				retain_count+=1
				RetainedsizeHistory+=v1[0]
		print("%d %d %d" ,gone_count,new_count,retain_count)
		return_set={'range':new_count+retain_count,
	'gone':gone_count,'OldValueGone':GonesizeHistory/g2_count,'avgValueGone':GoneTotalsize/gone_count, 
	'avgValueNew':NewTotalsize/new_count, 'OldValueofRetained':RetainedsizeHistory/retain_count,
	'avgValueRetained':RetainedTotalsize/retain_count}
	except Exception as err:
		print ("summary err"+str(err))




	#return len(listTop),Len(ListGone),GoneTotalsize/Len(ListGone)
	



	else:
		return return_set
#返回 跟踪的Top数，已消失钱包数，下板大户的下板前均值，下板后均值，新加入大户的平均值，仍在板者的之前均值，仍在板者now均值
if __name__ == '__main__':
    
	config = configparser.ConfigParser()
	config.read('dbconfig.ini')
	dbconn=db_connect(config)
	#print(getbalance(dbconn,'xdag','4DtNq71TeY9rdp/QX63mpNsEUu+xNSBv',0))
	compareIfChange(dbconn,'xdag',0.05,['4DtNq71TeY9rdp/QX63mpNsEUu+xNSBv',],['dfKdPEdqac23INOdR/juDDY1LKFRePFk','U54RHG+snKt+rzpWVv/iN3ZOaXx3MZCJ'],totalCap=0)
