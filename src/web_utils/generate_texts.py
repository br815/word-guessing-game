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

    # Avoid repeated consecutive underscores.
    filename = re.sub(r"_+", "_", filename)

    # Remove characters that are invalid in Windows filenames.
    filename = re.sub(r"[<>:/|?*\"\\]", "", filename)

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
   
    all_scraped_text = []
    print(f"URLs collected: {len(urls)}")
    for num, url in enumerate(urls, start=1):
        # Display URLs with numbers & parantheses: 1), 2), ... etc.
        print(f"{num}) {url}")
        # Try-except block is necessary in case downloading the webpage encounters any unexpected interruptions (see scrape_page() in web_scraper.py).
        try:
            current_scraped_text = scrape_page(url)
            # If scraping was successful on the current URL, format the scraped text for output to the text file.
            if current_scraped_text:
                if num != 1:
                    # Places a total of 3 blank lines before each scraped text, except for the 1st one.
                    all_scraped_text.append("\n\n")
                if config.GENERATE_TEXTS_DEBUGGER or config.DEBUG_ALL:
                    # Add a link header for debugging purposes only.
                    all_scraped_text.append("=" * config.BORDER_LEN)
                    all_scraped_text.append(f"SOURCE: {url}")
                    all_scraped_text.append("=" * config.BORDER_LEN)
                # Then add the current URL text to what will eventually be written to the text file.
                all_scraped_text.append(f"{current_scraped_text}")
        # Failure handled here instead of in scrape_page() because it is more logical to handle the failure at the level where scrape_page() is actually being called.
        # (Unlike in crawl(), where the same failure was more logical to handle directly in crawl().)
        except requests.RequestException as err_msg:
            print(f"ERROR: Could not scrape {url}: {err_msg}")

    if not all_scraped_text:
        raise ValueError("ERROR: The crawler found webpages, but no usable text could be extracted.")

    # Get timestamp & combine it with the seed URL to make the text file name.
    timestamp = datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
    filename = (f"{get_filename_from_url(seed_url)}_{timestamp}.txt")

    # Make path to text file.
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, filename)

    # Write final scraped texts to text file.
    final_text = "\n".join(all_scraped_text)
    with open(path, "w", encoding="utf-8") as file:
        file.write(final_text)

    return path
# End of generate_text_file()
