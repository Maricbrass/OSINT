import sqlite3
import os

def save_to_db(records, db_path="data/osint.db"):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS osint_data (
        platform TEXT,
        user TEXT,
        timestamp TEXT,
        text TEXT,
        url TEXT
    )""")
    inserted = 0
    for r in records:
        if not isinstance(r, dict):
            continue
        platform = r.get("platform", "")
        user = r.get("user", "")
        timestamp = r.get("timestamp", "")
        text = r.get("text", "")
        url = r.get("url", "")
        try:
            cur.execute(
                "INSERT INTO osint_data (platform, user, timestamp, text, url) VALUES (?, ?, ?, ?, ?)",
                (platform, user, timestamp, text, url)
            )
            inserted += 1
        except Exception as e:
            print("Database: failed to insert record:", e)
            continue
    conn.commit()
    conn.close()
    print(f"Database: saved {inserted} records to {db_path}")