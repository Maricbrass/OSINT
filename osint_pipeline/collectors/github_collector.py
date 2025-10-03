from github import Github, GithubException
import os
import random
from datetime import datetime, timedelta

def fetch_github(query="leak", limit=10):
    token = os.getenv("GITHUB")
    if token and token.strip():
        g = Github(token.strip())
    else:
        print("GitHub: GITHUB token not set, using unauthenticated client (rate-limited).")
        g = Github()

    try:
        repos = g.search_repositories(query=query)
    except GithubException as e:
        # log error and attempt fallback to unauthenticated client if token was used
        status = getattr(e, "status", None)
        data = getattr(e, "data", None)
        print(f"GitHub API error {status}: {data or e}")
        if token:
            print("Falling back to unauthenticated client (may be rate-limited).")
            g = Github()
            try:
                repos = g.search_repositories(query=query)
            except GithubException as e2:
                print(f"GitHub fallback also failed: {getattr(e2,'status',None)} {getattr(e2,'data',None) or e2}")
                return []
        else:
            return []

    results = []
    for i, repo in enumerate(repos):
        if i >= limit:
            break
        results.append({
            "platform": "github",
            "user": repo.owner.login,
            "timestamp": str(repo.created_at),
            "text": repo.description or "",
            "url": repo.html_url
        })
    print(f"GitHub: Fetched {len(results)} results for query '{query}'")
    return results