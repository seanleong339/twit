from pymongo import MongoClient
from bson import json_util
import datetime
import json
import pandas

def get_tweets(date_start, date_end, region, news):
    if region == '1':
        tweet = sgtweet
        reply = sgreply

    result = tweet.find({
        'date': {'$gte':datetime.datetime.strptime(date_start, '%Y-%m-%d'), '$lte':datetime.datetime.strptime(date_end,'%Y-%m-%d')},
        'News': {'$eq': news}
    })

    listtweet = []

    for i in result:
        listtweet.append(i)

    return listtweet

client = MongoClient('localhost', 27017)

db = client.Twitter

sgtweet = db['sg']
sgreply = db['sgreply']

tweets = get_tweets('2022-01-12', '2022-04-10', '1', True)

tweets = json_util.dumps(tweets)

tweets = json.loads(tweets)

with open('myfile.json', 'w') as file:
    json.dump(tweets, file, ensure_ascii=False, indent=4)

