from bs4 import BeautifulSoup
from urllib.parse import urljoin

def parse_page(url, html):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    title = (
        soup.title.string
        if soup.title
        else ""
    )

    text = soup.get_text(
        " ",
        strip=True
    )

    return {
        "url": url,
        "title": title,
        "content": text
    }, soup


def extract_links(base_url, soup):

    links = []

    for tag in soup.find_all("a"):

        href = tag.get("href")

        if href:

            absolute = urljoin(
                base_url,
                href
            )

            if absolute.startswith("http"):
                links.append(absolute)

    return links