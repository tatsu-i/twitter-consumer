from datetime import datetime, timedelta
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from bs4 import BeautifulSoup
import schedule
import requests
import tweepy
import time
import os

consumer_key = os.environ.get("TWITTER_API_KEY", "")
consumer_secret = os.environ.get("TWITTER_API_SECRET_KEY", "")
oauth_token = os.environ.get("TWITTER_ACCESS_TOKEN", "")
oauth_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET", "")
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(oauth_token, oauth_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

client = Elasticsearch(host="elasticsearch", port=9200)


def get_title(url):
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    headers = {"User-Agent": user_agent}
    resp = requests.get(url, headers=headers)
    resp.encoding = resp.apparent_encoding
    text = resp.text
    soup = BeautifulSoup(text, "html.parser")
    title = soup.find("title").text
    return title


def tweet_aggs():
    s = Search(using=client, index="twitter*").query(
        "range", **{"@timestamp": {"gte": datetime.now() - timedelta(hours=3), "lte": datetime.now()}}
    )
    s.aggs.bucket("urls", "terms", field="urls.keyword", size=1000)

    response = s.execute()

    for urls in response.aggregations.urls.buckets:
        try:
            if urls.doc_count > 5:
                url = urls.key
                status = get_title(url)
                print(url, status)
                if len(status) > 5:
                    status = f"{status}\n{url}"
                    api.update_status(status)
                    break
        except Exception as e:
            print(e)


tweet_aggs()
schedule.every(3).hours.do(tweet_aggs)

while True:
    schedule.run_pending()
    time.sleep(1)
