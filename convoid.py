from pymongo import MongoClient
import snscrape.modules.twitter as sntwitter
from bson import json_util
import itertools
import datetime
import json
import time
import numpy as np
import pandas as pd
import re

#client = MongoClient('localhost', 27017)
#
#db = client.Twitter
#
#sgtweet = db['sg']
#sgreply = db['sgreply']
#
#convoid = list(sgtweet.distinct('conversationId'))
#
#splits = np.array_split(convoid, 92)
#print(len(splits[0]))

start = 2 

convoids = []

for i in range(8):
    curr = start + i
    f = open(f'tweet_ids/{str(curr)}.json')
    convoids = convoids + json.load(f)

end = curr
print(len(convoids))
print(start)
print(end)
    

replies = []

tic = time.perf_counter()
for id in convoids:
    replies = replies + list(itertools.islice(sntwitter.TwitterTweetScraper(id, mode = sntwitter.TwitterTweetScraperMode.RECURSE).get_items(),100))

toc = time.perf_counter()
print(f"Downloaded {len(replies)} tweets in {toc - tic:0.4f} seconds")

df = pd.DataFrame(replies)
df.to_json(f'{start}_{end}_reply.json', orient='records', date_format='iso', force_ascii=False)

#for index, id in enumerate(splits):
#    data = json_util.dumps(id, indent = 4)
#
#    data = json.loads(data)
#
#    with open(f'tweet_ids/{index}.json', 'w', encoding='utf-8') as file:
#        json.dump(data, file, ensure_ascii=False, indent=4)