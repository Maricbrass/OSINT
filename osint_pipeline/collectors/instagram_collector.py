import instaloader, os, time
from dotenv import load_dotenv
from instaloader import ConnectionException, Profile, ProfileNotExistsException

load_dotenv()
INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")
SESSION_FILE = os.getenv("INSTALOADER_SESSION_FILE")  # optional full path

L = instaloader.Instaloader(download_pictures=False, download_videos=False,
                            save_metadata=False, compress_json=False)

# Try to load existing session, else login and save session
def _ensure_session():
    if not INSTAGRAM_USERNAME:
        print("Instagram: INSTAGRAM_USERNAME not set")
        return False
    try:
        if SESSION_FILE and os.path.exists(SESSION_FILE):
            L.load_session_from_file(INSTAGRAM_USERNAME, SESSION_FILE)
            return True
        try:
            L.load_session_from_file(INSTAGRAM_USERNAME)
            return True
        except FileNotFoundError:
            pass
        if INSTAGRAM_PASSWORD:
            L.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
            try:
                L.save_session_to_file(SESSION_FILE or None)
            except Exception:
                pass
            return True
        print("Instagram: no session and no password provided")
        return False
    except Exception as e:
        print("Instagram: session/login failed:", e)
        return False

_session_ready = _ensure_session()

def fetch_instagram(username="bbcnews", limit=5):
    if not _session_ready:
        print("Instagram: proceeding unauthenticated (may be rate-limited)")
    # small retry/backoff loop
    attempts = 3
    for attempt in range(1, attempts + 1):
        try:
            profile = Profile.from_username(L.context, username)
            break
        except (ConnectionException,) as e:
            print(f"Instagram: connection error (attempt {attempt}/{attempts}): {e}")
            if attempt < attempts:
                time.sleep(5 * attempt)
                continue
            return []
        except ProfileNotExistsException:
            print(f"Instagram: profile '{username}' does not exist")
            return []
        except Exception as e:
            print("Instagram: unexpected error:", e)
            return []
    results = []
    try:
        for i, post in enumerate(profile.get_posts()):
            if i >= limit: break
            results.append({
                "platform": "instagram",
                "user": username,
                "timestamp": str(post.date),
                "text": post.caption or "",
                "url": getattr(post, "url", f"https://www.instagram.com/p/{post.shortcode}/")
            })
    except ConnectionException as e:
        print("Instagram: connection lost while fetching posts:", e)
    return results