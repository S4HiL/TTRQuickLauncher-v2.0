#!/usr/bin/python
import getpass, urllib, sys, os, json, time, platform

class TTRQuickLauncher:
	'''
	This script logs you in into TTR instantly and skips the update process. 
	(Since it isn't documented on it's API documents)
	
	This isn't meant to replace TTR's original launcher.
	
	Visit here for more infomation on it's login API: https://github.com/ToontownRewritten/api-doc/blob/master/login.md
	'''

	login_url = 'https://www.toontownrewritten.com/api/login?format=json'

	def __init__(self):
		login = urllib.urlencode({'username': 'PUT USERNAME INSIDE QUOTES', 'password': 'PUT PASSWORD INSIDE QUOTES'})
		self.postRequest(login)

	def postRequest(self, request):
		post = urllib.urlopen(self.login_url, request)
		resp = json.loads(post.read())

		success = resp.get('success', 'false')
		
		if success == 'true':
			os.environ['TTR_PLAYCOOKIE'] = resp.get('cookie', 'CookieNotFound')
			os.environ['TTR_GAMESERVER'] = resp.get('gameserver', 'ServerNotFound')
			system = platform.system()
			if system == 'Windows':
				os.system('TTREngine.exe')
			elif system == 'Linux':
				os.system('./TTREngine')
			else:
				print 'Platform %s isn\' supported yet.' %system

		elif success == 'delayed':
			eta = resp.get('eta', '5')
			position = resp.get('position', '0')
			token = resp.get('queueToken', None)

			if token == None:
				print "No queue token was given. This is not supposed to be possible!"
			else:
				print "You are on %s place in the line. ETA: %s\n" % (position, eta)
				time.sleep(1)
				queueRequest = urllib.urlencode({'queueToken': token})
				self.postRequest(queueRequest)

		elif success == 'partial':
			banner = resp.get('banner', 'Please enter an authenticator token')
			authToken = resp.get('responseToken', None)

			if authToken == None:
				print "A auth token for response couldn't be found."
			else:
				appToken = raw_input(banner + '\n')

				authRequest = urllib.urlencode({'appToken': appToken, 'authToken': authToken})
				self.postRequest(authRequest)

		elif success == 'false':
			banner = resp.get('banner', "Login have failed, but the reason why was not given. Try again later.")
			print banner


TTRQuickLauncher = TTRQuickLauncher()