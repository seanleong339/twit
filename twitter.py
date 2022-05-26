import pandas as pd
import snscrape.modules.twitter as sntwitter
import itertools
from tabulate import tabulate

loc = '1.290270, 103.851959, 10km' #SG coordinates
testlib = itertools.islice(sntwitter.TwitterSearchScraper(' geocode:"{}" lang:en'.format(loc)).get_items(),100)
df_test = []
for i in testlib:
    df_test.append([i.date.ctime() ,i.user.username, i.content, i.retweetCount, i.likeCount, i.lang])
df_test = pd.DataFrame(df_test, columns=['DateTime','User','Text','Retweets','Likes','Language'])
df_test.to_json('temp.json', orient = 'records', force_ascii=False, lines=True, indent=4)
