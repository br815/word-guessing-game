import os
import requests
from datetime import datetime
from urllib.parse import urlparse

import config
from web_utils.web_crawler import crawl
from web_utils.web_scraper import scrape_page


def generate_text_file(
    seed_url: str,
    max_pages: int = 3,
    output_dir=config.TEXTS
):
    """
    Crawl and scrape webpages and save their text to an input file.

    Args:
        seed_url: Starting webpage supplied by the user.
        max_pages: Maximum number of webpages to collect.
        output_dir: Directory in which to create the input file.

    Returns:
        Path to the newly created text file.

    Raises:
        ValueError: If no webpages or no usable text can be collected.
    """

    urls = crawl(
        seed_url,
        max_pages
    )

    if not urls:
        raise ValueError(
            "ERROR: The crawler could not access any webpages."
        )

    print(f"URLs collected: {len(urls)}")

    for url in urls:
        print(f"  - {url}")

    all_text = []

    for url in urls:
        try:
            text = scrape_page(url)

            if text:
                all_text.append(
                    f"\n\n{'=' * 50}\n"
                    f"SOURCE: {url}\n"
                    f"{'=' * 50}\n\n"
                    f"{text}"
                )

        except requests.RequestException as err_msg:
            print(
                f"ERROR: Could not scrape {url}: {err_msg}"
            )

    if not all_text:
        raise ValueError(
            "ERROR: The crawler found webpages, "
            "but no usable text could be extracted."
        )

    final_text = "\n".join(all_text)

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    # Use the domain as the basis for the filename.
    domain = urlparse(seed_url).netloc
    domain = domain.removeprefix("www.")
    domain = domain.replace(".", "_")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"{domain}_{timestamp}.txt"

    path = os.path.join(
        output_dir,
        filename
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(final_text)

    return path
# End of generate_text_file()