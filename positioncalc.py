import ReadGoogle
import mysql.connector
from mysql.connector import Error

def returnTopX():
	pass
	return listTop[wallet,balance]

def getbalance(addr,version=0,date='1990-01-01'):
	# version=0 means latest
	sql=""
	if date>'1990-01-01':
		sql="select balance, createtime from BalanceHistory where address='"+add+"'"
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
	oldValueGone=compareIfChange(pctThreshold,stack,LastPersisted,1000)[2]
	avgValueGone=compareIfChange(pctThreshold,stack,LastPersisted,1000)[3]
	OldValueofRetained=compareIfChange(pctThreshold,stack,LastPersisted,1000)[5]
	DeltaOfRetained=compareIfChange(pctThreshold,stack,LastPersisted,1000)[6]
	
	if avgValueGone/oldValueGone < PctChangeOld or OldValueofRetained :# when is a siginifcant change? avg 5%?
		persist()

def compareIfChange(pctThreshold,listTop,listPrev,totalCap=0): # ?need to detect when ranking changed? streamline??
	'''
	1 gone, 2 new, Max, Min, Avg
	'''
	listRetained=list(set(listPrev).intersection(listTop))
	listGone=list(set(listPrev)-set(listRetained))
	listNew=list(set(listTop)-set(listRetained))
	'''for listitem in listTop:
		if listitem in listPrev:
			listRetained.add(listitem)
		else:
			listNew.add(listitem)'''
	listGone = list(set(listPrev)-set(listTop))
	GoneTotalsize=0
	GonesizeHistory=0
	NewTotalsize=0
	RetainedTotalsize=0
	RetainedsizeHistory=0

	for listitem in listGone:
		#PYTHON how to evaluate a function so None can be processed in arithmatic
		GoneTotalsize+=getbalance(listitem,0)
		GonesizeHistory+=getbalance(listitem,1) # However board moving could be due to new bought more, old no sale
	for listitem in listNew:
		NewTotalsize+=getbalance(listitem,0)
	for listitem in listRetained:
		RetainedTotalsize+=getbalance(listitem,0)
		RetainedsizeHistory+=getbalance(listitem,1)





	#return len(listTop),Len(ListGone),GoneTotalsize/Len(ListGone)
	



	return rangecounted,goneCount,OldValueGone,avgValueGone, avgValueNew, OldValueofRetained,DeltaOfRetained 
#返回 跟踪的Top数，已消失钱包数，下板大户的下板前均值，下板后均值，新加入大户的平均值，仍在板者的之前均值，仍在板者均值变动
if __name__ == '__main__':
    compareIfChange(0.05,ReadGoogle.ReadGoogle('1we9iYgXDIpsPCnp5JpQBAOOyrGy-r4zNZWl2gjpiNQM','newlist'),ReadGoogle.ReadGoogle('1we9iYgXDIpsPCnp5JpQBAOOyrGy-r4zNZWl2gjpiNQM','top 2000 wallets'),totalCap=0)
