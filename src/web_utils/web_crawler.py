import config

from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup, Tag


    
def normalize_url(url: str) -> str:
    """
    Normalize a URL for crawl comparison.

    Fragments are removed because they do not identify
    a separate webpage.
    """

    parsed = urlparse(url)

    return parsed._replace(fragment="").geturl()
# End of normalize_url()



def is_valid_url(url: str, domain: str) -> bool:
    """
    Determine whether a URL can be crawled.

    A valid URL must:
    - use HTTP or HTTPS
    - belong to the seed domain
    - not point to an obvious non-HTML resource
    """

    parsed = urlparse(url)

    # Only HTTP and HTTPS URLs.
    if parsed.scheme not in {"http", "https"}:
        return False

    # Stay on the same domain.
    if parsed.netloc != domain:
        return False

    # Reject obvious non-HTML resources.
    excluded_extensions = (
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".svg",
        ".webp",
        ".ico",
        ".pdf",
        ".mp3",
        ".mp4",
        ".avi",
        ".mov",
        ".zip",
        ".doc",
        ".docx",
        ".xls",
        ".xlsx")

    if parsed.path.lower().endswith(excluded_extensions):
        return False
    
    return True
# End of is_valid_url()



def get_page_content(soup: BeautifulSoup) -> Tag | None:
    """
    Locate the main content area of a webpage.

    Falls back from article -> main -> body.
    """

    content = soup.find("article")

    if content is None:
        content = soup.find("main")

    if content is None:
        content = soup.find("body")

    return content
# End of get_page_content()



def get_candidate_urls(content: Tag, current_url: str, domain: str) -> list[str]:
    """
    Find eligible links inside paragraph text,
    in the order they appear.

    Returns:
        A list of unique URLs in document order.
    """

    candidates = []
    seen_urls = set()

    # Look only inside paragraphs rather than every
    # link contained anywhere in the main page area.
    for paragraph in content.find_all("p"):
        for link in paragraph.find_all("a", href=True):
            href = link.get("href")

            if not isinstance(href, str):
                continue

            full_url = urljoin(current_url, href)
            full_url = normalize_url(full_url)

            if not is_valid_url(full_url, domain):
                continue

            if full_url == current_url:
                continue

            if full_url in seen_urls:
                continue

            candidates.append(full_url)
            seen_urls.add(full_url)

    return candidates
# End of get_candidate_urls()



def crawl(seed_url: str, num_webpages: int) -> list[str]:
    """
    Crawl webpages beginning at seed_url.

    The crawler:
    - always includes the seed URL
    - stays on the seed domain
    - follows links found in main page content
    - considers links in document order
    - avoids duplicate URLs
    - counts the seed as one of max_webpages

    Args:
        seed_url:
            Starting webpage.

        max_webpages:
            Maximum total number of webpages to collect,
            including the seed URL.

    Returns:
        List of collected webpage URLs.
    """

    # Normalize the starting URL.
    seed_url = normalize_url(seed_url)

    parsed_seed = urlparse(seed_url)

    domain = parsed_seed.netloc

    visited = set()

    # Queue of URLs waiting to be crawled.
    to_visit = [seed_url]

    # URLs already placed in the queue.
    queued = {seed_url}

    collected_urls = []

    while (to_visit and len(collected_urls) < num_webpages):
        # FIFO queue: the first discovered URL is crawled first.
        url = to_visit.pop(0)

        if url in visited:
            continue

        try:
            response = requests.get(url, timeout=10, headers=config.REQUEST_HEADERS)
            response.raise_for_status()
        except requests.RequestException as err_msg:
            if config.WEB_CRAWLER_DEBUGGER or config.DEBUG_ALL:
                print(f"ERROR: Could not crawl {url}: {err_msg}")

            visited.add(url)
            continue

        visited.add(url)
        collected_urls.append(url)

        if config.WEB_CRAWLER_DEBUGGER or config.DEBUG_ALL:
            print(f"Crawled: {url}")

        # Parse the downloaded HTML.
        soup = BeautifulSoup(response.text, "html.parser")

        # Locate the main content.
        content = get_page_content(soup)

        if content is None:
            if config.WEB_CRAWLER_DEBUGGER or config.DEBUG_ALL:
                print(f"WARNING: No main content found: {url}")
            continue

        # Find links in the order they occur in the page's main content.
        candidates = get_candidate_urls(content, url, domain)

        # Add candidates to the crawl queue in document order.
        for candidate_url in candidates:

            if candidate_url in visited:
                continue

            if candidate_url in queued:
                continue

            # Stop adding URLs once we have enough pages waiting/collected to satisfy the requested maximum.
            if (len(collected_urls) + len(to_visit) >= num_webpages):
                break

            to_visit.append(candidate_url)
            queued.add(candidate_url)

    if config.WEB_CRAWLER_DEBUGGER or config.DEBUG_ALL:
        print(f"URLs collected: {len(collected_urls)}")

    return collected_urls
# End of crawl()
