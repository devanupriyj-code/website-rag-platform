import requests

USER_AGENT = (
    "MiniSearchEngineBot/1.0 "
    "(educational search engine crawler)"
)


def fetch(url):

    response = requests.get(
        url,
        timeout=10,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": (
                "text/html,application/xhtml+xml,"
                "application/xml;q=0.9,*/*;q=0.8"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        },
        allow_redirects=True,
    )

    return {
        "html": response.text,
        "url": response.url,
        "status_code": response.status_code,
        "redirects": [
            r.url
            for r in response.history
        ],
    }
