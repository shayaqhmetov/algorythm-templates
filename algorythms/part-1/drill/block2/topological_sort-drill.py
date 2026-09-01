"""
ДРИЛЛ — TOPOLOGICAL SORT

Пиши тела функций. Объяснений здесь нет специально — они в
topological_sort-ethalon.py, туда заглядывать ТОЛЬКО после запуска тестов.

Одна функция за сессию, 5 минут.
Ротация: 1) topo_order  2) can_finish  3) с начала.

Перед тем как писать, проговори вслух: КУДА СМОТРИТ РЕБРО.
У двух функций ниже направление задано ПО-РАЗНОМУ — это не опечатка.

Не уложился или тест упал — пометь шаблон и поставь на завтра вне очереди,
но не досиживай.
"""

from collections import deque


# =============================================================================
# topo_order
#
# Дано: n вершин 0..n-1 и список ОРИЕНТИРОВАННЫХ рёбер.
#       Ребро [a, b] означает: a должен идти РАНЬШЕ b.
# Вернуть любой валидный топологический порядок (список всех n вершин).
# Если есть цикл — пустой список.
#
#     n = 4, edges = [[0,1], [0,2], [1,3], [2,3]]
#
#         0 -> 1
#         |    |
#         v    v
#         2 -> 3
#
#     -> [0, 1, 2, 3]   (валиден также [0, 2, 1, 3])
#
#     n = 2, edges = [[0,1], [1,0]]  -> []
# =============================================================================

def topo_order(n, edges):
    pass


# =============================================================================
# can_finish — LeetCode 207
#
# Дано: num_courses курсов 0..num_courses-1 и список пар prerequisites.
#       Пара [a, b] означает: чтобы взять курс a, надо СНАЧАЛА пройти b.
#       (направление обратное тому, что в topo_order выше)
# Вернуть True, если можно пройти все курсы; False, если есть цикл.
#
#     can_finish(2, [[1, 0]])          -> True
#     can_finish(2, [[1, 0], [0, 1]])  -> False
# =============================================================================

def can_finish(num_courses, prerequisites):
    pass


# =============================================================================
# ТЕСТЫ
# Валидных порядков обычно несколько, поэтому проверяется валидность,
# а не точный список. is_valid_order уже написан — его дриллить не надо.
# =============================================================================

def is_valid_order(n, edges, order):
    if sorted(order) != list(range(n)):
        return False
    pos = {v: i for i, v in enumerate(order)}
    return all(pos[a] < pos[b] for a, b in edges)


def test_topo_order():
    edges = [[0, 1], [0, 2], [1, 3], [2, 3]]
    assert is_valid_order(4, edges, topo_order(4, edges))
    assert topo_order(2, [[0, 1], [1, 0]]) == []
    assert topo_order(3, [[0, 1], [1, 2], [2, 0]]) == []
    assert topo_order(4, [[0, 1], [2, 3], [3, 2]]) == []
    assert sorted(topo_order(3, [])) == [0, 1, 2]
    res = topo_order(4, [[0, 1], [1, 2]])
    assert is_valid_order(4, [[0, 1], [1, 2]], res)
    assert topo_order(3, [[0, 1], [1, 2]]) == [0, 1, 2]
    assert topo_order(3, [[2, 1], [1, 0]]) == [2, 1, 0]
    e = [[0, 1], [0, 2], [1, 3], [2, 3], [3, 4]]
    assert is_valid_order(5, e, topo_order(5, e))
    assert topo_order(1, []) == [0]
    assert topo_order(0, []) == []
    assert topo_order(2, [[0, 0]]) == []


def test_can_finish():
    assert can_finish(2, [[1, 0]]) is True
    assert can_finish(2, [[1, 0], [0, 1]]) is False
    assert can_finish(3, []) is True
    assert can_finish(4, [[1, 0], [2, 1], [3, 2]]) is True
    assert can_finish(3, [[0, 1], [1, 2], [2, 0]]) is False
    assert can_finish(4, [[1, 0], [2, 0], [3, 1], [3, 2]]) is True
    assert can_finish(5, [[1, 0], [3, 4], [4, 3]]) is False
    assert can_finish(1, []) is True
    assert can_finish(1, [[0, 0]]) is False


# Закомментируй те, что сегодня не пишешь.
test_topo_order()
test_can_finish()
print("ok")
