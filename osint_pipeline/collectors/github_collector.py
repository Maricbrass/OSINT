from github import Github
import os
def fetch_github(query="leak", limit=10):
    g = Github(os.getenv("GITHUB"))
    repos = g.search_repositories(query=query)
    results = []
    for repo in repos[:limit]:
        results.append({
            "platform": "github",
            "user": repo.owner.login,
            "timestamp": str(repo.created_at),
            "text": repo.description or "",
            "url": repo.html_url
        })
    print(f"GitHub: Fetched {len(results)} results for query '{query}'")
    return results