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



def get_webpage_content(soup: BeautifulSoup) -> Tag | None:
    """
    Locate the best available "main" content container by a hierarchy of descending best fit: article -> main -> body.
    
    This function is called by crawl(), so it can extract more links from the main content area to crawl.

    This function is also called by scrape_page(), which needs to extract paragraphs from the main content area.
    """

    content = soup.find("article")

    if content is None:
        content = soup.find("main")

    if content is None:
        content = soup.find("body")

    return content
# End of get_webpage_content()



def get_candidate_urls(content: Tag, current_url: str, domain: str) -> list[str]:
    """
    Find eligible links inside paragraph text,
    in the order they appear.

    Returns:
        A list of unique URLs in document order.
    """

    candidate_urls = []
    seen_urls = set()

    # Look only inside paragraphs rather than every link contained anywhere in the main page area.
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

            candidate_urls.append(full_url)
            seen_urls.add(full_url)

    return candidate_urls
# End of get_candidate_urls()



def crawl(seed_url: str, num_webpages: int) -> list[str]:
    """
    Crawl webpages beginning at seed_url.

    The crawler:
    - always includes the seed URL
    - stays on the seed domain
    - follows links found in main page content
    - considers links in document order (breadth-first)
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

    # Extract the seed domain.
    parsed_seed = urlparse(seed_url)
    domain = parsed_seed.netloc

    # List of URLs (acts as a FIFO queue) that have been discovered but haven't been crawled yet.
    urls_to_visit = [seed_url]
    # Set to keep track of which URLs have been placed into the queue of URLs to visit.
    queued_urls = {seed_url}
    # Set of URLs that the crawler has attempted to crawl.
    visited_urls = set()
    # List of webpages that have been successfully crawled and counted toward the requested number of webpages.
    collected_urls = []

    while (urls_to_visit and len(collected_urls) < num_webpages):
        # FIFO queue: the first discovered URL is crawled first.
        url = urls_to_visit.pop(0)
        # Check if URL has already been visited.
        if url in visited_urls:
            continue

        # Try-except block is necessary in case downloading the webpage encounters any unexpected interruptions.
        try:
            response = requests.get(url, timeout=10, headers=config.REQUEST_HEADERS)
            response.raise_for_status()
        except requests.RequestException as err_msg:
            print(f"ERROR: Could not crawl {url}: {err_msg}")
            # Count the URL as visited even if it can't be crawled.
            visited_urls.add(url)
            continue

        # Add URL to visited URLs set once it has been visited.
        visited_urls.add(url)

        # Parse the downloaded HTML.
        soup = BeautifulSoup(response.text, "html.parser")

        # Locate the main webpage content.
        content = get_webpage_content(soup)
        if content is None:
            print(f"ERROR: No main content found: {url}")
            continue

        # Add URL to collected URLs list if its main content has been found.
        collected_urls.append(url)

        if config.WEB_CRAWLER_DEBUGGER or config.DEBUG_ALL:
            print(f"Successfully crawled: {url}")

        # Find links in the order they occur in the page's main content.
        candidate_urls = get_candidate_urls(content, url, domain)

        # Add candidate URLs to the crawl queue in document order.
        for candidate_url in candidate_urls:
            # Skip URL if it is already visited or queued.
            if candidate_url in visited_urls or candidate_url in queued_urls:
                continue

            # Stop adding URLs once there are enough webpages waiting/collected to satisfy the requested maximum.
            if (len(collected_urls) + len(urls_to_visit) >= num_webpages):
                break

            # Add url to pending URLs list and queued URLs set.
            urls_to_visit.append(candidate_url)
            queued_urls.add(candidate_url)

    if config.WEB_CRAWLER_DEBUGGER or config.DEBUG_ALL:
        print(f"URLs collected: {len(collected_urls)}\n")

    return collected_urls
# End of crawl()
