from typing import List
from exceptions import HeapError

class Heap():
    def __init__(self):
        self._tree: List[tuple] = []
        self._counter = 0

    def __len__(self):
        return len(self._tree)

    def push(self, key, obj) -> None:
        """create a new entry, key, sequence (insertion order), and object, pushed up into the correct spot"""
        entry = (key, self._counter, obj)
        self._counter+=1
        self._tree.append(entry)
        self._sift_up(len(self._tree) -1)

    @staticmethod
    def _less(a, b):
        """check two tuples first against their key and second against their sequence assigned (order of insertion prioritised)"""
        return a[:2] < b[:2]

    def _sift_up(self, index: int) -> None:
        """take in an index, continue swapping elements with parents in the list until sequence/index is in order low - > high"""
        while index > 0:
            parent = (index - 1) // 2
            if self._less(self._tree[index], self._tree[parent]): # if index < parent
                self._tree[index], self._tree[parent] = self._tree[parent], self._tree[index]
                index = parent
            else: return
