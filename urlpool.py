# -*- coding: utf-8 -*-

import concurrent.futures
import requests
import queue
import threading

import datetime
import ReadGoogle
import urllib.request as req
import mysql.connector
from mysql.connector import Error
import configparser

import json_parse



# Time interval (in seconds)
INTERVAL = 10 * 60

# The number of worker threads
MAX_WORKERS =4 

# You should set up request headers
# if you want to better evade anti-spider programs
HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    #'Host': None,
    'If-Modified-Since': '0',
    #'Referer': None,
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
}

############################
def db_connect(config):
    #https://stackoverflow.com/questions/42906665/import-my-database-connection-with-python
    

    try:
        
        dbconn = mysql.connector.connect(host = config['mysqlDB']['host'],
                           database = config['mysqlDB']['database'],user = config['mysqlDB']['user'],
                           password = config['mysqlDB']['password']
                           ,auth_plugin='mysql_native_password')

       
        
    
    except Exception as err:
        print ("exception"+err)
    if dbconn.is_connected():
            print('Connected to MySQL database')
            return dbconn
    

def handle_response(response,url,dbconn):
    # TODO implement your logics here !!!
    print("handle")
    query="select response, create_time from api_snapshot where url='"+url+"' and version=0 order by create_time desc"
    cursor = dbconn.cursor(buffered=True)
    cursor.execute(query,multi=true)
    result = cursor.fetchone()
    if result is not None:
        #print('%s' %response,create_date )# %(response,create_time))
        print("old value"+result[0][:20])
        print(response[:20])
        if result[0] != response:
                    write_db(url,response,datetime.datetime.now(),0,dbconn)
                    alarm(response, result)


        #get_info_db(query,url,dbconn,0,datetime.datetime.now())
        
    else:
        print("first write"+response[:20])
        write_db(url,response,datetime.datetime.now(),0,dbconn)

def get_info_db(sql,addr,dbconn,version=0,date='1990-01-01'):
    # version=0 means latest
    
    if date>'1990-01-01':
        sql=sql+"select balance, create_time from balance_history where address='"+add+"'"
        sql=sql+" and date>"
    sql=sql+" order by CreateTime desc"
    try:
        dbconn = mysql.connector.connect(host='localhost',database='python_mysql',user='root',password='secret')
        if conn.is_connected():
            print('Connected to MySQL database')
            cursor = dbconn.cursor(buffered=True)
            cursor.execute(sql,multi=true)
            results = cursor.fetchall()
            for row in results:
                print (row[0])
            if count(queryresult)>=version:

                    queryresult[version]
    except Exception as err:
        print ("exception2"+err)


    pass
    return balance
def alarm(msg,msg2):
    print("alarm")
    pass

def write_db(url,response,dt,version,conn):
    query0 = "UPDATE api_snapshot set version=NULL where url=%s"
    args0 =(url,)
    query = "INSERT INTO api_snapshot (url,response,create_time,version) " \
            "VALUES(%s,%s,%s,%s)"
    args = (url,response,dt,version)

    try:
        
 
        print (query0+str(url))
        cursor = conn.cursor(buffered=True) #bug as init_URL didn't require buffered, also delte binance Ticker then can insert
        cursor.execute(query0, args0)
 
        
        print("overwrite verion")
        cursor.execute(query, args,multi=true)
        conn.commit()
        print("writedb")
 
        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')
 
        conn.commit()
    except Error as error:
        print("write Db err:"+str(error))
# Retrieve a single page and report the URL and contents
def load_url(session, url,dbconn):
    print("now"+url)
    raw_response = session.get(url) #init_requests()#
    print (url+"http code %d" %(raw_response.status_code))#"parsedJson:"+json)
    json=json_parse.parsejson(raw_response.content.decode("utf-8"),url) #decode from binary b'string'
    if raw_response.status_code == 200:
        # You can refactor this part and
        # make it run in another thread
        # devoted to handling local IO tasks,
        # to reduce the burden of Net IO worker threads
        return handle_response(json,url,dbconn)
def ThreadPoolExecutor():
    return concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)

# Generate a session object
def Session():
    session = requests.Session()
    session.headers.update(HEADERS)
    return session


config = configparser.ConfigParser()
config.read('dbconfig.ini')
dbconn=db_connect(config)
#load_url(Session(),'https://www.binance.com/api/v1//exchangeInfo',dbconn)

#load_url(Session(),'https://www.binance.com/api/v1/ticker/allBookTickers',dbconn)
#load_url(Session(),'https://api.kucoin.com/v1/market/open/symbols',dbconn)
URLS=[["https://api.kucoin.com/v1/market/open/symbols"],["http://api.huobi.pro/v1/common/currencys"],["https://api.coinex.com/v1/market/list"],["https://data.gate.io/api2/1/pairs"],["https://api.bithumb.com/public/ticker/All"],["https://www.binance.com/api/v1/ticker/allBookTickers"],["https://www.binance.com/api/v1//exchangeInfo"]]

# We can use a with statement to ensure threads are cleaned up promptly
with ThreadPoolExecutor() as executor, Session() as session:
    if not URLS:
        raise RuntimeError('Please fill in the array `URLS` to start probing!')

    tasks = queue.Queue()

    for urlArray in URLS:
        url=urlArray[0]
        #print(url)
        tasks.put_nowait(url)

    def wind_up(url):
        #print('wind_up(url={})'.format(url))
        tasks.put(url)

    i=0
    while True:
        url = tasks.get()

        # Work
        executor.submit(load_url, session, url,dbconn)
        i=i+1
        print(i)

        threading.Timer(interval=INTERVAL, function=wind_up, args=(url,)).start()
