import tweepy, os
from dotenv import load_dotenv
load_dotenv()
TWITTER_BEARER = os.getenv("TWITTER_BEARER")
client = tweepy.Client(bearer_token=TWITTER_BEARER)
def fetch_twitter(query="OSINT", count=20):
    tweets = client.search_recent_tweets(query=query, max_results=count, tweet_fields=["created_at", "text", "author_id"])
    results = []
    if tweets.data:
        for t in tweets.data:
            results.append({
                "platform": "twitter",
                "user": str(t.author_id),  # Note: author_id is numeric; use includes for username if needed
                "timestamp": str(t.created_at),
                "text": t.text,
                "url": f"https://twitter.com/i/web/status/{t.id}"
            })
    print("Twitter: Fetched", len(results), "tweets for query:", query)
    return results