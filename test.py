import pandas as pd
import snscrape.modules.twitter as sntwitter
import itertools
import copy
import json
import time
from pymongo import MongoClient
from tabulate import tabulate

location = '1.317351,103.8194992,15km'

client = MongoClient('localhost', 27017)

db = client.Twitter

sgtweet = db['sg']
sgreply = db['sgreply']

tweets = []
replies = []

startdate=''
enddate = ''

tic = time.perf_counter()

for i, tweet in enumerate(sntwitter.TwitterSearchScraper('geocode:"{}" lang:en filter:news  until:2022-06-22'.format(location)).get_items()):
	if i > 1000:
		break
	tweets.append(tweet)
	replies = replies + list(itertools.islice(sntwitter.TwitterTweetScraper(tweet.id, mode = sntwitter.TwitterTweetScraperMode.RECURSE).get_items(),100))

print(f'Got {len(tweets)} tweets, {len(replies)} replies')

df = pd.DataFrame(tweets)
print(f'{df.shape[0]} tweets found')
df['News'] = True

#tweetdict = df.to_dict('records')

#sgtweet.insert_many(tweetdict, ordered=False)

if len(replies) > 0:
	repliesdf = pd.DataFrame(replies)
	repliesdf = repliesdf[repliesdf.lang == 'en']
	repliesdf.to_json('replies.json', orient='records', date_format='iso',
			    force_ascii=False)

	#sgreply.insert_many(repliesdf.to_dict('records'), ordered=False)

df.to_json('test.json', orient='records', date_format='iso',
		    force_ascii=False)


toc = time.perf_counter()
print(f"Downloaded {df.shape[0]} tweets in {toc - tic:0.4f} seconds")
