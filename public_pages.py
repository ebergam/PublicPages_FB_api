import requests, json, datetime, time
import unicodecsv as csv

# Definitions
app_token = '<INSERT>'
app_secret = '<INSERT>'
since_date = "2013-04-01" # YYYY-MM-DD
until_date = "2019-05-17" # YYYY-MM-DD
pagelist = ['repubblica', 'ilGiornale']

# Functions
def call_api(url):
	# Try until success or rate limiting
	success = False
	while success is False:
		try:
			r = requests.get(url)
			print('API call... '+str(r.status_code))
			if r.status_code == 200:
				#print(r.headers)
				success = True
			elif r.status_code == 403:
				print("Rate limiting reached, sleep and retry every minute... ")
				print(r.headers)
				time.sleep(60)
			elif r.status_code != 200:
				print(r.headers)
				time.sleep(60)
		except Exception as e:
			print(e)
			time.sleep(5)
			print("Error for URL {}: {}".format(url, datetime.datetime.now()))
			print("Retrying.")
	return r


def parse_response(text_response, wr):
	json_object = json.loads(text_response)

	if 'paging' in json_object:
		pass#print('parsing...')
	else: 
		print(json_object)

	def extract_attribute(attr, obj):
		if attr in obj:
			return obj[attr]
		else:
			return 'NA'
	
	### Check for next page
	if 'paging'in json_object:
		if 'cursors' in json_object['paging']:
			after = extract_attribute('after', json_object['paging']['cursors'])
		else:
			after = ''
	else:
		after = ''

	### Check and restructure data
	posts_num = len(json_object['data'])
	#print('writing ' + str(len(json_object['data'])) + ' posts...')

	for post in json_object['data']:
		#print(post.keys())
		## define nested structures
		if 'attachments' in post:
			attachments = post['attachments']['data'][0]
		else:
			#with open('err.json', 'w') as outfile: #check errors?
			#	json.dump(json_object, outfile)
			attachments = ''

		## extract
		title = extract_attribute('title', attachments)
		description = extract_attribute('description', attachments)
		message = extract_attribute('message', post)
		status_type = extract_attribute('status_type', post)

		url = extract_attribute('unshimmed_url', attachments)
		date = extract_attribute('created_time', post)
		post_id = extract_attribute('id', post)

		## numeric nested attributes
		if 'shares' in post:
			shares = extract_attribute('count', post['shares'])
		else:
			shares = 'NA'

		if 'comments' in post:
			comments = extract_attribute('total_count', post['comments']['summary'])
		else:
			comments = 'NA'

		if 'likes' in post:
			likes = extract_attribute('total_count', post['likes']['summary'])
		else:
			likes = 'NA'
		
		if 'Love' in post:
			love = extract_attribute('total_count', post['Love']['summary'])
		else:
			love = 'NA'

		if 'Wow' in post:
			wow = extract_attribute('total_count', post['Wow']['summary'])
		else:
			wow = 'NA'
		
		if 'Haha' in post:
			haha = extract_attribute('total_count', post['Haha']['summary'])
		else:
			haha = 'NA'

		if 'Sad' in post:
			sad = extract_attribute('total_count', post['Sad']['summary'])
		else:
			sad = 'NA'

		if 'Angry' in post:
			angry = extract_attribute('total_count', post['Angry']['summary'])
		else:
			angry = 'NA'
 		
		wr.writerow({
			"title": title,
			"description": description,
			"message": message,
			"status_type": status_type,
			"url": url,
			"date": date,
			"post_id": post_id,
			"comments": comments,
			"shares": shares,
			"likes": likes,
			"love": love,
			"wow": wow,
			"haha": haha,
			"sad": sad,
			"angry": angry,
			})
			
	return posts_num, after

def page_handler(page_id, access_token, since_date, until_date):
	# CSV handling
	outfile = page_id+"_fb_statuses.csv"

	with open(outfile, 'wb') as outcsv:
		wr = csv.DictWriter(outcsv, fieldnames=['title', 'description', 'message', 'status_type', 'url', 'date', 'post_id', 'comments', 'shares', 'likes', 'love', 'wow', 'haha', 'sad', 'angry'])
		wr.writeheader()
		print('Querying '+page_id+' ...')
		## Compose URL
		url0 = "https://graph.facebook.com/v3.3/{0}/feed?&fields=attachments%7Bdescription%2Ctitle%2Cunshimmed_url%7D%2Cmessage%2Cstatus_type%2Cid%2Ccreated_time%2Cshares%2Clikes.summary(true)%2Ccomments.limit(0).summary(true)%2Creactions.type(LOVE).limit(0).summary(total_count).as(Love)%2Creactions.type(WOW).limit(0).summary(total_count).as(Wow)%2Creactions.type(HAHA).limit(0).summary(total_count).as(Haha)%2Creactions.type(SAD).limit(0).summary(1).as(Sad)%2Creactions.type(ANGRY).limit(0).summary(1).as(Angry)&limit=100&access_token=".format(page_id)
		url0 = url0 + "&access_token=" + access_token
		url0 = url0 + "&since=" + since_date
		url0 = url0 + "&until=" + until_date
		url_base = url0 + "&after="

		## Make request
		r = call_api(url_base)
		counter, after = parse_response(r.text, wr)
		
		# loop to next page and repeat
		while after != '':
			r = call_api(url_base+after)
			posts_num, after = parse_response(r.text, wr)
			counter = counter + posts_num
			print('Got '+str(counter)+' posts from '+page_id+' ...')
			time.sleep(7)

		print('Finished querying '+page_id)
		print(datetime.datetime.now())

# Main
if __name__ == "__main__":
	access_token = app_token+"|"+app_secret
	for page_id in pagelist: 
		page_handler(page_id, access_token, since_date, until_date)
