from typing import Any, List

from exceptions import InvalidTrieKeyError, InvalidPrefixTypeError

class _Node():
    """node used within the trie data structure, containing a dict of child nodes and a list of entries"""
    def __init__(self):
        self.children = {}
        self.entries = []


class Trie():
    """class defining a trie data structure including methods to insert items and search by a prefix"""
    def __init__(self):
        """init function assigns new node as the root and initialises a couner to zero"""
        self._root = _Node()
        self._counter = 0

    def insert(self, key: str, obj: Any) -> None:
        """takes a key and an object and inserts into a trie data structure, self._counter is used as an insertion ID"""

        # validation
        if not isinstance(key, str):
            raise InvalidTrieKeyError(key, "Key must be an instance of string")

        if not key.strip():
            raise InvalidTrieKeyError(key, "Key must not be empty or only whitespace")

        if key != key.strip() or "  " in key:
            raise InvalidTrieKeyError(key, "Key must not have malformed spacing")

        if "\t" in key or "\n" in key:
            raise InvalidTrieKeyError(key, "Key must not have tab or new line spacing")

        # entry id set to current counter
        entry_id = self._counter
        self._counter += 1 # counter increased

        words = key.split(' ')

        for word in words:
            node = self._root
            for char in word:
                if char not in node.children:
                   newEntry = _Node()
                   node.children[char] = newEntry
                   node = newEntry
                else: node = node.children[char]
            node.entries.append((entry_id, obj))


    def search_by_prefix(self, prefix: str) -> List[Any]:
        """takes in a prefix and returns all objects for which at least one word in the associated key begins with prefix"""
        if not isinstance(prefix, str):
            raise InvalidPrefixTypeError(prefix, "Prefix must be a valid instance of string")

        node = self._root
        for char in prefix:
            if char not in node.children: return []
            node = node.children[char]

        stack = [node]
        matches = {}
        while len(stack) > 0:
            current = stack.pop()
            for entry_id, obj in current.entries: 
                key = id(obj)
                if key not in matches or entry_id < matches[key][0]:
                    matches[key] = (entry_id, obj)
            for child in current.children.values(): stack.append(child)

        matches_sorted = sorted(matches.values(), key=lambda pair: pair[0])
        return [obj for _, obj in matches_sorted]