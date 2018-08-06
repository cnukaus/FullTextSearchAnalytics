import re
def calcprice(filename):
	
	try:
		print ('ok')
		f = open(filename, 'r')
		data = f.read()
		rows = data.split('\n')

		for row in rows:
			print (re.search("(?: 1+)\d*\.?\d*",row))
			

	except Exception as e:
		print(e)
		

if __name__ == "__main__": ## If we are not importing this:
	calcprice('dfk balance.txt')