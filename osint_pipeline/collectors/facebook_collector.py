import facebook, os
from dotenv import load_dotenv
load_dotenv()
FACEBOOK_TOKEN = os.getenv("FACEBOOK_TOKEN")
graph = facebook.GraphAPI(access_token=FACEBOOK_TOKEN)
def fetch_facebook(page_id="cnn", limit=10):
    posts = graph.get_connections(id=page_id, connection_name="posts")
    results = []
    for p in posts["data"][:limit]:
        if "message" in p:
            results.append({
            "platform": "facebook",
            "user": page_id,
            "timestamp": p.get("created_time"),
            "text": p["message"],
            "url": f"https://facebook.com/{p['id']}"
            })
    return results