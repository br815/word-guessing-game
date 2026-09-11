import config
from web_utils.web_crawler import get_webpage_content

import re
import requests
from bs4 import BeautifulSoup



def scrape(url: str) -> str:
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
        print(f"***URL INFO FROM SCRAPE(): {url}***")
        print(f"- Status: {response.status_code}")
        print(f"- HTML length: {len(response.text)}")

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove elements that are not useful article content.
    for tag in soup([
        "script",
        "style",
        "noscript",
        "nav",
        "footer",
        "header",
        "aside",
        "form"]):
        tag.decompose()

    # Locate the main webpage content.
    content = get_webpage_content(soup)
    if content is None:
        return ""

    if config.WEB_SCRAPER_DEBUGGER or config.DEBUG_ALL:
        print("***CONTENT INFO FROM SCRAPE()***")
        print(f"- Content tag: {content.name}")
        print(f"- Content ID: {content.get("id")}")
        print(f"- Content classes: {content.get("class")}")

    # Remove interactive elements.
    for tag in content.find_all(["button", "input", "select", "textarea"]):
        tag.decompose()

    # Extract paragraphs only.
    scraped_text_parts = []
    for paragraph in content.find_all("p"):
        scraped_text = paragraph.get_text(separator=" ", strip=True)
        if scraped_text:
            scraped_text_parts.append(scraped_text)

    # Put each paragraph on its own line.
    scraped_text = "\n".join(scraped_text_parts)

    # Special characters: remove only those which are unlikely to have lingustic or textual meaning in English text.
    scraped_text = re.sub(r"[|_~`\\]", " ", scraped_text)

    # Normalize whitespace.
    scraped_text = re.sub(r"[ \t]+", " ", scraped_text)

    # Replace excessive blank lines between paragraphs with 2 newlines to create 1 blank line between the paragraphs.
    scraped_text = re.sub(r"\n\s*\n+", "\n\n", scraped_text).strip()

    if config.WEB_SCRAPER_DEBUGGER or config.DEBUG_ALL:
        print(f"***EXTRACTED RAW TEXT LENGTH FROM SCRAPE(): {len(scraped_text)}***\n")

    return scraped_text
# End of scrape()
