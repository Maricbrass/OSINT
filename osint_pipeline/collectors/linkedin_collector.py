from linkedin_api import Linkedin
import os
def fetch_linkedin(keyword="cybersecurity", limit=10):
    print(os.getenv("LK_MAIL"), os.getenv("LK_PASS"))
    api = Linkedin(os.getenv("LK_MAIL"), os.getenv("LK_PASS"))
    print(api)
    results = []
    people = api.search_people(keyword=keyword, limit=limit)
    for p in people:
        results.append({
        "platform": "linkedin",
        "user": p.get("public_id", ""),
        "timestamp": "N/A",
        "text": p.get("headline", ""),
        "url": f"https://linkedin.com/in/{p.get('public_id','')}"
        })
    print(f"LinkedIn: Fetched {len(results)} results for keyword '{keyword}'")
    return results