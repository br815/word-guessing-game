import config
from web_utils.web_crawler import crawl
from web_utils.web_scraper import scrape_page

import os
import re
from datetime import datetime
from urllib.parse import urlparse
import requests



def get_filename_from_url(url: str) -> str:
    """
    Create a filename from a webpage URL.

    The filename is based on the website domain and
    URL path rather than the webpage's HTML title.
    """

    parsed = urlparse(url)

    # Remove "www." from the domain.
    domain = parsed.netloc.removeprefix("www.")

    # Remove language subdomains such as "en." from Wikipedia and Wiktionary URLs.
    domain_parts = domain.split(".")

    if len(domain_parts) > 2:
        domain = ".".join(domain_parts[-2:])

    # Keep only the main domain name.
    domain = domain.split(".")[0]

    # Get the URL path.
    path = parsed.path.strip("/")

    # Remove common file extensions.
    path = re.sub(r"\.(html?|php)$", "", path, flags=re.IGNORECASE)

    # Remove common filename prefixes/suffixes from Gutenberg-style ebook URLs.
    path = re.sub(r"pg(\d+)-images$", r"\1", path, flags=re.IGNORECASE)

    # Replace "/" with "_".
    path = path.replace("/", "_")

    # Combine domain and path.
    filename = f"{domain}_{path}"
    filename = filename.lower()

    # Remove characters that are invalid in Windows filenames.
    filename = re.sub(r'[<>:"/\\|?*]', "", filename)

    # Avoid repeated underscores.
    filename = re.sub(r"_+", "_", filename)

    return filename.strip("_.")
# End of get_filename_from_url()



def generate_text_file(seed_url: str, num_webpages: int, output_dir=config.TEXTS) -> str:
    """
    Crawl and scrape webpages and save their text to an input file.

    Args:
        seed_url: Starting webpage supplied by the user.
        max_webpages: Maximum number of webpages to collect.
        output_dir: Directory in which to create the input file.

    Returns:
        Path to the newly created text file.

    Raises:
        ValueError: If no webpages or no usable text can be collected.
    """

    urls = crawl(seed_url, num_webpages)

    if not urls:
        raise ValueError("ERROR: The crawler could not access any webpages.")

    print(f"URLs collected: {len(urls)}")

    for url in urls:
        print(f"  - {url}")

    all_text = []

    for url in urls:
        try:
            text = scrape_page(url)
            if text:
                all_text.append(f"\n\n{'=' * 50}\nSOURCE: {url}\n{'=' * 50}\n\n{text}")

        except requests.RequestException as err_msg:
            print(f"ERROR: Could not scrape {url}: {err_msg}")

    if not all_text:
        raise ValueError("ERROR: The crawler found webpages, but no usable text could be extracted.")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = (f"{get_filename_from_url(seed_url)}_{timestamp}.txt")

    os.makedirs(output_dir, exist_ok=True)

    path = os.path.join(output_dir, filename)

    final_text = "\n".join(all_text)

    with open(path, "w", encoding="utf-8") as file:
        file.write(final_text)

    return path
# End of generate_text_file()
