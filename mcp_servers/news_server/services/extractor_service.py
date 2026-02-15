import requests
from readability import Document
from bs4 import BeautifulSoup


def extract_article_text(url: str):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return ""

        doc = Document(response.text)
        html = doc.summary()

        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator=" ")

        return text.strip()

    except Exception as e:
        return ""
