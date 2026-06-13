from crawler.url_utils import normalize_url

visited = set()
queue = []

def add_url(url):

    url = normalize_url(url)

    if url not in visited and url not in queue:
        queue.append(url)

def get_next():

    if queue:
        return queue.pop(0)

    return None