from collectors.twitter_collector import fetch_twitter
from collectors.reddit_collector import fetch_reddit
from collectors.facebook_collector import fetch_facebook
from collectors.instagram_collector import fetch_instagram
from collectors.github_collector import fetch_github
from collectors.linkedin_collector import fetch_linkedin
# from collectors.discord_collector import on_message
from collectors.quora_collector import fetch_quora
# from collectors.telegram_collector import fetch_telegram
from collectors.tiktok_collector import fetch_tiktok
from collectors.vk_collector import fetch_vk
from utils.cleaner import clean_text, filter_english
from utils.database import save_to_db
from utils.sentiment import add_sentiment

def run_pipeline():
    # Collect
    data = []
    data.extend(fetch_twitter("AI", 10))
    data.extend(fetch_reddit("technology", 100))
    data.extend(fetch_facebook("paris", 5))
    data.extend(fetch_instagram("security", 10))
    data.extend(fetch_github("security", 50))
    data.extend(fetch_quora("Social Media", 50))
    data.extend(fetch_tiktok("cybersecurity", 5))
    data.extend(fetch_vk("paris", 5))
    # data.extend(fetch_telegram("osint_channel", 50))
    # data.extend(fetch_linkedin("cybersecurity", 5))
    # data.extend(on_message("cybersecurity"))

    # Clean
    for d in data:
        d["text"] = clean_text(d.get("text", ""))

    data = filter_english(data)

    # Enrich
    data = add_sentiment(data)

    # Store
    save_to_db(data)

    print(f"Collected and stored {len(data)} OSINT records.")
    print("Print record:")
    print(data)

if __name__ == "__main__":
    run_pipeline()