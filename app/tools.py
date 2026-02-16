from crewai.tools import tool
from app.mcp_client import news_client, mail_client


@tool("get_filtered_news")
def news_tool(topic: str, fetch_limit: int = 10):
    """
    Fetch top news articles for a given topic.

    Args:
        topic (str): The news topic to search.
        fetch_limit (int): Number of articles to retrieve.

    Returns:
        List of news articles with title and source.
    """
    return news_client.call(
        "get_filtered_news",
        {"topic": topic, "fetch_limit": fetch_limit}
    )


@tool("send_email")
def mail_tool(to: str, subject: str, body: str):
    """
    Send an email to a recipient.

    Args:
        to (str): Recipient email address.
        subject (str): Email subject line.
        body (str): Email body content.

    Returns:
        Confirmation message from the mail server.
    """
    return mail_client.call(
        "send_email",
        {"to": to, "subject": subject, "body": body}
    )
