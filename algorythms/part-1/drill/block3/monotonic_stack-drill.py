"""
ДРИЛЛ — MONOTONIC STACK

Пиши тела функций. Объяснений здесь нет специально — они в
monotonic_stack-ethalon.py, туда заглядывать ТОЛЬКО после запуска тестов.

Одна функция за сессию, 5 минут.
Ротация: 1) next_greater  2) daily_temperatures  3) largest_rectangle
         4) с начала.

Перед тем как писать, проговори вслух: ЧТО ЛЕЖИТ В СТЕКЕ И КОГДА ОНО УХОДИТ.
В третьей функции знак сравнения ДРУГОЙ, чем в первых двух — это не опечатка.

Не уложился или тест упал — пометь шаблон и поставь на завтра вне очереди,
но не досиживай.
"""


# =============================================================================
# next_greater — LeetCode 496
#
# Дан массив чисел. Вернуть массив той же длины, где на месте i стоит
# первое число СПРАВА от i, которое строго больше nums[i].
# Такого нет — -1.
#
#     [2, 1, 2, 4, 3]  -> [4, 2, 4, -1, -1]
#     [2, 2, 3]        -> [3, 3, -1]        (нужен СТРОГО больший)
# =============================================================================

def next_greater(nums):
    pass


# =============================================================================
# daily_temperatures — LeetCode 739
#
# Даны температуры по дням. Для каждого дня вернуть, сколько дней ждать
# до первого более тёплого. Такого дня нет — 0.
#
#     [73, 74, 75, 71, 69, 72, 76, 73]  ->  [1, 1, 4, 2, 1, 1, 0, 0]
#     [30, 30, 30]                      ->  [0, 0, 0]
# =============================================================================

def daily_temperatures(temps):
    pass


# =============================================================================
# largest_rectangle — LeetCode 84
#
# Дана гистограмма — массив высот столбиков ширины 1.
# Вернуть площадь самого большого прямоугольника, который в неё влезает.
#
#     [2, 1, 5, 6, 2, 3]  -> 10    (столбики 5 и 6: высота 5, ширина 2)
#     [2, 4]              -> 4
#     []                  -> 0
# =============================================================================

def largest_rectangle(heights):
    pass


# =============================================================================
# ТЕСТЫ
# =============================================================================

def test_next_greater():
    assert next_greater([2, 1, 2, 4, 3]) == [4, 2, 4, -1, -1]
    assert next_greater([1, 2, 3]) == [2, 3, -1]
    assert next_greater([3, 2, 1]) == [-1, -1, -1]
    assert next_greater([2, 2, 3]) == [3, 3, -1]
    assert next_greater([2, 2]) == [-1, -1]
    assert next_greater([5, 4, 3, 9]) == [9, 9, 9, -1]
    assert next_greater([]) == []
    assert next_greater([1]) == [-1]
    assert next_greater([-2, -1, -3]) == [-1, -1, -1]


def test_daily_temperatures():
    assert daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
    assert daily_temperatures([30, 40, 50, 60]) == [1, 1, 1, 0]
    assert daily_temperatures([30, 60, 90]) == [1, 1, 0]
    assert daily_temperatures([30, 30, 30]) == [0, 0, 0]
    assert daily_temperatures([90, 80, 70]) == [0, 0, 0]
    assert daily_temperatures([50, 40, 30, 20, 60]) == [4, 3, 2, 1, 0]
    assert daily_temperatures([]) == []
    assert daily_temperatures([50]) == [0]


def test_largest_rectangle():
    assert largest_rectangle([2, 1, 5, 6, 2, 3]) == 10
    assert largest_rectangle([2, 4]) == 4
    assert largest_rectangle([2, 1, 2]) == 3
    assert largest_rectangle([5, 4, 3, 2, 1]) == 9
    assert largest_rectangle([1, 2, 3, 4, 5]) == 9
    assert largest_rectangle([3, 3, 3]) == 9
    assert largest_rectangle([6, 7, 5, 2, 4, 5, 9, 3]) == 16
    assert largest_rectangle([1, 0, 1]) == 1
    assert largest_rectangle([]) == 0
    assert largest_rectangle([1]) == 1
    assert largest_rectangle([0]) == 0


# Закомментируй те, что сегодня не пишешь.
test_next_greater()
test_daily_temperatures()
test_largest_rectangle()
print("ok")
