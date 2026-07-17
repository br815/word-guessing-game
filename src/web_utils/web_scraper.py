import re
import requests
from bs4 import BeautifulSoup


def scrape_page(url: str) -> str:
    """
    Fetch a webpage and extract visible text.

    Args:
        url (str): Webpage URL.

    Returns:
        str: Cleaned visible text content.
    """

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove scripts/styles
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ")

    # Clean whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text