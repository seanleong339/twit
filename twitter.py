import pandas as pd
import snscrape.modules.twitter as sntwitter
import itertools
import folium
import os
import time
import re
import concurrent.futures
import shutil
from tabulate import tabulate
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

def extractNewsData(data):
    index = data[0]
    row = data[1]
    filename = '{}.json'.format(index)
    file = drive.CreateFile({'title': filename})
    bound = []
    bound.append(row['Latitude'])
    bound.append(row['Longtitude'])
    folium.Circle(
        location=bound, 
        radius=row['Radius']*1000, 
        tooltip='{}'.format(index),
        color="#3186cc",
        fill=True,
        fill_color="#3186cc"
    ).add_to(mapObj)

    testlib = itertools.islice(sntwitter.TwitterSearchScraper(
        'geocode:"{}" lang:en min_retweets:5 min_faves:5 {} {} {}'
        .format(row['locs'], news, timestart, timeend))
        .get_items(), 
        1)


    df_test = pd.DataFrame(
        testlib)


    df_test['Replies'] = df_test.apply(
        lambda row : list(itertools.islice(sntwitter.TwitterTweetScraper(
                row.id, mode = sntwitter.TwitterTweetScraperMode.RECURSE)
                .get_items(),
                100))[1:],
        axis=1)

    df_test.to_json('tweets/{}'.format(filename), orient='records', date_format='iso',
                    force_ascii=False, lines=True, indent=4)

    file.SetContentFile('tweets/{}'.format(filename))
    file.Upload()

def extractUserTweets(user):

    filename = "{}'s Tweets.json".format(user)
    file = drive.CreateFile({'title': filename})

    testlib = sntwitter.TwitterSearchScraper(
        'from:{} since:{} until:{}'
        .format(user, timestart, timeend)).get_items() 

    df_test = pd.DataFrame(
        testlib)

    df_test.to_json('tweets/{}'.format(filename), orient='records', date_format='iso',
                    force_ascii=False, lines=True, indent=4)

    file.SetContentFile('tweets/{}'.format(filename))
    file.Upload()

def replyToTweet(id):
    filename = "Reply to tweet {}.json".format(id)
    file = drive.CreateFile({'title': filename})

    testlib = sntwitter.TwitterTweetScraper(
                id, 
                mode = sntwitter.TwitterTweetScraperMode.RECURSE).get_items()

    df_test = pd.DataFrame(
        testlib)

    df_test.to_json('tweets/{}'.format(filename), orient='records', date_format='iso',
                    force_ascii=False, lines=True, indent=4)

    file.SetContentFile('tweets/{}'.format(filename))
    file.Upload()


# exception handler
def handler(func, path, exc_info):
    print("Inside handler")
    print(exc_info)

gauth = GoogleAuth()
gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()

gauth.SaveCredentialsFile("mycreds.txt")
drive = GoogleDrive(gauth)

#import location
data = pd.read_excel(r'D:\Sean\Intern\Twitter\twit\location.xlsx')
location = pd.DataFrame(data)
location["locs"] = location['Latitude'].map(str) + ', ' + location['Longtitude'].map(str) + ', ' + location['Radius'].map(str) + 'km'
location.set_index('Location',inplace=True)

if not os.path.exists('tweets/'):
    os.mkdir('tweets/')

datereg = '^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$'
# input time range that tweets are from, in yyyy-mm-dd format
timestart = input('Start of time range in yyyy-mm-dd format:') #inclusive

if not timestart or not re.match(datereg,timestart):
    timestart = ''
else:
    timestart = 'since:'+timestart
timeend = input('End of time range in yyyy-mm-dd format:') #not inclusive
if not timeend or not re.match(datereg, timeend):
    timeend = ''
else: 
    timeend = 'until:' + timeend

first = input('Search tweets enter 1, search replies enter 2: ')
while first != '1' and first != '2':
    first = input('Invalid input. Enter 1 to search tweet, enter 2 to search replies: ')

if first == '1':
    second = input('Search by location enter 1, search by user enter 2: ')
    while second != '1' and second != '2':
        second = input('Invalid input. Enter 1 to search by location, enter 2 to search by user: ')
    if second == '1':
        news = input('Search news tweet enter 1, search for all tweets enter 2: ')
        while news != '1' and news != '2':
            news = input('Invalid input. Enter 1 for news, 2 for all tweets: ')
        if news == '1':
            news = 'filter:news'
        else:
            news = ''
        tic = time.perf_counter()
        mapObj = folium.Map(location=location.loc['Singapore','Latitude':'Longtitude'])
        with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
            executor.map(extractNewsData, location.iterrows())
            print('Uploading tweets...')
            executor.shutdown(wait=True)
        mapObj.save('output.html')
        file = drive.CreateFile({'title': 'map.html'})
        file.SetContentFile('output.html')
        file.Upload()
        toc = time.perf_counter()
        print(f"Downloaded the tweets in {toc - tic:0.4f} seconds")
        print('All tweets uploaded')
    else:
        user = input('Enter username to search tweets:\n')
        tic = time.perf_counter()
        extractUserTweets(user)
        toc = time.perf_counter()
        print(f"Downloaded the tweets in {toc - tic:0.4f} seconds")
        print('All tweets uploaded')
else:
    tweetid = input('Enter id of tweet to search replies: ')
    replyToTweet(tweetid)

#os.remove('output.html')
shutil.rmtree('tweets/', onerror=handler)
