import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
import sqlite3
import base64
from io import BytesIO

def plot_sentiment(db_path="data/osint.db"):
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql("SELECT * FROM osint_data", conn)
    except Exception as e:
        conn.close()
        print("Visualizer: failed to read DB/table:", e)
        return None
    conn.close()
    if df.empty:
        print("Visualizer: no data found")
        return None
    df["sentiment"] = df["text"].fillna("").apply(lambda x: TextBlob(x).sentiment.polarity)
    df.groupby("platform")["sentiment"].mean().plot(kind="bar")
    plt.title("Average Sentiment by Platform")
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def plot_post_frequency(db_path="data/osint.db"):
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql("SELECT * FROM osint_data", conn)
    except Exception as e:
        conn.close()
        print("Visualizer: failed to read DB/table:", e)
        return None
    conn.close()
    if df.empty:
        print("Visualizer: no data found")
        return None

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
        return None

    if pd.api.types.is_datetime64tz_dtype(df["timestamp"]):
        df["timestamp"] = df["timestamp"].dt.tz_convert(None)
    df.set_index("timestamp", inplace=True)
    df.resample("D").size().plot()
    plt.title("Post Frequency Over Time")
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def plot_platform_distribution(db_path="data/osint.db"):
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql("SELECT platform FROM osint_data", conn)
    except Exception as e:
        conn.close()
        print("Visualizer: failed to read DB/table:", e)
        return None
    conn.close()
    if df.empty:
        return None
    df["platform"].value_counts().plot(kind="pie", autopct='%1.1f%%')
    plt.title("Data Distribution by Platform")
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def get_sentiment_data(db_path="data/osint.db"):
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql("SELECT * FROM osint_data", conn)
    except Exception as e:
        conn.close()
        print("Visualizer: failed to read DB/table:", e)
        return None
    conn.close()
    if df.empty:
        print("Visualizer: no data found")
        return None
    df["sentiment"] = df["text"].fillna("").apply(lambda x: TextBlob(x).sentiment.polarity)
    sentiment_means = df.groupby("platform")["sentiment"].mean()
    return {
        "labels": sentiment_means.index.tolist(),
        "datasets": [{
            "label": "Average Sentiment",
            "data": sentiment_means.values.tolist(),
            "backgroundColor": "rgba(75, 192, 192, 0.6)",
            "borderColor": "rgba(75, 192, 192, 1)",
            "borderWidth": 1
        }]
    }

def get_frequency_data(db_path="data/osint.db"):
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql("SELECT * FROM osint_data", conn)
    except Exception as e:
        conn.close()
        print("Visualizer: failed to read DB/table:", e)
        return None
    conn.close()
    if df.empty:
        print("Visualizer: no data found")
        return None

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
        return None

    if pd.api.types.is_datetime64tz_dtype(df["timestamp"]):
        df["timestamp"] = df["timestamp"].dt.tz_convert(None)
    df.set_index("timestamp", inplace=True)
    freq = df.resample("D").size()
    return {
        "labels": freq.index.strftime('%Y-%m-%d').tolist(),
        "datasets": [{
            "label": "Post Count",
            "data": freq.values.tolist(),
            "fill": False,
            "borderColor": "rgba(255, 99, 132, 1)",
            "backgroundColor": "rgba(255, 99, 132, 0.2)",
            "tension": 0.1
        }]
    }

def get_platform_data(db_path="data/osint.db"):
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql("SELECT platform FROM osint_data", conn)
    except Exception as e:
        conn.close()
        print("Visualizer: failed to read DB/table:", e)
        return None
    conn.close()
    if df.empty:
        return None
    platform_counts = df["platform"].value_counts()
    colors = ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF", "#FF9F40"]
    return {
        "labels": platform_counts.index.tolist(),
        "datasets": [{
            "data": platform_counts.values.tolist(),
            "backgroundColor": colors[:len(platform_counts)],
            "hoverOffset": 4
        }]
    }

if __name__ == "__main__":
    # plot_post_frequency()
    plot_sentiment()