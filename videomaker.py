import ffmpeg 
import subprocess
import os
from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap #if long tweet
import threading
import queue
from multiprocessing import Queue
from queue import Empty
import shutil #delete images folder with all its content


class WorkerThread(threading.Thread):
	def __init__(self,q,arg, *args, **kwargs):
		self.q=q
		self.arg=arg
		super().__init__(*args, **kwargs)
		#self.daemon=True

	def run(self):
		while True:
			try:
				work=self.q.get(timeout=1) #1s timeout
			except Empty:
				#pass
				return

			convertToVideo(work)
			self.q.task_done()
		print('Thread '+str(self.arg)+' is done.')

			#print('Thread '+str(self.ident)+' is done.')



def convertToImage(User,Text,number,day):
	fnt = ImageFont.truetype('Fonts/DejaVuSans.ttf', 15) #need a font that accepts high unicode values that could be in a tweet
	W,H = (740,460)
	
	pic = Image.open('twitter-logo-button.jpg','r')
	img = Image.new('RGB', (W,H), color = (0, 172, 238))
	img.paste(pic,(650,0))
	
	d = ImageDraw.Draw(img)
	w,h = d.textsize(Text, font=fnt)


	day = day.replace(' ','_') #need _ for file name
	path = 'tweetimages/'+str(User)+'_'+str(day)



	d.multiline_text((0,0), '@'+User+' tweeted on '+day+': ', fill=(255, 255, 255),align='left',spacing=15, font=fnt)

	if(len(Text) <= 90): #if it can fit in one line, else draw each line by spliting every 93 char
		d.multiline_text((((W-w)/2,(H-h)/2)), Text, fill=(255, 255, 255),align='left',spacing=15, font=fnt)
	else:
		splittext = wrap(Text,90)
		for i in range(len(splittext)):
			d.multiline_text((0,230+20*i), splittext[i], fill=(255, 255, 255),align='left',spacing=15, font=fnt)
			
	


	if(not os.path.isdir(path)): #because mdkir will fail if already exists
		try:
			os.mkdir(path)
		except OSError:
			print ("Creation of the directory %s failed" % path)
		else:
			#print ("Successfully created the directory %s " % path)
			pass

	name = path+'/'+str(number)+'.png'
	img.save(name)
	return



def convertToVideo(path):
	stream = ffmpeg.input(r'tweetimages/'+path+'/*.png', pattern_type='glob', framerate=0.33)
	#stream = ffmpeg.input(r'tweetimages/*.png', pattern_type='glob', framerate=1)
	#stream = ffmpeg.output(stream,'tweetimages/movie1.mp4')
	stream = ffmpeg.output(stream,'Videos/'+path+'.mp4',loglevel="quiet")
	stream = ffmpeg.overwrite_output(stream)
	ffmpeg.run(stream)
	shutil.rmtree('tweetimages/'+path)



if __name__ == '__main__': #just some testing
	#convertToVideo("elonmusk_Mon_Feb_17")
	#stri="Hellott, this is a very long textrykcvhk.xhfmxfhc,gjvklzmdgfxhcg,j 123456789abcdefghijklmnopq"
	#print(len(stri))
	#convertToImage("elon", "Hellott, this is a very long textrykcvhk.xhfmxfhc,gjvklzmdgfxhcg,j 123456789abcdefghijklmnopq and it is uu",'1','May_15')

	tasklist=["elonmusk_Mon_Feb_17","elonmusk_Sat_Feb_15","elonmusk_Sun_Feb_16","elonmusk_Tue_Feb_18","twitter_Fri_Feb_14","twitter_Wed_Feb_19","elonmusk_Mon_Feb_17","elonmusk_Sat_Feb_15","elonmusk_Sun_Feb_16","elonmusk_Tue_Feb_18",]

	print(len(tasklist))
	q=queue.Queue()
	for i in range(len(tasklist)):
		q.put(tasklist[i])

	for i in range(4):
		WorkerThread(q,i).start()


	#q.join()#stop until q empty