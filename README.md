# OSINT Pipeline

A comprehensive Open Source Intelligence (OSINT) data collection and analysis pipeline that aggregates data from multiple social media platforms and performs sentiment analysis.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📋 Overview

This OSINT pipeline automates the collection, processing, and analysis of publicly available data from various social media platforms. It provides a unified framework for gathering intelligence, performing text analysis, and storing results in a structured database.

### Supported Platforms

- 🐦 **Twitter/X** - Collect tweets using Tweepy
- 🤖 **Reddit** - Fetch posts and comments from subreddits
- 📘 **Facebook** - Gather public posts and data
- 📸 **Instagram** - Collect posts and metadata using Instaloader
- 🐙 **GitHub** - Search repositories, issues, and discussions
- 💼 **LinkedIn** - Extract professional content and posts
- 💬 **Discord** - Monitor Discord channels
- ❓ **Quora** - Scrape questions and answers
- 📱 **Telegram** - Collect messages from channels
- 🎵 **TikTok** - Gather video metadata and content
- 🌐 **VK** - Collect data from VK social network
- 🐘 **Mastodon** - Fetch toots from Mastodon instances

## 🚀 Features

- **Multi-Platform Data Collection**: Aggregate data from 12+ social media platforms
- **Automated Scheduling**: Run collection tasks on a configurable schedule
- **Text Processing**: Clean and normalize collected text data
- **Language Filtering**: Filter content by language (English by default)
- **Sentiment Analysis**: Automatic sentiment scoring using TextBlob
- **SQLite Database**: Store all collected data in a structured database
- **Extensible Architecture**: Easy to add new collectors and processors

## 📁 Project Structure

```
OSINT/
├── osint_pipeline/
│   ├── main.py                 # Main pipeline orchestration
│   ├── automate.py            # Scheduled automation script
│   ├── collectors/            # Platform-specific collectors
│   │   ├── twitter_collector.py
│   │   ├── reddit_collector.py
│   │   ├── facebook_collector.py
│   │   ├── instagram_collector.py
│   │   ├── github_collector.py
│   │   ├── linkedin_collector.py
│   │   ├── discord_collector.py
│   │   ├── quora_collector.py
│   │   ├── telegram_collector.py
│   │   ├── tiktok_collector.py
│   │   ├── vk_collector.py
│   │   └── mastodon_collector.py
│   ├── utils/                 # Utility modules
│   │   ├── cleaner.py        # Text cleaning and filtering
│   │   ├── database.py       # Database operations
│   │   ├── sentiment.py      # Sentiment analysis
│   │   └── visualizer.py     # Data visualization
│   └── data/
│       └── osint.db          # SQLite database
├── data/
│   └── osint.db              # Alternative database location
├── screenshots/              # Project screenshots
├── requirements.txt          # Python dependencies
├── .gitignore
└── README.md
```

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- API credentials for the platforms you want to collect from

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Maricbrass/OSINT.git
   cd OSINT
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API credentials**
   
   Create a `.env` file in the project root with your API credentials:
   
   ```env
   # Twitter/X
   TWITTER_API_KEY=your_api_key
   TWITTER_API_SECRET=your_api_secret
   TWITTER_ACCESS_TOKEN=your_access_token
   TWITTER_ACCESS_SECRET=your_access_secret
   
   # Reddit
   REDDIT_CLIENT_ID=your_client_id
   REDDIT_CLIENT_SECRET=your_client_secret
   REDDIT_USER_AGENT=your_user_agent
   
   # Facebook
   FACEBOOK_ACCESS_TOKEN=your_access_token
   
   # Instagram
   INSTAGRAM_USERNAME=your_username
   INSTAGRAM_PASSWORD=your_password
   
   # GitHub
   GITHUB_TOKEN=your_personal_access_token
   
   # LinkedIn
   LINKEDIN_EMAIL=your_email
   LINKEDIN_PASSWORD=your_password
   
   # Add other platform credentials as needed
   ```

4. **Download NLTK data (for text processing)**
   ```python
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```

## 💻 Usage

### Run a Single Collection

To run the pipeline once:

