import json

def save_pages(pages):

    with open(
        "data/pages.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            pages,
            f,
            indent=4
        )