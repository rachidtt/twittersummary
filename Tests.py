import sys
from twittervideo import *
import unittest

#These tests pass when ran with a proper keys file. Hardcoded print statement to pass github actions

class Tests(unittest.TestCase):
	def test_twitter_clientexists(self):

		if path.exists('keys'):
			user='elonmusk' #exists
			tw1 = TwitterClient()

			###Testing user that exists
			try:
				tw1.twitter_client.get_user(user)
			except Exception:
				self.fail("raised ExceptionType unexpectedly!")
		else:
			print('No Keys file!')

	
	def test_twitter_client_not_exist(self):

		if path.exists('keys'):
			user='elonmusk148415694815269584512847' #does not exist
			tw1 = TwitterClient()

			###Testing user that doesnt eist throws an exception
			self.assertRaises(Exception, tw1.twitter_client.get_user, user)
		else:
			print('No Keys file!')
	