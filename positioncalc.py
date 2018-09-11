import mysql.connector
from mysql.connector import Error
import configparser

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
	sql="select balance, createtime from balance_history where asset_type='"+asset+"'"
	if date>'1990-01-01':
		
		sql=sql+" and date>"
	sql=sql+" order by CreateTime desc"
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

def getbalance(conn,addr,version=0,date='1990-01-01'):
	# version=0 means latest
	sql="select balance, createtime from balance_history where address='"+addr+"'"
	if date>'1990-01-01':
		
		sql=sql+" and date>"
	sql=sql+" order by CreateTime desc"
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

def compareIfChange(conn,pctThreshold,listTop,listPrev,totalCap=0): # ?need to detect when ranking changed? streamline??
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

	for listitem in listGone:
		#PYTHON how to evaluate a function so None can be processed in arithmatic
		GoneTotalsize+=getbalance(conn,listitem,0)
		GonesizeHistory+=getbalance(conn,listitem,1) # However board moving could be due to new bought more, old no sale
	for listitem in listNew:
		NewTotalsize+=getbalance(conn,listitem,0)
	for listitem in listRetained:
		RetainedTotalsize+=getbalance(conn,listitem,0)
		RetainedsizeHistory+=getbalance(conn,listitem,1)





	#return len(listTop),Len(ListGone),GoneTotalsize/Len(ListGone)
	



	return {'range':rangecounted,
	'gone':goneCount,'OldValueGone':OldValueGone,'avgValueGone':avgValueGone, 
	'avgValueNew':avgValueNew, 'OldValueofRetained':OldValueofRetained,
	'avgValueRetained':avgValueRetained}
#返回 跟踪的Top数，已消失钱包数，下板大户的下板前均值，下板后均值，新加入大户的平均值，仍在板者的之前均值，仍在板者now均值
if __name__ == '__main__':
    
	config = configparser.ConfigParser()
	config.read('dbconfig.ini')
	dbconn=db_connect(config)
	print(getbalance(dbconn,'4DtNq71TeY9rdp/QX63mpNsEUu+xNSBv',0))#compareIfChange(dbconn,0.05,['4DtNq71TeY9rdp/QX63mpNsEUu+xNSBv',],['dfKdPEdqac23INOdR/juDDY1LKFRePFk','U54RHG+snKt+rzpWVv/iN3ZOaXx3MZCJ'],totalCap=0)
