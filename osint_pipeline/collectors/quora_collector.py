import requests
from bs4 import BeautifulSoup

def fetch_quora(query="osint", limit=5):
    url = f"https://www.quora.com/search?q={query}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    for i, q in enumerate(soup.find_all("span", {"class": "q-text"})):
        if i >= limit:
            break
        results.append({
            "platform": "quora",
            "user": "anonymous",
            "timestamp": "N/A",
            "text": q.get_text(),
            "url": url
        })
    print(f"Quora: Fetched {len(results)} results for query '{query}'")
    return results
