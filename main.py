try:
	import tweepy, time, random, oauth, re, requests
	from datetime import datetime
	from sys import getsizeof #for grabbing variable ram usage
except:
	sys.exit("Could not import all modules...")

data = []
media_urls = []

c_key = ""
c_secret = ""
a_key = ""
a_secret = ""

auth = tweepy.OAuthHandler(c_key,c_secret)
auth.set_access_token(a_key,a_secret)
api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

def downloadPhoto(url):
	print("Downloading " + url + "...")
	try:
		img = requests.get(url).content
		with open('tmp.jpg', 'wb') as file:
			file.write(img)
	except Exception as e:
		print("Error downloading: " + str(e))
		return False
	print("Downloaded Successfully!")
	return True

def log(message):
	print(message)
	with open('log.log', 'w+') as file:
		a = file.read()
		a += "\n"+str(datetime.now())+": "+message
		file.write(a)

def tweet(text1, text2):
	global media_urls
	try:
		#Formatting
		#there's probably a better way with beautiful soup but... yeah
		text1 = text1.replace("<br>","\n").replace("\\n","\n").replace("&gt;",">").replace("&lt;","<").replace("RT"," ")
		text2 = text2.replace("<br>","\n").replace("\\n","\n").replace("&gt;",">").replace("&lt;","<").replace("RT"," ")
		text1 = re.sub(r'^.https?:\/\/.*[\r\n]*', ' ', text1, flags=re.MULTILINE)
		text2 = re.sub(r'^.https?:\/\/.*[\r\n]*', ' ', text2, flags=re.MULTILINE)
		text1 = ' '.join(filter(lambda x:x[0]!='@', text1.split()))
		text2 = ' '.join(filter(lambda x:x[0]!='@', text2.split()))
		#Get half tweets
		texto2 = int((len(text2) / 2) * -1)
		texto1 = int(len(text1) / 2)
		#Find the mid point, then increment until it finds a space. This way whole words aren't cut into two
		try:
			while text1[texto1] != " ":
				texto1 += 1
			while text2[texto2] != " ":
				texto2 -= 1
		except:
			pass
		#TODO: fix
		#lastWord = text1.split(' ')[len(text1)-1]
		#if text2[texto2:].startswith(lastWord): #if the last word of the first tweet is the same as the first word of the second tweet, remove it.
		#	text1.replace(lastWord, "")
		finalMessage = text1[:texto1] + " " + text2[texto2:] #get the first half and second half and then mash them up
		if len(finalMessage) > 280: #if it's over the limt then start again
			tweet(random.choice(data),random.choice(data1))
		log("Tweet1: "+text1)
		log("Tweet2: "+text2)
		if random.randint(0,29) == 15: # 1 in 30 chance of updating with a photo
			if downloadPhoto(random.choice(media_urls)):
				api.update_with_media('tmp.jpg', finalMessage)
			else:
				api.update_status(finalMessage)
		else:
			api.update_status(finalMessage) #tweet!
		log("Tweeted: "+finalMessage)
	except Exception as e:
		print("Error Tweeting: " + str(e))

def update_data():
	global data
	global media_urls
	log("Updating tweet archive...")
	if random.randint(0,100) > 90:
		data = []
	for page in tweepy.Cursor(api.user_timeline,id='twitter', count=200, include_entities=True).pages(16):
		for status in page:
			if 'media' in status.entities:
				for image in status.entities['media']:
					if image['type'] == "photo":
						media_urls += [image['media_url']]
			data += [status.text]
	log("Done!")

update_data()

while True:
	#print(random.choice(data))
	if random.randint(0,250) == 172: #while the bot is running, new tweets will obviously be made. I chose a 1/250th chance, which means it should update every week or so.
		update_data()
	tweeta = random.choice(data)
	tweetb = random.choice(data)
	while tweeta == tweetb:
		tweetb = random.choice(data)
	tweet(tweeta,tweetb)
	log("Number of tweets caught: "+str(len(data)))
	log("Data size: "+str(getsizeof(data)/1024)+" kb")
	time.sleep(1800)
	log("Tweeting...")
