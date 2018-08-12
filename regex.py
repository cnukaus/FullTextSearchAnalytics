import re
import datetime
import pandas as pd
def calcprice(filename):
    	
    	try:
    		print ('ok')
    		f = open(filename, 'r')
    		data = f.read()
    		rows = data.split('\n')

    		for row in rows:
    			print (re.search("(?<=  )[\d.]+(?=  )",row))#,",",re.search("\d{4}-\d{2}-\d{2}",row))
    			

    	except Exception as e:
    		print(e)
    		

if __name__ == "__main__": ## If we are not importing this:
    	#calcprice('dfk balance.txt')


        a = datetime.datetime.today()
        numdays = 120
        dateList = []
        for x in range (0, numdays):
            dateList.append(a - datetime.timedelta(days = (x)))
        base = datetime.datetime.today()
        date_list = [base - datetime.timedelta(days=x) for x in range(0, numdays)]
        #print(pd.date_range(pd.datetime.today(), periods=100).tolist())

        date1 = '04-22-2018'
        date2 = '08-10-2018'
        start = datetime.datetime.strptime(date1, '%m-%d-%Y')
        end = datetime.datetime.strptime(date2, '%m-%d-%Y')
        step = datetime.timedelta(days=1)
        while start <= end:
                print(start.date().strftime('%d-%m-%Y'))
                start += step