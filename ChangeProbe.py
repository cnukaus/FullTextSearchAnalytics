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

def looper (sleepLength=720,urlList):
	time.sleep(sleepLength)  # how to parallel this? if we have 100 urls, then takes 100*20 min to loop?
	detector(urlList) #? use last saved status returned to compare?

def detector (urlList):
	
	for url in urlList: #initial save
		save_state(url_reader(url))


	while TRUE:
		for url in urlList:
			contentFirst=url_reader(url)
			
			contentNext=url_reader(url)

			if contentFirst!=contentNext:
				save_state(contentFirst)
				save_state(contentNext)
