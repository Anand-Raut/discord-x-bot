import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

BEARER_TOKEN = os.getenv("BEARER_TOKEN")

async def get_tweet(previd):
    client = tweepy.Client(bearer_token=BEARER_TOKEN)

    username = os.getenv("ACCOUNT_NAME")
    user = client.get_user(username=username)
    user_id = user.data.id

    tweets = client.get_users_tweets(id=user_id, max_results=5, tweet_fields=["created_at", "attachments"])

    if tweets.data:
        tweet = tweets.data[0]

        if tweet.id == previd:
            return None

        text = tweet.text.lower()
        if "india" in text or "pakistan" in text:
            tweet_data = {
                "id": tweet.id,
                "body": tweet.text,
                "link": f"https://twitter.com/{username}/status/{tweet.id}",
                "created_at": str(tweet.created_at),
                "metrics": tweet.public_metrics,
            }
            return tweet_data

    return None
