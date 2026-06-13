import json
from pathlib import Path

from search.trie import Trie

BASE_DIR = Path(__file__).resolve().parent.parent
INDEX_PATH = BASE_DIR / "data" / "index.json"

_trie = None
_index_mtime = None


def _load_trie():

    global _trie, _index_mtime

    mtime = INDEX_PATH.stat().st_mtime

    if _trie is None or mtime != _index_mtime:

        with open(
            INDEX_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            index = json.load(f)

        trie = Trie()

        for word in index.keys():

            trie.insert(word)

        _trie = trie
        _index_mtime = mtime

    return _trie


def get_suggestions(
    prefix,
    limit=10
):

    trie = _load_trie()

    return trie.search_prefix(
        prefix.lower(),
        limit
    )
