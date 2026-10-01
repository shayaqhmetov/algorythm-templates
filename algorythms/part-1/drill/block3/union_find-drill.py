"""
ДРИЛЛ — UNION-FIND (DSU)

Пиши тела функций. Объяснений здесь нет специально — они в
union_find-ethalon.py, туда заглядывать ТОЛЬКО после запуска тестов.

Одна функция за сессию, 5 минут.
Ротация: 1) DSU  2) count_components  3) find_redundant_connection
         4) с начала.
DSU пишется каждый раз, на нём стоят обе остальные.

Перед тем как писать, проговори вслух: ЧТО ЗНАЧИТ False ОТ union.

Не уложился или тест упал — пометь шаблон и поставь на завтра вне очереди,
но не досиживай.
"""


# =============================================================================
# DSU — сама структура
#
# n элементов 0..n-1, изначально каждый сам по себе.
# Поля: parent, size, count (сколько групп сейчас).
# Методы:
#     find(x)     -> корень группы x
#     union(a, b) -> True, если слили две РАЗНЫЕ группы
#                    False, если они уже были одной (count не меняется)
#
#     d = DSU(5)
#     d.union(0, 1)  -> True,  count = 4
#     d.union(1, 0)  -> False, count = 4
#     d.find(0) == d.find(1)
#
# find — циклом, а не рекурсией. Сжатие пути и объединение по размеру
# обязательны: без них find вырождается в проход по цепочке.
# =============================================================================

class DSU:
    def __init__(self, n):
        pass

    def find(self, x):
        pass

    def union(self, a, b):
        pass


# =============================================================================
# count_components — LeetCode 323
#
# Дано: n вершин 0..n-1 и список НЕОРИЕНТИРОВАННЫХ рёбер.
# Вернуть число связных компонент.
#
#     n = 5, edges = [[0,1], [1,2], [3,4]]
#
#         0 - 1 - 2      3 - 4
#
#     -> 2
#
#     n = 5, edges = []  -> 5   (изолированные вершины тоже компоненты)
# =============================================================================

def count_components(n, edges):
    pass


# =============================================================================
# find_redundant_connection — LeetCode 684
#
# Дано: дерево из n вершин (нумерация С ЕДИНИЦЫ), в которое добавили одно
#       лишнее ребро. Рёбра даны в порядке добавления.
# Вернуть ребро, которое можно убрать, чтобы снова стало дерево. Подходит
# любое ребро цикла — вернуть то из них, которое в списке ПОСЛЕДНЕЕ.
# Лишнего ребра нет — вернуть [].
#
#     [[1,2], [1,3], [2,3]]  -> [2,3]
#
#         1 - 2
#         |  /
#         3
#
#     [[1,4], [3,4], [1,3], [1,2], [4,5]]  -> [1,3]
#     последнее ребро цикла 1-4-3-1, а не последнее ребро списка
# =============================================================================

def find_redundant_connection(edges):
    pass


# =============================================================================
# ТЕСТЫ
# =============================================================================

def test_dsu():
    d = DSU(5)
    assert d.find(3) == 3
    assert d.count == 5
    assert d.union(0, 1) is True
    assert d.find(0) == d.find(1)
    assert d.count == 4
    assert d.union(1, 0) is False
    assert d.count == 4
    d.union(2, 3)
    assert d.union(0, 2) is True
    assert d.count == 2
    assert d.find(1) == d.find(3)
    assert d.find(4) != d.find(0)
    d.union(3, 4)
    assert d.count == 1
    assert len({d.find(i) for i in range(5)}) == 1
    one = DSU(1)
    assert one.find(0) == 0
    assert one.count == 1
    chain = DSU(50)
    for i in range(49):
        assert chain.union(i, i + 1) is True
    assert chain.count == 1
    assert chain.find(0) == chain.find(49)


def test_count_components():
    assert count_components(5, [[0, 1], [1, 2], [3, 4]]) == 2
    assert count_components(5, []) == 5
    assert count_components(4, [[0, 1]]) == 3
    assert count_components(4, [[0, 1], [1, 2], [2, 3]]) == 1
    assert count_components(3, [[0, 1], [1, 0], [0, 1]]) == 2
    assert count_components(3, [[0, 1], [1, 2], [2, 0]]) == 1
    assert count_components(0, []) == 0
    assert count_components(1, []) == 1
    assert count_components(5, [[0, 1], [0, 2], [0, 3], [0, 4]]) == 1


def test_find_redundant_connection():
    assert find_redundant_connection([[1, 2], [1, 3], [2, 3]]) == [2, 3]
    assert find_redundant_connection([[1, 2], [2, 3], [3, 4], [1, 4]]) == [1, 4]
    assert find_redundant_connection([[1, 2], [2, 1], [2, 3]]) == [2, 1]
    assert find_redundant_connection([[1, 2], [1, 3], [1, 4], [3, 4]]) == [3, 4]
    assert find_redundant_connection([[1, 2], [1, 2]]) == [1, 2]
    assert find_redundant_connection([[1, 2], [2, 3]]) == []
    assert find_redundant_connection([]) == []
    assert find_redundant_connection(
        [[1, 4], [3, 4], [1, 3], [1, 2], [4, 5]]) == [1, 3]


# Закомментируй те, что сегодня не пишешь.
test_dsu()
test_count_components()
test_find_redundant_connection()
print("ok")
