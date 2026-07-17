import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def is_valid_url(url: str, domain: str) -> bool:
    parsed = urlparse(url)
    return parsed.netloc == domain


def crawl(seed_url: str, max_pages: int = 10):
    """
    Crawl webpages starting from seed_url and collect URLs.

    Args:
        seed_url (str): Starting webpage.
        max_pages (int): Limit number of pages visited.

    Returns:
        list[str]: List of discovered URLs.
    """

    visited = set()
    to_visit = [seed_url]

    domain = urlparse(seed_url).netloc

    collected = []

    while to_visit and len(visited) < max_pages:

        url = to_visit.pop(0)

        if url in visited:
            continue

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except Exception:
            continue

        visited.add(url)
        collected.append(url)

        soup = BeautifulSoup(response.text, "html.parser")

        for link_tag in soup.find_all("a", href=True):
            full_url = urljoin(url, link_tag["href"])
            
            if is_valid_url(full_url, domain):
                if full_url not in visited:
                    to_visit.append(full_url)

    return collected