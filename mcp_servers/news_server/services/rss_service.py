import feedparser
from bs4 import BeautifulSoup
from urllib.parse import quote


def fetch_google_news(topic: str = "world", limit: int = 10):
    # 🔥 Encode topic properly
    encoded_topic = quote(topic)

    url = (
        f"https://news.google.com/rss/search?"
        f"q={encoded_topic}&hl=en-IN&gl=IN&ceid=IN:en"
    )

    feed = feedparser.parse(url)

    articles = []

    for entry in feed.entries[:limit]:
        source = ""
        summary_text = ""

        if "description" in entry:
            soup = BeautifulSoup(entry.description, "html.parser")

            # Extract publisher
            font_tag = soup.find("font")
            if font_tag:
                source = font_tag.text.strip()

            # Extract clean summary text
            #summary_text = soup.get_text(separator=" ").strip()

        articles.append({
            "title": entry.title,
            "source": source,
            # "content": summary_text
        })

    return articles
