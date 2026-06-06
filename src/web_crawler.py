from pathlib import Path
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup



# GLOBALS
TEXTS_DIR = Path("texts")
MAX_LINKS_PER_PAGE = 10



def fetch_page(url):
    """
    Downloads the HTML from a webpage.

    Returns:
        str  -> HTML text if successful
        None -> if request fails
    """

    try:
        response = requests.get(url, timeout=5)

        # Return None if webpage request failed
        if response.status_code != 200:
            return None

        return response.text

    except requests.RequestException:
        return None
# End of fetch_page()



def extract_links(html, base_url):
    """
    Extracts all links from HTML and converts
    relative URLs into absolute URLs.

    Returns:
        list[str]
    """

    soup = BeautifulSoup(html, "html.parser")

    links = []

    for tag in soup.find_all("a", href=True):

        href = tag["href"]

        # Convert relative URL -> absolute URL
        full_url = urljoin(base_url, href)

        # Only keep actual web pages
        if full_url.startswith("http"):
            links.append(full_url)

        # Limit links per page to avoid explosion
        if len(links) >= MAX_LINKS_PER_PAGE:
            break

    return links
# End of extract_links()



def extract_text(html):
    """
    Extracts visible text from HTML.

    Returns:
        str
    """

    soup = BeautifulSoup(html, "html.parser")

    # Remove script/style content
    for unwanted in soup(["script", "style"]):
        unwanted.decompose()

    text = soup.get_text(separator=" ")

    return text
# End of extract_text()



def save_page(filename, text):
    """
    Saves extracted text into the texts folder.
    """

    TEXTS_DIR.mkdir(exist_ok=True)

    filepath = TEXTS_DIR / filename

    with open(filepath, "w", encoding="utf-8") as outfile:
        outfile.write(text)
# End of save_page()



def crawl(url, depth, visited):
    """
    Recursively crawls webpages, extracts text,
    and stores text files locally.
    """

    # Stop condition
    if depth == 0 or url in visited:
        return

    print(f"Crawling: {url}")

    visited.add(url)

    # Download webpage
    html = fetch_page(url)

    # Stop if webpage could not be retrieved
    if html is None:
        print("Failed to retrieve webpage.")
        return

    # Extract webpage text
    text = extract_text(html)

    # Save webpage text locally
    filename = f"{hash(url)}.txt"
    save_page(filename, text)

    # Extract hyperlinks from webpage
    links = extract_links(html, url)

    # Recursively crawl discovered links
    for link in links:
        crawl(link, depth - 1, visited)
# End of crawl()



if __name__ == "__main__":

    START_URL = "https://example.com"
    MAX_DEPTH = 2

    visited_pages = set()

    crawl(
        url=START_URL,
        depth=MAX_DEPTH,
        visited=visited_pages
    )