from pymongo import MongoClient
from bson import json_util
import datetime
import json
import pandas
import re

def get_tweets(date_start, date_end, region, news):
    if region == '1':
        tweet = sgtweet
        reply = sgreply

    if date_start != None:
        date_start = datetime.datetime.strptime(date_start, '%Y-%m-%d')
    else:
        date_start = datetime.datetime.strptime('1990-01-01', '%Y-%m-%d')

    if date_end != None:
        datetime.datetime.strptime(date_end,'%Y-%m-%d')
    else:
        date_end = datetime.datetime.today().strftime('%Y-%m-%d')

    result = tweet.find({
        'date': {'$gte':date_start, '$lte':datetime.datetime.strptime(date_end,'%Y-%m-%d')},
        'News': {'$eq': news}
    }, {'_id':0})

    listtweet = list(result)

    return listtweet

def get_reply(convoid, region):
    if region == '1':
        reply = sgreply
    
    result = reply.find({
        'conversationId' : convoid
    })

    listreply = list(result)
    return listreply

def get_userid(region):
    if region == '1':
        tweet = sgtweet
    
    result = tweet.find({},{
        '_id':0,
        'user':1
    })

    return list(result)

def get_usertweets(userid, region):
    if region == '1':
        tweet = sgtweet
    
    result = tweet.find({'user.id':userid})
    return list(result)

client = MongoClient('localhost', 27017)

db = client.Twitter

sgtweet = db['sg']
sgreply = db['sgreply']

cmd = input('Enter 1 for tweets, 2 for replies, 3 for userid, 4 for user tweets: ')

while not cmd.isdigit() or (int(cmd) < 0 or int(cmd) > 4) :
    cmd = input('Please enter a number. Enter 1 for tweets, 2 for replies, 3 for userid, 4 for user tweets: ')

if int(cmd) == 1:
    datereg = '^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$'
    # input time range that tweets are from, in yyyy-mm-dd format
    date_start = input('Start of date range in yyyy-mm-dd format: ') #inclusive

    while not date_start or not re.match(datereg,date_start):
        date_start = input('Please input start of date range in yyyy-mm-dd format: ') 
    if date_start == '':
        date_start = None
    
    date_end = input('End of date range in yyyy-mm-dd format: ') #not inclusive
    while not date_end or not re.match(datereg, date_end):
        date_end = input('Please input end of date range in yyyy-mm-dd format: ') 
    if date_end == '':
        date_end = None

    region = input('Enter region, 1 for Singapore: ')
     
    while not region.isdigit() or (int(region) < 0 or int(region) > 1) :
        region = input('Please enter a number. Enter 1 for Singapore: ')
    
    news = input('Enter 1 for news, 0 for non-news')
    while not news.isdigit() or (int(news) < 0 or int(news) > 1):
        news = input('Enter 1 for news, 0 for non-news')
    
    tweets = get_tweets(date_start, date_end, region, news)
    
if int(cmd) == 2:
    convoid = input('Enter the conversationId: ')
    region = input('Enter region, 1 for Singapore: ')
     
    while not region.isdigit() or (int(region) < 0 or int(region) > 1) :
        region = input('Please enter a number. Enter 1 for Singapore: ')
    
    tweets = get_reply(convoid, region)

if int(cmd) == 3:
    tweets = get_userid('1')

if int(cmd) == 4:
    userid = input('Enter the userid: ')
    region = input('Enter region, 1 for Singapore: ')

    while not region.isdigit() or (int(region) < 0 or int(region) > 1) :
        region = input('Please enter a number. Enter 1 for Singapore: ')
    
    tweets = get_usertweets(userid, region)
     

#Sample of function calls used in report

#tweets = get_tweets('2022-01-12', '2022-04-10', '1', True)

#tweets = get_reply(1538521795627692032, '1')

#tweets = get_userid('1')

#tweets = get_usertweets(74932298, '1')

num = len(tweets)

tweets = json_util.dumps(tweets, indent=4)

tweets = json.loads(tweets)

with open('myfile.json', 'w', encoding='utf-8') as file:
    json.dump(tweets, file, ensure_ascii=False, indent=4)

print(f'{num} results written to myfile')