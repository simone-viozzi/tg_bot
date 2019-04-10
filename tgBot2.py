  
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple Bot to reply to Telegram messages.
This is built on the API wrapper, see echobot2.py to see the same example built
on the telegram.ext bot framework.
This program is dedicated to the public domain under the CC0 license.
"""
import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
import threading
import saver
import os


class tg_bot:
	update_id = None
	users_obj = []
	s = None
	usr_problems = {}
	
	def __init__(self):
		with open('token', 'r') as file:
			TOKEN = file.read().replace('\n', '')
		
		self.bot = telegram.Bot(TOKEN)

		try:
			self.update_id = self.bot.get_updates()[0].update_id
		except IndexError:
			self.update_id = None

		t = threading.Thread(target=self.get_users, args=(self.bot,))
		t.start()
		
		dir_path = os.path.dirname(os.path.realpath(__file__))

		self.s = saver.saver(dir_path + "/tgUsers")

		[i, tgUsers] = self.s.load()
		if (i == -1):
			print("no users saved")
		else:
			self.users_obj = tgUsers
			for u in self.users_obj:
				self.usr_problems[str(u.id)] = 0
			
	def printCurrentUsers(self):
		print("current users: \n{\n\t" + '\n\t'.join(map(str, self.users_obj)) + "\n}")

	def get_users(self, bot):
		"""thread worker function"""
		print('Worker')
		while(1):
			try:
				for u in bot.get_updates(offset=self.update_id, timeout=10):
					ids = []
					for usr in self.users_obj:
						ids.append(usr.id)
					if u.effective_user.id not in ids:
						self.users_obj.append(u.effective_user)
						u.effective_user.send_message("benvenuto")
						self.update_id = u.update_id + 1
						print("new user")
						self.usr_problems[str(u.effective_user.id)] = 0
						self.s.save(self.users_obj)
						self.printCurrentUsers()
			except Exception as e: 
				print(e)
				sleep(1)
	

	def echo(self, msg):
		"""Echo the message the user sent."""
		# Request updates after the last update_id
		for u in self.users_obj:
			flag = True
			while (flag):
				try:
					u.send_message(msg)
					print("msg for " + str(u) + " sent")
					flag = False
				except Unauthorized:
					flag = False
					self.usr_problems[str(u.id)] += 1
					try:
						print("problem by user: " + u.username)
					except:
						print("problem by user: " + str(u))
					if (self.usr_problems[str(u.id)] > 3):
						self.users_obj.remove(u)
						self.s.save(self.users_obj)
				except:
					print("connection to the user " + str(u))
					print("retrying...")
					flag = True
		
				
				



