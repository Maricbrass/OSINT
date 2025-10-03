# ...existing code...
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
import sqlite3

def plot_sentiment(db_path="data/osint.db"):
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql("SELECT * FROM osint_data", conn)
    except Exception as e:
        conn.close()
        print("Visualizer: failed to read DB/table:", e)
        return
    conn.close()
    if df.empty:
        print("Visualizer: no data found")
        return
    df["sentiment"] = df["text"].fillna("").apply(lambda x: TextBlob(x).sentiment.polarity)
    df.groupby("platform")["sentiment"].mean().plot(kind="bar")
    plt.title("Average Sentiment by Platform")
    plt.show()

def plot_post_frequency(db_path="data/osint.db"):
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql("SELECT * FROM osint_data", conn)
    except Exception as e:
        conn.close()
        print("Visualizer: failed to read DB/table:", e)
        return
    conn.close()
    if df.empty:
        print("Visualizer: no data found")
        return

    ts_col = df["timestamp"].astype(str).fillna("")
    nums = pd.to_numeric(ts_col, errors="coerce")
    ts = pd.to_datetime(nums, unit="s", errors="coerce", utc=True)
    mask = ts.isna()
    if mask.any():
        parsed = pd.to_datetime(ts_col[mask], errors="coerce", utc=True)
        ts.loc[mask] = parsed
    df["timestamp"] = ts
    df = df.dropna(subset=["timestamp"])
    if df.empty:
        print("Visualizer: no valid timestamps to plot")
        return

    if pd.api.types.is_datetime64tz_dtype(df["timestamp"]):
        df["timestamp"] = df["timestamp"].dt.tz_convert(None)
    df.set_index("timestamp", inplace=True)
    df.resample("D").size().plot()
    plt.title("Post Frequency Over Time")
    plt.show()

if __name__ == "__main__":
    # plot_post_frequency()
    plot_sentiment()
# ...existing code...