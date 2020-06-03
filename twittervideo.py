from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from io import open
from collections import Counter
from videomaker import *
import configparser
import tweepy
import json
import os.path
from os import path
from zipfile import ZipFile


class JsonTweet():
	def __init__(self,tweet):
		self.user = tweet['user']['name']
		self.date = tweet['created_at']
		self.daystr = (self.date).split()[:3] #first three words for just mmddyy
		self.day = ' '.join(self.daystr) #cat the 3 string into one
		
		
		if not 'retweeted_status' in tweet:
			self.text = tweet['full_text']
			self.rt = False
			self.favct = tweet['favorite_count']
			self.rtct = tweet['retweet_count']
		else:
			self.text = tweet['retweeted_status']['full_text']
	
	def separateByDay(JsonTweet,len):
		pass





class TwitterClient():
	def __init__(self,user=None): #None goes to own timeline
		self.auth=Authenticator().authenticate()
		self.twitter_client=API(self.auth)
		self.twitter_user=user

	def get_user_timeline_tweets(self,amount):
		tweets=[]
		for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user,tweet_mode='extended').items(amount):
			tweets.append(tweet)		
				
		return tweets





class Authenticator():
	def authenticate(self):


		if path.exists('keys'):
			config = configparser.ConfigParser()
			config.read('keys')
			CONSUMER_KEY = config.get('auth', 'consumer_key').strip()
			CONSUMER_KEY_SECRET = config.get('auth', 'consumer_secret').strip()
			ACCESS_TOKEN = config.get('auth', 'access_token').strip()
			ACCESS_TOKEN_SECRET = config.get('auth', 'access_secret').strip()

		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
		auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
		return auth




def twittervideo(handle):
	user = handle

	num = 100 
	numcores=4 
	jsonwtlist = [] 
	daylist = []
	tw1 = TwitterClient()		
	exist=False
	try:
		u=tw1.twitter_client.get_user(user)
	except Exception:
		return 'user does not exist'


	twitter_client=TwitterClient(user)
	data = twitter_client.get_user_timeline_tweets(num)
	for i in range(len(data)):
		jsonwtlist.append(JsonTweet(data[i]._json))#put each into JsonTweet Object
		daylist.append(jsonwtlist[i].daystr[2])


	lastday=jsonwtlist[0].daystr[2]
	number=0
	daylist2=[]
	daylist2.append(jsonwtlist[0].day.replace(' ','_'))
	for i in range(len(jsonwtlist)): #Create a folder for each day, inside has numbered pictures of tweets that day
		if(jsonwtlist[i].daystr[2] == lastday):
			number+=1
			convertToImage(user,jsonwtlist[i].text,number,jsonwtlist[i].day)
		else:
			daylist2.append(jsonwtlist[i].day.replace(' ','_'))
			number=1
			lastday=jsonwtlist[i].daystr[2]
			convertToImage(user,jsonwtlist[i].text,number,jsonwtlist[i].day)
	jobqueue=queue.Queue()


	for i in range(len(daylist2)):#For each user_ddmmyy Folder, make a video of all the pictures in it
		imagespath=user+'_'+daylist2[i]
		jobqueue.put(imagespath)
		

	for i in range(numcores):
		WorkerThread(jobqueue,i).start()

	jobqueue.join()

	vidlist =[]
	for i in range(len(daylist2)):#For each user_ddmmyy Folder, make a video of all the pictures in it
		temp = handle+'_'+daylist2[i]+'.mp4'
		vidlist.append(temp)


	zipname='Videos/'+handle+'.zip'
	zipObj = ZipFile(zipname, 'w')
	for i in range(len(vidlist)):
		zipObj.write('Videos/'+vidlist[i])
	zipObj.close()

	for i in range(len(vidlist)):
		os.remove('Videos/'+vidlist[i])

	return zipname


if(__name__ == "__main__"):

	print('Welcome to the Twitter Daily Video Summary! \n\n\n')
	#user="elonmusk"  #Enter the @ of wanted user
	num = 100 #Number of tweets to fetch
	numcores=4 #will be the number of concurent threads we will let run
	jsonwtlist = [] #list of Jsontwt objects
	daylist = []
	tw1 = TwitterClient()		
	exist=False

	while(exist==False):
		print('Please enter the Twitter @:')
		user=input()	
		try:
			u=tw1.twitter_client.get_user(user)
			print("user "+user+" exists, continuing")
			exist=True
		except Exception:
			print('Error: User does not exist!\n')




	twitter_client=TwitterClient(user)
	data = twitter_client.get_user_timeline_tweets(num)
	for i in range(len(data)):
		jsonwtlist.append(JsonTweet(data[i]._json))#put each into JsonTweet Object
		daylist.append(jsonwtlist[i].daystr[2])


	lastday=jsonwtlist[0].daystr[2]
	number=0
	daylist2=[]
	daylist2.append(jsonwtlist[0].day.replace(' ','_'))
	for i in range(len(jsonwtlist)): #Create a folder for each day, inside has numbered pictures of tweets that day
		if(jsonwtlist[i].daystr[2] == lastday):
			number+=1
			convertToImage(user,jsonwtlist[i].text,number,jsonwtlist[i].day)
		else:
			daylist2.append(jsonwtlist[i].day.replace(' ','_'))
			number=1
			lastday=jsonwtlist[i].daystr[2]
			convertToImage(user,jsonwtlist[i].text,number,jsonwtlist[i].day)

	print('converting the videos...')


	jobqueue=queue.Queue()

	for i in range(len(daylist2)):#For each user_ddmmyy Folder, make a video of all the pictures in it
		imagespath=user+'_'+daylist2[i]
		jobqueue.put(imagespath)

	for i in range(numcores):
		WorkerThread(jobqueue,i).start() 
	
	jobqueue.join()


	#print('Done!\n')


	
	