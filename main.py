import sys
import pickle
import urllib.request
import urllib
from bs4 import BeautifulSoup
import time
import random
import tgBot2
import os 
import saver

b = tgBot2.tg_bot()
while(1):
	try:
		request = urllib.request.Request('http://www.tlc.dii.univpm.it/blog/teaching/corsi-di-preparazione-per-la-certificazione-hcna')

		#request = urllib.request.Request('https://stackoverflow.com/')

		response = urllib.request.urlopen(request) # Make the request
		# Grab everything before the dynabic double-click link
		htmlString = response.read().decode('utf-8')

		soup = BeautifulSoup(htmlString, features='lxml')
		l = soup.find('body').find_all('div')
		htmlString = '\n'.join([str(ele) for ele in l])
		
		
		dir_path = os.path.dirname(os.path.realpath(__file__))

		s = saver.saver(dir_path + "/htmlString")

		[i, htmlString_old] = s.load()
		if (i == -1):
			s.save(htmlString)
			print("first run")
			b.echo("first run")
		else:
			if (htmlString_old == htmlString):
				print("site doesn't changed")
				b.echo("site doesn't changed")
			else:
				s.save(htmlString)
				for i in range(50):
					print("site changed!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
					b.echo("site changed!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
					time.sleep(5)
		rdn = random.randint(60,300)
		print("going to sleep for " + str(round(rdn/60, 2)) + " minutes")
		b.echo("going to sleep for " + str(round(rdn/60, 2)) + " minutes")
		b.printCurrentUsers()
		time.sleep(rdn)
	except urllib.request.URLError:
		print("connection error!!!")		
		time.sleep(1)


