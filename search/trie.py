class TrieNode:

    def __init__(self):

        self.children = {}
        self.is_word = False


class Trie:

    def __init__(self):

        self.root = TrieNode()

    def insert(self, word):

        node = self.root

        for char in word:

            if char not in node.children:

                node.children[char] = TrieNode()

            node = node.children[char]

        node.is_word = True

    def _collect(
        self,
        node,
        prefix,
        results,
        limit
    ):

        if len(results) >= limit:
            return

        if node.is_word:

            results.append(prefix)

        for char, child in node.children.items():

            self._collect(
                child,
                prefix + char,
                results,
                limit
            )

    def search_prefix(
        self,
        prefix,
        limit=10
    ):

        node = self.root

        for char in prefix:

            if char not in node.children:
                return []

            node = node.children[char]

        results = []

        self._collect(
            node,
            prefix,
            results,
            limit
        )

        return results