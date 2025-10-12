from flask import Flask, render_template, request
import sqlite3
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'osint_pipeline'))
from main import run_pipeline
from utils.visualizer import plot_sentiment, plot_post_frequency, plot_platform_distribution, get_sentiment_data, get_frequency_data, get_platform_data

app = Flask(__name__)

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), 'osint_pipeline', 'data', 'osint.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').strip()
    if not query:
        return render_template('results.html', results=[], query=query)

    # Trigger collection with the query
    try:
        run_pipeline(query)
    except Exception as e:
        print(f"Error during collection: {e}")
        # Continue to show existing results

    conn = get_db_connection()
    cursor = conn.cursor()
    # Search in text field, case-insensitive
    cursor.execute("""
        SELECT platform, user, timestamp, text, url
        FROM osint_data
        WHERE text LIKE ?
        ORDER BY timestamp DESC
    """, ('%' + query + '%',))
    rows = cursor.fetchall()
    conn.close()

@app.route('/database', methods=['GET'])
def database():
    page = int(request.args.get('page', 1))
    per_page = 50
    offset = (page - 1) * per_page

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM osint_data")
    total = cursor.fetchone()[0]
    cursor.execute("""
        SELECT platform, user, timestamp, text, url
        FROM osint_data
        ORDER BY timestamp DESC
        LIMIT ? OFFSET ?
    """, (per_page, offset))
    rows = cursor.fetchall()
    conn.close()

    results = [dict(row) for row in rows]
    total_pages = (total + per_page - 1) // per_page
    return render_template('database.html', results=results, page=page, total_pages=total_pages)

@app.route('/charts')
def charts():
    sentiment_data = get_sentiment_data(os.path.join(os.path.dirname(__file__), 'osint_pipeline', 'data', 'osint.db'))
    frequency_data = get_frequency_data(os.path.join(os.path.dirname(__file__), 'osint_pipeline', 'data', 'osint.db'))
    platform_data = get_platform_data(os.path.join(os.path.dirname(__file__), 'osint_pipeline', 'data', 'osint.db'))
    return render_template('charts.html', sentiment_data=sentiment_data, frequency_data=frequency_data, platform_data=platform_data)

if __name__ == '__main__':
    app.run(debug=True)