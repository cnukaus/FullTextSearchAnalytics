import configparser
import mysql.connector
from mysql.connector import Error
import difflib
import os
import sys


def db_connect():
    
    config = configparser.ConfigParser()
    config.read(os.path.join(sys.path[0],'dbconfig.ini'))
    

    try:
        dbconn = mysql.connector.connect(host = config['mysqlDB']['host'],
                           user = config['mysqlDB']['user'],
                           passwd = config['mysqlDB']['password'],
                           db = config['mysqlDB']['database'],auth_plugin='mysql_native_password')
        if dbconn.is_connected():
            print('Connected to MySQL database')
            return dbconn
    except Exception as err:
        print ("error"+str(err))



def query_db(conn,asset_type,address,balance,version,dt):
    query0 = "select * from (select tb1.*,lead(balance,1) as old_balance over (partition by address order by rn) from (select address,create_time,balance,row_number() over (partition by asset_type,address order by create_time desc) as rn from api_snapshot where asset_type=%s) tb1 inner join (select address from api_snapshot group by address having count(1)>1) tb2 on tb1.address=tb2.address where rn<3) tb where (rn%2)=1"
    args0 =(asset_type)
    query="select * from(select tb1.rn,tb1.url,tb1.response,lead(tb1.response,1) over (partition by url order by rn) last_response from (select url,create_time,response,row_number() over (partition by url order by create_time desc) as rn from monitor.api_snapshot ) tb1 inner join (select url from monitor.api_snapshot group by url having count(1)>1) tb2 on tb1.url=tb2.url where rn<3) tr where rn%2=1;"
    # lag() to retrieve altenate line
#select * from (select address,create_time,balance,row_number() over (partition by address order by create_time desc) as rn from balance_history ) tb1 where rn=1
 
    d=difflib.Differ()
    try:
        
 

        cursor = conn.cursor(buffered=True)
            
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
        	print(row[1]+"\n")
        	if row[3] is None:
        		print ('row3 is none')
        	if row[2] is not None and row[3] is not None:
	        	diff=difflib.unified_diff(row[2], row[3], lineterm='')
	        	print (''.join(list(diff)))
	        cursor.close
    except Error as error:
        print(error)
c=db_connect()
query_db(c,'xdag','','','','')