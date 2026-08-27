import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

import config


REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/151.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def normalize_url(url: str) -> str:
    """
    Normalize a URL for crawl comparison.

    Fragments are removed because they do not identify
    a separate webpage.
    """

    parsed = urlparse(url)

    return parsed._replace(
        fragment=""
    ).geturl()


def is_valid_url(
    url: str,
    domain: str
) -> bool:
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
        ".xlsx",
    )

    if parsed.path.lower().endswith(
        excluded_extensions
    ):
        return False

    return True


def get_page_content(
    soup: BeautifulSoup
):
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


def get_candidate_urls(
    content,
    current_url: str,
    domain: str
) -> list[str]:
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

        for link in paragraph.find_all(
            "a",
            href=True
        ):

            href = link.get("href")

            if not isinstance(href, str):
                continue

            full_url = urljoin(
                current_url,
                href
            )

            full_url = normalize_url(
                full_url
            )

            if not is_valid_url(
                full_url,
                domain
            ):
                continue

            if full_url == current_url:
                continue

            if full_url in seen_urls:
                continue

            candidates.append(
                full_url
            )

            seen_urls.add(
                full_url
            )

    return candidates


def crawl(
    seed_url: str,
    max_pages: int = 5
) -> list[str]:
    """
    Crawl webpages beginning at seed_url.

    The crawler:
    - always includes the seed URL
    - stays on the seed domain
    - follows links found in main page content
    - considers links in document order
    - avoids duplicate URLs
    - counts the seed as one of max_pages

    Args:
        seed_url:
            Starting webpage.

        max_pages:
            Maximum total number of webpages to collect,
            including the seed URL.

    Returns:
        List of collected webpage URLs.
    """

    if max_pages < 1:
        raise ValueError(
            "ERROR: Number of webpages must be at least 1."
        )

    # Normalize the starting URL.
    seed_url = normalize_url(
        seed_url
    )

    parsed_seed = urlparse(
        seed_url
    )

    domain = parsed_seed.netloc

    visited = set()

    # Queue of URLs waiting to be crawled.
    to_visit = [seed_url]

    # URLs already placed in the queue.
    queued = {seed_url}

    collected = []

    while (
        to_visit
        and len(collected) < max_pages
    ):

        # FIFO queue:
        # the first discovered URL is crawled first.
        url = to_visit.pop(0)

        if url in visited:
            continue

        try:
            response = requests.get(
                url,
                timeout=10,
                headers=REQUEST_HEADERS
            )

            response.raise_for_status()

        except requests.RequestException as err_msg:

            if config.CRAWLER_DEBUGGER:
                print(
                    f"ERROR: Could not crawl "
                    f"{url}: {err_msg}"
                )

            visited.add(url)
            continue

        visited.add(url)
        collected.append(url)

        if config.CRAWLER_DEBUGGER:
            print(
                f"Crawled: {url}"
            )

        # Parse the downloaded HTML.
        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Locate the main content.
        content = get_page_content(
            soup
        )

        if content is None:
            if config.CRAWLER_DEBUGGER:
                print(
                    f"WARNING: No main content found: "
                    f"{url}"
                )

            continue

        # Find links in the order they occur in
        # the page's main content.
        candidates = get_candidate_urls(
            content,
            url,
            domain
        )

        # Add candidates to the crawl queue in
        # document order.
        for candidate_url in candidates:

            if candidate_url in visited:
                continue

            if candidate_url in queued:
                continue

            # Stop adding URLs once we have enough
            # pages waiting/collected to satisfy the
            # requested maximum.
            if (
                len(collected) + len(to_visit)
                >= max_pages
            ):
                break

            to_visit.append(
                candidate_url
            )

            queued.add(
                candidate_url
            )

    if config.CRAWLER_DEBUGGER:
        print(
            f"URLs collected: "
            f"{len(collected)}"
        )

    return collected