import pandas as pd
import snscrape.modules.twitter as sntwitter
import itertools
import folium
import os
import concurrent.futures
import shutil
import threading
from tabulate import tabulate
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

def extractData(data):
    index = data[0]
    row = data[1]
    filename = '{}.json'.format(index)
    file = drive.CreateFile({'title': filename})
    bound = []
    bound.append(row['Latitude'])
    bound.append(row['Longtitude'])
    folium.Circle(location=bound, radius=row['Radius']*1000).add_to(mapObj)

    testlib = itertools.islice(sntwitter.TwitterSearchScraper(
        ' geocode:"{}" lang:en min_retweets:5 min_faves:5'.format(row['locs'])).get_items(), 10)
    df_test = []
    for i in testlib:
        df_test.append([i.date.ctime(), i.user.username,
                       i.content, i.retweetCount, i.likeCount, i.lang])
    df_test = pd.DataFrame(
        df_test, columns=['DateTime', 'User', 'Text', 'Retweets', 'Likes', 'Language'])
    df_test.to_json('tweets/{}'.format(filename), orient='records',
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
data = pd.read_excel(r'C:\Users\seang\OneDrive\Desktop\Intern\twitter\location.xlsx')
location = pd.DataFrame(data)
location["locs"] = location['Latitude'].map(str) + ', ' + location['Longtitude'].map(str) + ', ' + location['Radius'].map(str) + 'km'
location.set_index('Location',inplace=True)

mapObj = folium.Map(location=location.loc['Singapore','Latitude':'Longtitude'])

if not os.path.exists('tweets/'):
    os.mkdir('tweets/')

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    executor.map(extractData, location.iterrows())
    print('Uploading tweets...')
    executor.shutdown(wait=True)

print('All tweets uploaded')

#for index,row in location.iterrows():
#    filename = '{}.json'.format(index)
#    file = drive.CreateFile({'title':filename})
#    bound = []
#    bound.append(row['Latitude'])
#    bound.append(row['Longtitude'])
#    folium.Circle(location=bound, radius=row['Radius']*1000).add_to(mapObj)
#
#    testlib = itertools.islice(sntwitter.TwitterSearchScraper(' geocode:"{}" lang:en min_retweets:5 min_faves:5'.format(row['locs'])).get_items(),10)
#    df_test = []
#    for i in testlib:
#        df_test.append([i.date.ctime() ,i.user.username, i.content, i.retweetCount, i.likeCount, i.lang])
#    df_test = pd.DataFrame(df_test, columns=['DateTime','User','Text','Retweets','Likes','Language'])
#    df_test.to_json('tweets/{}'.format(filename), orient = 'records', force_ascii=False, lines=True, indent=4)
#
#    file.SetContentFile('tweets/{}'.format(filename))
#    file.Upload()

mapObj.save('output.html')
file = drive.CreateFile({'title': 'map.html'})
file.SetContentFile('output.html')
file.Upload()

#os.remove('output.html')
#shutil.rmtree('twitter\tweets', onerror=handler)
