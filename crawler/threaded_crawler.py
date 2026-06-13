from concurrent.futures import ThreadPoolExecutor
import threading

from crawler.fetcher import fetch
from crawler.parser import (
    parse_page,
    extract_links
)
from crawler.url_utils import (
    same_domain
)

from database.storage import save_page

ALLOWED_DOMAIN = "python.org"

MAX_PAGES = 100
MAX_WORKERS = 10

visited = set()
queue = ["https://www.python.org"]

lock = threading.Lock()


def crawl_url(url):

    try:

        fetched = fetch(url)

        page, soup = parse_page(
            fetched["url"],
            fetched["html"]
        )

        if page is None:
            return

        save_page(page)

        links = extract_links(
            url,
            soup
        )

        new_links = []

        for link in links:

            if same_domain(
                link,
                ALLOWED_DOMAIN
            ):
                new_links.append(link)

        with lock:

            for link in new_links:

                if (
                    link not in visited
                    and link not in queue
                ):
                    queue.append(link)

        print(
            "Saved:",
            page["url"]
        )

    except Exception as e:

        print(
            "Error:",
            url,
            e
        )


def get_next_url():

    with lock:

        if not queue:
            return None

        url = queue.pop(0)

        if url in visited:
            return None

        visited.add(url)

        return url


with ThreadPoolExecutor(
    max_workers=MAX_WORKERS
) as executor:

    futures = []

    while len(visited) < MAX_PAGES:

        url = get_next_url()

        if url is None:

            if not futures:
                break

            continue

        futures.append(
            executor.submit(
                crawl_url,
                url
            )
        )

    for future in futures:
        future.result()

print()
print("===== DONE =====")
print("Visited:", len(visited))
print("Queue:", len(queue))