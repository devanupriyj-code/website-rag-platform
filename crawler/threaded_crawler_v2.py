from queue import Queue
import threading

from crawler.fetcher import fetch
from crawler.parser import parse_page, extract_links
from crawler.url_utils import (
    same_domain,
    normalize_url,
    get_crawl_domain,
)

from database.storage import save_page
from database.links import save_link


def crawl_site(
    seed_url,
    max_pages=100,
    num_workers=10
):

    seed_url = normalize_url(seed_url)

    crawl_domain = get_crawl_domain(
        seed_url
    )

    print()
    print("===== CRAWL START =====")
    print("Seed URL       :", seed_url)
    print("Allowed domain :", crawl_domain)

    visited = set()

    url_queue = Queue()

    lock = threading.Lock()

    pages_crawled = 0

    def worker():

        nonlocal pages_crawled

        while True:

            url = url_queue.get()

            if url is None:

                url_queue.task_done()
                break

            try:

                fetched = fetch(url)

                final_url = normalize_url(
                    fetched["url"]
                )

                print(
                    f"FETCH {url}"
                    f" -> {fetched['status_code']}"
                    f" -> {final_url}"
                )

                if fetched["redirects"]:
                    print(
                        "  redirects:",
                        fetched["redirects"]
                    )

                if fetched["status_code"] >= 400:
                    print(
                        f"  SKIP HTTP {fetched['status_code']}"
                    )
                    continue

                page, soup = parse_page(
                    final_url,
                    fetched["html"]
                )

                if page:

                    save_page(page)

                    links = extract_links(
                        final_url,
                        soup
                    )

                    accepted = 0

                    with lock:

                        pages_crawled += 1

                        print(
                            f"[{pages_crawled}] Saved:",
                            page["url"]
                        )
                        print(
                            f"  links extracted: {len(links)}"
                        )

                        for link in links:

                            link = normalize_url(
                                link
                            )

                            if same_domain(
                                link,
                                crawl_domain
                            ):

                                accepted += 1

                                save_link(
                                    final_url,
                                    link
                                )

                                if (
                                    link not in visited
                                    and len(visited)
                                    < max_pages
                                ):

                                    visited.add(
                                        link
                                    )

                                    url_queue.put(
                                        link
                                    )

                        print(
                            f"  links accepted: {accepted}"
                        )

            except Exception as e:

                print(
                    f"Error crawling {url}: {e}"
                )

            finally:

                url_queue.task_done()

    visited.add(
        seed_url
    )

    url_queue.put(
        seed_url
    )

    threads = []

    for _ in range(
        num_workers
    ):

        thread = threading.Thread(
            target=worker,
            daemon=True
        )

        thread.start()

        threads.append(
            thread
        )

    url_queue.join()

    for _ in range(
        num_workers
    ):

        url_queue.put(
            None
        )

    for thread in threads:

        thread.join()

    print()
    print(
        "===== CRAWL COMPLETE ====="
    )
    print(
        "Pages Crawled :",
        pages_crawled
    )
    print(
        "Visited URLs  :",
        len(visited)
    )
    print(
        "Workers       :",
        num_workers
    )

    return {
        "pages_crawled":
        pages_crawled,

        "visited":
        len(visited)
    }


if __name__ == "__main__":

    crawl_site(
        "https://www.python.org"
    )
