import urllib.request as req
import time
def url_reader(url = "http://stackoverflow.com"):

	try
		f = req.urlopen(url)
		print (f.read())

	except Exception as err
		print (err)

def save_state():
	pass
	return []

def looper (sleepLength=720,urlList):
	for url in urlList: #initial save
		Latest_saved.append(save_state(url_reader(url))) # return a list
	while TRUE:
		pool = ThreadPool(4) 

		# open the urls in their own threads ??HOW to process queue larger then thread number? https://stackoverflow.com/questions/20533126/python-multithreading-without-a-queue-working-with-large-data-sets
		results = pool.map(urllib2.urlopen, urls)
		time.sleep(sleepLength)  # how to parallel this? if we have 100 urls, then takes 100*20 min to loop?
		detector(urlList) #? use last saved status returned to compare?

def detector (urlList):
	
	


	for url in urlList:
			contentFirst=url_reader(url)
			
			contentNext=url_reader(url)

			if contentFirst!=contentNext:
				save_state(contentFirst)
				save_state(contentNext)
