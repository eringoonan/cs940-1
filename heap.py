from typing import Any, List
from exceptions import HeapError

class Heap():
    def __init__(self):
        self._tree: List[tuple] = []
        self._counter = 0

    def __len__(self):
        return len(self._tree)

    def __bool__(self):
        """"""

    def __repr__(self):
        """"""

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

    def _sift_down(self, index: int) -> None:
        """take an index and sift the value at index down the tree until it reaches the correct spot"""
        while True:
            left = 2 * index + 1
            if left >= len(self._tree): return
            smallest = left
            if(left + 1 < len(self._tree)) and (self._less(self._tree[left+1], self._tree[left])): smallest = left+1
            if not self._less(self._tree[smallest], self._tree[index]): return
            self._tree[smallest], self._tree[index] = self._tree[index], self._tree[smallest]
            index = smallest

    def pop(self) -> Any:
        """removes the root and assigns the last element as the new root, then sifts down until it is in the correct pos"""
        if len(self._tree) == 0:
            raise HeapError("cannot pop from empty heap")

        root = self._tree[0]
        last = self._tree.pop()

        if len(self._tree) == 0: return root[2]

        self._tree[0] = last
        self._sift_down(0)

        return root[2]

    def peek(self) -> Any:
        """returns the root object without removing it"""
        if len(self._tree) == 0:
            raise HeapError("cannot peek from empty heap")

        return self._tree[0][2]

    def ksmallest(self, k: int) -> List[Any]:
        """"""

    @classmethod
    def heapify(cls, items: List) -> "Heap":  
        """"""
        heap = cls()
        entries = []

        # verify input is valid
        if not isinstance(items, list): raise HeapError("Items must be a valid instance of List")
        for i, item in enumerate(items):
            if not isinstance(item, (tuple, list)) or len(item) != 2:
                raise HeapError(f"Invalid item pair at position {i}")
            entries.append((item[0], i, item[1]))

        heap._tree = entries
        for i in range(len(heap) // 2 - 1, -1, -1): # stop at -1 (include root 0) and decrease instead of increase
            heap._sift_down(i)

        heap._counter = len(heap._tree)

        return heap