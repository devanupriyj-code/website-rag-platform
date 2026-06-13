from urllib.parse import urlparse


def normalize_url(url):

    parsed = urlparse(url)

    clean = (
        parsed.scheme +
        "://" +
        parsed.netloc +
        parsed.path
    )

    return clean.rstrip("/")


def get_crawl_domain(seed_url):

    netloc = urlparse(seed_url).netloc.lower()

    if netloc.startswith("www."):
        return netloc[4:]

    return netloc


def same_domain(url, crawl_domain):

    netloc = urlparse(url).netloc.lower()

    if netloc.startswith("www."):
        netloc = netloc[4:]

    crawl_domain = crawl_domain.lower()

    return (
        netloc == crawl_domain
        or netloc.endswith("." + crawl_domain)
    )