```bash
cd osint_pipeline
python main.py
```

This will:
1. Collect data from all configured platforms
2. Clean and filter the text
3. Perform sentiment analysis
4. Store results in the SQLite database

### Run Automated Collection

To run the pipeline on a schedule (default: every hour):

```bash
cd osint_pipeline
python automate.py
```

Press `Ctrl+C` to stop the scheduler.

### Customize Collection Parameters

Edit `main.py` to customize what data to collect:

```python
def run_pipeline():
    data = []
    # Customize search terms and limits
    data.extend(fetch_twitter("your_search_term", 10))
    data.extend(fetch_reddit("your_subreddit", 100))
    data.extend(fetch_github("your_topic", 50))
    # Add more collectors as needed
    
    # Process and store data
    for d in data:
        d["text"] = clean_text(d.get("text", ""))
    data = filter_english(data)
    data = add_sentiment(data)
    save_to_db(data)
```

## 📊 Database Schema

The collected data is stored in SQLite with the following schema:

```sql
CREATE TABLE osint_data (
    platform TEXT,      -- Source platform (twitter, reddit, etc.)
    user TEXT,          -- Username or author
    timestamp TEXT,     -- Post/content timestamp
    text TEXT,          -- Collected text content
    url TEXT,           -- URL to original content
    sentiment REAL      -- Sentiment score (-1 to 1)
)
```

## 🔧 Configuration

### Modify Collection Schedule

Edit `automate.py` to change the collection frequency:

```python
# Run every hour (default)
schedule.every(1).hours.do(run_pipeline)

# Or use other intervals:
schedule.every(30).minutes.do(run_pipeline)
schedule.every().day.at("10:30").do(run_pipeline)
schedule.every().monday.do(run_pipeline)
```

### Add Custom Collectors

Create a new collector in `osint_pipeline/collectors/`:

```python
# your_platform_collector.py
def fetch_your_platform(query, limit):
    results = []
    # Your collection logic here
    for item in your_api_call(query, limit):
        results.append({
            "platform": "your_platform",
            "user": item.author,
            "timestamp": item.date,
            "text": item.content,
            "url": item.url
        })
    return results
```

Then import and use it in `main.py`:

```python
from collectors.your_platform_collector import fetch_your_platform
# ...
data.extend(fetch_your_platform("query", 10))
```

## 📈 Data Analysis

Use the utilities for data analysis:

- **Text Cleaning**: `utils/cleaner.py` - Remove special characters, URLs, normalize text
- **Sentiment Analysis**: `utils/sentiment.py` - Calculate sentiment polarity scores
- **Visualization**: `utils/visualizer.py` - Create charts and visualizations (customize as needed)

## 🔒 Security & Ethics

### Important Considerations

⚠️ **Legal & Ethical Usage**:
- Always comply with platform Terms of Service (ToS)
- Respect rate limits and robots.txt
- Only collect publicly available data
- Obtain necessary permissions and API access
- Follow data protection regulations (GDPR, CCPA, etc.)
- Use collected data responsibly and ethically

⚠️ **API Credentials**:
- Never commit API keys or credentials to version control
- Use `.env` files or environment variables
- Rotate credentials regularly
- Follow the principle of least privilege

## 🐛 Troubleshooting

### Common Issues

1. **API Rate Limits**: Reduce collection limits or increase delays between requests
2. **Authentication Errors**: Verify your API credentials in `.env`
3. **Missing Dependencies**: Run `pip install -r requirements.txt` again
4. **Database Locked**: Ensure only one instance is writing to the database

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Contact

Project Maintainer: Maricbrass
- GitHub: [@Maricbrass](https://github.com/Maricbrass)

## 🙏 Acknowledgments

- Built with Python and open-source libraries
- Uses APIs from various social media platforms
- Sentiment analysis powered by TextBlob
- Natural language processing with NLTK

## 📸 Screenshots

See the `screenshots/` folder for example outputs and visualizations.

---

**Disclaimer**: This tool is for educational and research purposes only. Users are responsible for ensuring compliance with all applicable laws, regulations, and terms of service when collecting and analyzing data.
