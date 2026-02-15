from fastmcp import FastMCP
from mcp_servers.news_server.services.rss_service import fetch_google_news
from mcp_servers.news_server.services.cleaner import trim_text, clean_text

mcp = FastMCP("news-mcp")


def get_filtered_news_logic(
    topic: str = "world",
    fetch_limit: int = 10
):
    """
    Stable RSS-based news fetch.
    No scraping.
    Token-efficient.
    """

    articles = fetch_google_news(topic, fetch_limit)

    cleaned_articles = []

    for article in articles:
        #cleaned = clean_text(article["content"])
        # trimmed = trim_text(cleaned, max_words=200)

        cleaned_articles.append({
            "title": article["title"],
            "source": article["source"]
        })

    return cleaned_articles


@mcp.tool
def get_filtered_news(
    topic: str = "world",
    fetch_limit: int = 10
):
    return get_filtered_news_logic(topic, fetch_limit)
