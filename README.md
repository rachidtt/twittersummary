# Rest API of Twitter video summarizer



## How to use the api:

When the flask webserver is running, go to on your web browser, go to http://3.21.128.209:5000/twittervideo?handle=USERHANDLE where USERHANDLE is the twitter handle of the user you want, for example: http://3.21.128.209:5000/twittervideo?handle=elonmusk 

An error will inform you if the user does not exist, if the user exists, you will start downloading a zip file of all the days the user tweeted for his last 100 tweets. Each video contains pictures of all tweets that day



## Set up:

The process is similar to the twitter video summarizer, (https://github.com/BUEC500C1/video-rachidtt), but I have added cleanup that deletes pictures and videos after it uses them. 

The server runs Flask on an AWS EC2 micro-instance that uses Ubuntu.

git clone https://github.com/BUEC500C1/twitter-summarizer-rest-service-rachidtt.git  
sudo apt install python3-pip  
pip3 install -r requirements.txt  
python3 api.py  
add keys  
mkdir tweetimages  
install ffmpeg  
python3 api.py  

