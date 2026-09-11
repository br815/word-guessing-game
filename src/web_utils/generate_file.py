import config
from web_utils.web_crawler import crawl
from web_utils.web_scraper import scrape

import os
import re
from datetime import datetime
from urllib.parse import urlparse
import requests



def get_file_name_from_url(url: str) -> str:
    """
    Create a filename from a webpage URL.

    The filename is based on the website domain and
    URL path rather than the webpage's HTML title.
    """

    # 1st: Get the domain name.
    parsed = urlparse(url)

    # Remove "www." from the domain.
    domain = parsed.netloc.removeprefix("www.")

    # Remove language subdomains such as "en." from Wikipedia and Wiktionary URLs.
    domain_parts = domain.split(".")

    if len(domain_parts) > 2:
        domain = ".".join(domain_parts[-2:])

    # Keep only the main domain name.
    domain = domain.split(".")[0]

    # 2nd: Get the URL path.
    path = parsed.path.strip("/")

    # Remove common file extensions.
    path = re.sub(r"\.(html?|php)$", "", path, flags=re.IGNORECASE)

    # Remove common filename prefixes/suffixes from Gutenberg-style ebook URLs.
    path = re.sub(r"pg(\d+)-images$", r"\1", path, flags=re.IGNORECASE)

    # Replace "/" with "_".
    path = path.replace("/", "_")

    # 3rd: Combine domain and path.
    file_name = f"{domain}_{path}"
    file_name = file_name.lower()

    # Avoid repeated consecutive underscores.
    file_name = re.sub(r"_+", "_", file_name)

    # Remove characters that are invalid in Windows file_names.
    file_name = re.sub(r"[<>:/|?*\"\\]", "", file_name)

    return file_name.strip("_.")
# End of get_file_name_from_url()



def generate_file(seed_url: str, num_webpages: int, dir_name: str) -> str:
    """
    Crawl and scrape webpages and save their text to an input file.

    Args:
        seed_url: Starting webpage supplied by the user.
        max_webpages: Maximum number of webpages to collect.
        dir_name: Directory in which to create the input file.

    Returns:
        Path to the newly created text file.

    Raises:
        ValueError: If no webpages or no usable text can be collected.
    """

    urls = crawl(seed_url, num_webpages)

    if not urls:
        raise ValueError("ERROR: The crawler could not access any webpages.")
   
    all_scraped_text = []
    for num, url in enumerate(urls, start=1):
        # Try-except block is necessary in case downloading the webpage encounters any unexpected interruptions (see scrape() in web_scraper.py).
        try:
            current_scraped_text = scrape(url)
            # If scraping was successful on the current URL, format the scraped text for output to the text file.
            if current_scraped_text:
                if num != 1:
                    # Places a total of 3 blank lines before each scraped text, except for the 1st one.
                    all_scraped_text.append("\n\n")
                if config.GENERATE_TEXTS_DEBUGGER or config.DEBUG_ALL:
                    # Add a header citing the source link for debugging purposes only.
                    all_scraped_text.append("=" * config.BORDER_LEN)
                    all_scraped_text.append(f"SOURCE: {url}")
                    all_scraped_text.append("=" * config.BORDER_LEN)
                # Then add the current URL's scraped text to what will eventually be written to the text file.
                all_scraped_text.append(f"{current_scraped_text}")
        # Exception handled here instead of in scrape() because it is more logical to handle the exception at the level where scrape() is actually being called.
        # (Unlike in crawl(), where the same exception was more logical to handle directly in crawl().)
        except requests.RequestException as err_msg:
            print(f"ERROR: Could not scrape {url}: {err_msg}")

    if not all_scraped_text:
        raise ValueError("ERROR: The crawler found webpages, but no usable text could be extracted.")

    # Get timestamp & combine it with the seed URL to make the text file name.
    timestamp = datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
    file_name = (f"{get_file_name_from_url(seed_url)}_{timestamp}.txt")

    # Make path to text file.
    os.makedirs(dir_name, exist_ok=True)
    file_path = os.path.join(dir_name, file_name)

    final_text = "\n".join(all_scraped_text)
    with open(file_path, "w", encoding="utf-8") as file:
        # Write final joined scraped texts to text file.
        file.write(final_text)
        # Add a newline to the end of the text file.
        file.write("\n")

    return file_path
# End of generate_file()
