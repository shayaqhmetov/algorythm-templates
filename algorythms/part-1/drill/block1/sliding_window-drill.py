"""
ДРИЛЛ — SLIDING WINDOW

Пиши тела функций. Объяснений здесь нет специально — они в
sliding_window-ethalon.py, туда заглядывать ТОЛЬКО после запуска тестов.

Одна функция за сессию, 5 минут.
Ротация: 1) longest_ones  2) longest_unique  3) shortest_sum  4) с начала.

Перед тем как писать, проговори вслух: ЗАМЕР ДО ИЛИ ПОСЛЕ while.
У третьей функции он стоит НЕ ТАМ, где у первых двух — это не опечатка.

Не уложился или тест упал — пометь шаблон и поставь на завтра вне очереди,
но не досиживай.
"""


# =============================================================================
# longest_ones — LeetCode 1004
#
# Массив из 0 и 1. Можно перевернуть максимум k нулей в единицы.
# Найти длину самой длинной цепочки единиц, которая получится.
#
#     [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], k = 2  -> 6
#     [0, 0, 0], k = 0                          -> 0
# =============================================================================

def longest_ones(nums, k):
    pass


# =============================================================================
# longest_unique — LeetCode 3
#
# Дана строка s. Вернуть длину самой длинной подстроки
# без повторяющихся символов.
#
#     "abcabcbb"  -> 3    ("abc")
#     "bbbbb"     -> 1
#     ""          -> 0
# =============================================================================

def longest_unique(s):
    pass


# =============================================================================
# shortest_sum — LeetCode 209
#
# Массив ПОЛОЖИТЕЛЬНЫХ чисел и число target.
# Вернуть длину самого КОРОТКОГО окна с суммой >= target.
# Такого окна нет — вернуть 0.
#
#     [2, 3, 1, 2, 4, 3], target = 7  -> 2    (окно [4, 3])
#     [1, 1, 1], target = 7           -> 0
# =============================================================================

def shortest_sum(nums, target):
    pass


# =============================================================================
# ТЕСТЫ
# =============================================================================

def test_longest_ones():
    assert longest_ones([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2) == 6
    assert longest_ones([0, 0, 0], 0) == 0
    assert longest_ones([1, 0, 1, 1, 0, 1], 0) == 2
    assert longest_ones([0, 0, 1, 1], 5) == 4
    assert longest_ones([1, 1, 1], 1) == 3
    assert longest_ones([], 3) == 0
    assert longest_ones([0], 0) == 0
    assert longest_ones([0], 1) == 1
    assert longest_ones([1, 1, 0, 1, 1, 0, 0, 0, 1], 1) == 5


def test_longest_unique():
    assert longest_unique("abcabcbb") == 3
    assert longest_unique("") == 0
    assert longest_unique("bbbbb") == 1
    assert longest_unique("pwwkew") == 3
    assert longest_unique("abba") == 2
    assert longest_unique("abcdef") == 6
    assert longest_unique("a") == 1
    assert longest_unique("abcdeab") == 5


def test_shortest_sum():
    assert shortest_sum([2, 3, 1, 2, 4, 3], 7) == 2
    assert shortest_sum([1, 1, 1], 7) == 0
    assert shortest_sum([1, 4, 4], 4) == 1
    assert shortest_sum([8], 7) == 1
    assert shortest_sum([1, 2, 3], 6) == 3
    assert shortest_sum([1, 1, 9, 1, 1, 1], 9) == 1
    assert shortest_sum([], 1) == 0
    assert shortest_sum([1], 2) == 0


# Закомментируй те, что сегодня не пишешь.
test_longest_ones()
test_longest_unique()
test_shortest_sum()
print("ok")
