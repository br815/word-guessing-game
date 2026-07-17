import config
import os
from datetime import datetime
from web_utils.web_scraper import scrape_page
from web_utils.web_crawler import crawl


def generate_text_file(seed_url: str, output_dir=config.TEXTS):
    """
    Crawl a website and build a text file for the game.

    Args:
        seed_url (str): Starting URL.
        output_dir (str): Where to save file.

    Returns:
        str: Path to created file.
    """

    urls = crawl(seed_url)

    all_text = []

    for url in urls:
        try:
            text = scrape_page(url)
            all_text.append(text)
        except Exception:
            continue

    final_text = "\n".join(all_text)

    os.makedirs(output_dir, exist_ok=True)

    filename = f"web_input_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    path = os.path.join(output_dir, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(final_text)

    return path