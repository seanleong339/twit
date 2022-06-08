## Scrape twitter news

Code to scrape news tweets in a radius from a specific coordinate. Also generates a Folium HTML map with bounding of the approximate location where tweets are from.

Implemented using snsscrape on Python 3.8 and above. (https://github.com/JustAnotherArchivist/snscrape)

To add or remove locations to scrape, open the `location.xlsx` file and add the location name, coordinates and radius in km.
To modify the filters used when scraping e.g scraping all tweets instead of just news, modify string in the second line below, found in the function `extractData`

```
testlib = itertools.islice(sntwitter.TwitterSearchScraper(
        'geocode:"{}" lang:en min_retweets:5 min_faves:5 filter:news'
        .format(row['locs']))
        .get_items(), 
        100)
```

For filters available to be used, refer to https://github.com/igorbrigadir/twitter-advanced-search
