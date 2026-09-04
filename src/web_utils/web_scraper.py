import config
import re
import requests
from bs4 import BeautifulSoup



def scrape_page(url: str) -> str:
    """
    Extract the main textual content from a webpage.

    Args:
        url: URL of the webpage to scrape.

    Returns:
        Cleaned textual content.
    """

    response = requests.get(url, timeout=10, headers=config.REQUEST_HEADERS)
    response.raise_for_status()

    if config.WEB_SCRAPER_DEBUGGER or config.DEBUG_ALL:
        print(f"Scraping: {url}")
        print(f"Status: {response.status_code}")
        print(f"HTML length: {len(response.text)}")

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    # Remove elements that are not useful article content.
    for tag in soup([
        "script",
        "style",
        "noscript",
        "nav",
        "footer",
        "header",
        "aside",
        "form"
    ]):
        tag.decompose()

    # Find the main article.
    content = soup.find("article")

    if content is None:
        content = soup.find("main")

    if content is None:
        content = soup.body

    if content is None:
        return ""

    if config.WEB_SCRAPER_DEBUGGER or config.DEBUG_ALL:
        print(f"Content tag: {content.name}")
        print(f"Content id: {content.get('id')}")
        print(f"Content classes: {content.get('class')}")

    # Remove interactive elements.
    for tag in content.find_all(
        ["button", "input", "select", "textarea"]
    ):
        tag.decompose()

    # Extract paragraphs only.
    text_parts = []

    for paragraph in content.find_all("p"):
        text = paragraph.get_text(
            separator=" ",
            strip=True
        )

        if text:
            text_parts.append(text)

    # Put each paragraph on its own line.
    text = "\n".join(text_parts)

    # Remove visual separators.
    text = text.replace("|", " ")

    # Normalize whitespace.
    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    # Remove excessive blank lines.
    text = re.sub(
        r"\n\s*\n+",
        "\n\n",
        text
    ).strip()

    if config.WEB_SCRAPER_DEBUGGER or config.DEBUG_ALL:
        print(f"Extracted text length: {len(text)}")

    return text