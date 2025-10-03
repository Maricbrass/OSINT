import os
import requests
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("VK_RAPID_KEY")
RAPIDAPI_HOST = os.getenv("VK_RAPID_HOST")

def _parse_rapid_item(item):
    text = item.get("text") or item.get("content") or item.get("body") or item.get("message") or ""
    user = str(item.get("user_id") or item.get("from_id") or item.get("owner_id") or item.get("author") or "")
    timestamp = str(item.get("date") or item.get("time") or item.get("created_at") or "")
    url = item.get("url") or item.get("link") or ""
    return {"platform": "vk", "user": user, "timestamp": timestamp, "text": text, "url": url}

def fetch_vk(query="cybersecurity", count=5):
    results = []

    if not RAPIDAPI_KEY or not RAPIDAPI_HOST:
        print("VK RapidAPI: VK_RAPID_KEY or VK_RAPID_HOST not set in environment")
        return results

    url = "https://vk-scraper.p.rapidapi.com/api/v1/search"
    params = {"query": query, "limit": count}
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.RequestException as e:
        resp = getattr(e, "response", None)
        if resp is not None:
            print(f"VK RapidAPI error {resp.status_code}: {resp.text}")
        else:
            print(f"VK RapidAPI request failed: {e}")
        return results
    except ValueError as e:
        print("VK RapidAPI: invalid JSON response:", e)
        return results

    candidates = []
    if isinstance(data, dict):
        for key in ("data", "items", "result", "posts", "results"):
            val = data.get(key)
            if isinstance(val, list) and val:
                candidates = val
                break
        if not candidates:
            for v in data.values():
                if isinstance(v, list):
                    candidates = v
                    break
    elif isinstance(data, list):
        candidates = data

    if not candidates:
        print("VK RapidAPI: no results found in response")
        return results

    for item in candidates[:count]:
        if isinstance(item, dict):
            results.append(_parse_rapid_item(item))
        else:
            results.append({"platform": "vk", "user": "", "timestamp": "", "text": str(item), "url": ""})

    print(f"VK (RapidAPI): Fetched {len(results)} results for query '{query}'")
    return results