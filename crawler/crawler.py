from crawler.fetcher import fetch
from crawler.parser import parse_page, extract_links
from crawler.queue_manager import (
    add_url,
    get_next,
    queue,
    visited
)
from crawler.url_utils import same_domain
from database.links import save_link
from database.storage import save_page

from urllib.parse import urlparse

domain = urlparse(
    seed_url
).netloc
MAX_PAGES = 20

pages = []

# Seed URL
add_url("https://www.python.org")

while queue and len(visited) < MAX_PAGES:

    url = get_next()

    if url is None:
        break

    if url in visited:
        continue

    print(f"[{len(visited) + 1}] Crawling: {url}")

    visited.add(url)

    try:

        fetched = fetch(url)

        page, soup = parse_page(
            fetched["url"],
            fetched["html"]
        )

        if page is None:
            continue

        # Store in memory
        pages.append(page)

        # Save immediately to SQLite
        save_page(page)

        print(f"Saved: {page['url']}")

        links = extract_links(
            url,
            soup
        )

        for link in links:

            if same_domain(
                link,
                ALLOWED_DOMAIN
            ):
                add_url(link)

    except Exception as e:

        print(
            f"Error crawling {url}: {e}"
        )

print("\n===== Crawl Finished =====")

print(
    "Pages Crawled :",
    len(pages)
)

print(
    "Visited URLs  :",
    len(visited)
)

print(
    "Queue Size    :",
    len(queue)
)
for link in links:

    save_link(
        url,
        link
    )

    if same_domain(
        link,
        ALLOWED_DOMAIN
    ):
        add_url(link)