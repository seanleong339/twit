import pandas as pd
import snscrape.modules.twitter as sntwitter
import itertools
import copy
import json
from pymongo import MongoClient
from tabulate import tabulate

location = '1.317351,103.8194992,15km'

client = MongoClient('localhost', 27017)

db = client.Twitter

sgtweet = db['sg']
sgreply = db['sgreply']

testlib = sntwitter.TwitterSearchScraper(
	'geocode:"{}" lang:en min_retweets:5 min_faves:5 '
	.format(location))

tweets = []
replies = []

for i, tweet in enumerate(sntwitter.TwitterSearchScraper('geocode:"{}" lang:en filter:news  since:2022-03-20 until:2022-03-21'.format(location)).get_items()):
	if i > 4:
		break
	tweets.append(tweet)
	replies = replies + list(itertools.islice(sntwitter.TwitterTweetScraper(tweet.id, mode = sntwitter.TwitterTweetScraperMode.RECURSE).get_items(),100))

df = pd.DataFrame(tweets)
df['News'] = True

	


#users = copy.deepcopy(list)
#
#df_test = pd.DataFrame(testlib)
#
#users = df_test.copy()
#users = df_test.loc[:,'user'].tolist()
#names = [row['username'] for row in users]
#print(names)

testlib = sntwitter.TwitterTweetScraper(
		1538503214710296577, 
		mode = sntwitter.TwitterTweetScraperMode.RECURSE).get_items()

df_test = pd.DataFrame(testlib)

df_test.to_json('replies.json', orient='records', date_format='iso',
		    force_ascii=False, lines=True, indent=4)

#ids = df_test.loc[:,'id']
#
#df_test['Replies'] = df_test.apply(
#        lambda row : list(itertools.islice(sntwitter.TwitterTweetScraper(
#                row.id, mode = sntwitter.TwitterTweetScraperMode.RECURSE)
#                .get_items(),
#                100))[1:],
#        #lambda row: row.id,
#        axis=1
#)
#

tweetdict = df.to_dict('records')

for i in tweetdict:
	try:
		sgtweet.insert_one(i)
	except Exception as e:
		print(e)

if len(replies) > 0:
	repliesdf = pd.DataFrame(replies)
	repliesdf = repliesdf[repliesdf.lang == 'en']
	repliesdf.to_json(orient='records', date_format='iso',
			    force_ascii=False, lines=True, indent=4)

	sgreply.insert_many(repliesdf.to_dict('records'))

df.to_json('test.json', orient='records', date_format='iso',
		    force_ascii=False, lines=True, indent=4)
