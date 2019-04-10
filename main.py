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


site = 'http://www.tlc.dii.univpm.it/blog/teaching/corsi-di-preparazione-per-la-certificazione-hcna'
old_time = 0
b = tgBot2.tg_bot()
cont_failed = 0
while(1):
	try:
		request = urllib.request.Request(site)

		try:
			response = urllib.request.urlopen(request) # Make the request
		except:
			print("connessione al sito fallita!!!!")
			if (cont_failed > 10):
				b.echo("connessione al sito fallita per le scorse 10 vote!!!!\n\n" + "link: " + site + "\n" 
						+"paypal link for donation http://paypal.me/simo97")
				cont_failed = 0
			else:
				cont_failed += 1
			continue

		# Grab everything before the dynabic double-click link
		htmlString = response.read().decode('utf-8')

		soup = BeautifulSoup(htmlString, features='lxml')
		l = soup.find('body').find_all("div", id="main")
		htmlString = '\n'.join([str(ele) for ele in l])
		
		dir_path = os.path.dirname(os.path.realpath(__file__))

		s = saver.saver(dir_path + "/htmlString")

		[i, htmlString_old] = s.load()
		if (i == -1):
			s.save(htmlString)
			print("first run")
			b.echo("first run")
		elif (htmlString_old == htmlString):
			rdn = random.randint(60,300)
			print("site doesn't changed")
			print("going to sleep for " + str(round(rdn/60, 2)) + " minutes")
			if (old_time > 600):
				b.echo("site doesn't changed in the last " + str(round(old_time/60, 2)) 
					+ " minutes\n\n" + "link: " + site + "\n" 
					+"paypal link for donation http://paypal.me/simo97")
				old_time = 0
			else:
				old_time = old_time + rdn
			print("old_time: " + str(old_time))
			print("link rapido: " + site)
			b.printCurrentUsers()
			time.sleep(rdn)
		elif (htmlString_old != htmlString):
			s.save(htmlString)
			for i in range(50):
				print("site changed!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
				print("link rapido: " + site)
				b.echo("site changed!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
				b.echo("link: " + site)
				time.sleep(5)
		else:
			print("something goes truly wrong")
			b.echo("something goes truly wrong")
	except (urllib.request.URLError or ConnectionResetError):
		print("connection error!!!")		
		
		time.sleep(10)


