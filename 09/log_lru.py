# pylint: disable=too-few-public-methods
import logging
import argparse


# (повторяющиеся строки из дз по LRUCache"
# pylint: disable=R0801
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, limit=42):
        if limit < 0:
            # pylint: enable=R0801
            logging.error(
                "INIT: Попытка создания LRUCaсhe с отрицательным лимитом: '%s'",
                limit
            )
            raise ValueError('Лимит не может быть отрицательным.')
        self.limit = limit or 0
        self.cache = {}
        self.head = None
        self.last = None

        logging.debug("INIT: Создан LRUCaсhe объект с лимитом: '%s'", limit)

    def get(self, key):
        if key not in self.cache:
            logging.warning("GET: Ключ '%s' отсутствует в кэше.", key)
            return None
        node = self.cache[key]
        self._remove_node(node)
        self._update_head(node)
        logging.info("GET: Ключ '%s' найден, значение '%s'.", key, node.value)
        return node.value

    def set(self, key, value):
        if self.limit == 0:
            logging.debug("SET: Кэш имеет нулевой лимит, операция пропущена.")
            return
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._remove_node(node)
            self._update_head(node)
            logging.info(
                "SET: Ключ '%s' обновлён. Новое значение '%s'.", key, node.value
                )
        else:
            new_node = Node(key, value)
            if len(self.cache) == self.limit:
                logging.warning(
                    "SET: Переполнение кэша. Удалён ключ '%s'.", self.last.key
                    )
                del self.cache[self.last.key]
                self._remove_node(self.last)

            self._update_head(new_node)
            self.cache[key] = new_node
            logging.info(
                "SET: Новый ключ '%s' добавлен со значением '%s'.", key, value
                )

    def _remove_node(self, node):
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
            logging.debug(
                "Новая голова списка:  ключ-'%s', значение-'%s'.",
                node.next.key, node.next.value
                )

        if node.next:
            node.next.prev = node.prev
        else:
            self.last = node.prev
            logging.debug(
                "Новый конец списка:  ключ-'%s', значение-'%s'.",
                node.prev.key, node.prev.value
                )
        node.prev = node.next = None

    def _update_head(self, node):
        node.next = self.head
        node.prev = None
        if self.head:
            self.head.prev = node
        self.head = node
        logging.debug(
                "Новая голова списка:  ключ-'%s', значение-'%s'.",
                node.key, node.value
                )
        if self.last is None:
            self.last = node
            logging.debug(
                "Новый конец списка:  ключ-'%s', значение-'%s'.",
                node.key, node.value
                )

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)


def setup_logger(stdout, add_filter):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler("cache.log", encoding="utf-8")
    # можем задать уровень для конкретного хендлера
    # file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter(
            '%(asctime)s\t%(levelname)s\t%(message)s'
            )
        )
    logger.addHandler(file_handler)

    if stdout:
        stream_handler = logging.StreamHandler()
        # stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(
            logging.Formatter(
                "STDOUT %(asctime)s ~ %(levelname)s ~ %(message)s"
                )
            )
        logger.addHandler(stream_handler)

    if add_filter:
        class NoDEBUGFilter(logging.Filter):
            def filter(self, record):
                return record.levelname != "DEBUG"
        logger.addFilter(NoDEBUGFilter())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", action="store_true")
    parser.add_argument("-f", action="store_true")
    args = parser.parse_args()

    setup_logger(stdout=args.s, add_filter=args.f)

    cache1 = LRUCache(limit=3)
    cache1.set("a", 1)
    cache1.set("b", 2)
    cache1.set("c", 3)
    cache1.set("d", 4)
    cache1.get("b")
    cache1.get("a")
    cache1.set("b", 22)

    cache2 = LRUCache(0)
    cache2.get('key')
    cache2.set('key', 'value')

    LRUCache(-5)


if __name__ == "__main__":
    main()
