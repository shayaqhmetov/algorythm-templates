"""
ДРИЛЛ — СТРУКТУРЫ ПОД ЗАКАЗ

Пиши тела методов. Объяснений здесь нет специально — они в
structures-ethalon.py, туда заглядывать ТОЛЬКО после запуска тестов.

Один класс за сессию, 5 минут.
Ротация: 1) MinStack  2) LRUCache  3) Trie  4) с начала.

Перед тем как писать, проговори вслух: ЧТО ХРАНИМ ВНУТРИ.
Здесь всё решается выбором представления, а не алгоритмом.

Не уложился или тест упал — пометь шаблон и поставь на завтра вне очереди,
но не досиживай.
"""

from collections import OrderedDict


# =============================================================================
# MinStack — LeetCode 155
#
# Стек, у которого все четыре операции за O(1):
#     push(x)    положить
#     pop()      снять и вернуть верхний
#     top()      посмотреть верхний
#     get_min()  минимум среди всех, что сейчас в стеке
# На пустом стеке pop, top и get_min возвращают None.
#
#     push(-2) push(0) push(-3)
#     get_min() -> -3 ; pop() -> -3 ; top() -> 0 ; get_min() -> -2
# =============================================================================

class MinStack:
    def __init__(self):
        pass

    def push(self, x):
        pass

    def pop(self):
        pass

    def top(self):
        pass

    def get_min(self):
        pass


# =============================================================================
# LRUCache — LeetCode 146
#
# Кэш на capacity элементов, обе операции за O(1):
#     get(key)         значение или -1, если ключа нет
#     put(key, value)  положить; места нет — выселить тот ключ,
#                      к которому дольше всего не обращались
# Обращение — это И get, И put.
#
#     c = LRUCache(2); put(1,1); put(2,2); get(1) -> 1
#     put(3,3) выселяет 2, потому что к 1 только что обращались
# =============================================================================

class LRUCache:
    def __init__(self, capacity):
        pass

    def get(self, key):
        pass

    def put(self, key, value):
        pass


# =============================================================================
# Trie — LeetCode 208
#
# Префиксное дерево:
#     insert(word)         добавить слово
#     search(word)         True, если такое СЛОВО добавляли
#     starts_with(prefix)  True, если есть слово с таким префиксом
#
#     insert("apple"); search("apple") -> True
#     search("app") -> False ; starts_with("app") -> True
# =============================================================================

class Trie:
    def __init__(self):
        pass

    def insert(self, word):
        pass

    def search(self, word):
        pass

    def starts_with(self, prefix):
        pass


# =============================================================================
# ТЕСТЫ
# =============================================================================

def test_minstack():
    s = MinStack()
    assert s.pop() is None and s.top() is None and s.get_min() is None
    s.push(-2)
    s.push(0)
    s.push(-3)
    assert s.get_min() == -3
    assert s.pop() == -3
    assert s.top() == 0
    assert s.get_min() == -2
    s = MinStack()
    s.push(1)
    s.push(1)
    s.push(2)
    assert s.get_min() == 1
    s.pop()
    s.pop()
    assert s.get_min() == 1
    s = MinStack()
    for x in [3, 4, 5]:
        s.push(x)
    assert s.get_min() == 3 and s.top() == 5
    s = MinStack()
    for x in [5, 4, 3]:
        s.push(x)
    assert s.get_min() == 3
    s.pop()
    assert s.get_min() == 4
    s = MinStack()
    s.push(7)
    assert s.pop() == 7
    assert s.get_min() is None
    s.push(9)
    assert s.get_min() == 9


def test_lrucache():
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == 1
    c.put(3, 3)
    assert c.get(2) == -1
    assert c.get(1) == 1 and c.get(3) == 3
    assert c.get(42) == -1
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    c.put(1, 10)
    c.put(3, 3)
    assert c.get(1) == 10
    assert c.get(2) == -1
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    c.put(2, 22)
    c.put(3, 3)
    assert c.get(1) == -1 and c.get(2) == 22 and c.get(3) == 3
    c = LRUCache(1)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == -1 and c.get(2) == 2
    c = LRUCache(0)
    c.put(1, 1)
    assert c.get(1) == -1
    c = LRUCache(3)
    for k in range(10):
        c.put(k, k * k)
    assert [c.get(k) for k in range(10)] == [-1] * 7 + [49, 64, 81]


def test_trie():
    t = Trie()
    t.insert("apple")
    assert t.search("apple") is True
    assert t.search("app") is False
    assert t.starts_with("app") is True
    t.insert("app")
    assert t.search("app") is True
    empty = Trie()
    assert empty.search("a") is False
    assert empty.starts_with("a") is False
    assert empty.starts_with("") is True
    assert empty.search("") is False
    empty.insert("")
    assert empty.search("") is True
    t = Trie()
    t.insert("app")
    assert t.search("apple") is False
    assert t.starts_with("apple") is False
    t = Trie()
    for w in ["car", "card", "care", "cat"]:
        t.insert(w)
    assert all(t.search(w) for w in ["car", "card", "care", "cat"])
    assert t.search("ca") is False
    assert t.starts_with("car") is True
    assert t.starts_with("cab") is False
    t.insert("car")
    assert t.search("car") is True and t.search("card") is True


# Закомментируй те, что сегодня не пишешь.
test_minstack()
test_lrucache()
test_trie()
print("ok")
