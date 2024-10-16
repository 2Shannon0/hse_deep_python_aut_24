# pylint: disable=too-few-public-methods
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, limit=42):
        self.limit = limit
        self.cache = {}
        self.head = None
        self.last = None
        self.size = 0

    def get(self, key):
        if key not in self.cache:
            return None
        node = self.cache[key]
        self._remove_node(node)
        self._update_head(node)

        return node.value

    def set(self, key, value):
        if self.limit == 0:
            return
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._remove_node(node)
            self._update_head(node)
        else:
            new_node = Node(key, value)
            if self.size == self.limit:
                del self.cache[self.last.key]
                self._remove_node(self.last)
                self.size -= 1

            self._update_head(new_node)
            self.cache[key] = new_node
            self.size += 1

    def _remove_node(self, node):
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next

        if node.next:
            node.next.prev = node.prev
        else:
            self.last = node.prev

        node.prev = node.next = None

    def _update_head(self, node):
        node.next = self.head
        node.prev = None
        if self.head:
            self.head.prev = node
        self.head = node

        if self.last is None:
            self.last = node

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)
