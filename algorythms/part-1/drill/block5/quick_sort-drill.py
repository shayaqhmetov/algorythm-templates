"""
ДРИЛЛ — QUICK SORT И QUICKSELECT

Пиши тела функций. Объяснений здесь нет специально — они в
quick_sort-ethalon.py, туда заглядывать ТОЛЬКО после запуска тестов.

Одна функция за сессию, 5 минут.
Ротация: 1) partition  2) quick_sort  3) quick_select  4) с начала.
partition пишется каждый раз, на нём стоят обе остальные.

Перед тем как писать, проговори вслух: ЧТО ВОЗВРАЩАЕТ partition
И ПОЧЕМУ В РЕКУРСИЮ ИДУТ [lo, p - 1] и [p + 1, hi].

Не уложился или тест упал — пометь шаблон и поставь на завтра вне очереди,
но не досиживай.
"""

import random


# =============================================================================
# partition — схема Ломуто
#
# Дан список и границы lo, hi (обе включительно). Пивот — ПОСЛЕДНИЙ элемент
# отрезка. Переставить nums[lo..hi] на месте так, чтобы слева от пивота были
# строго меньшие, справа — не меньшие. Вернуть индекс пивота.
#
#     [3, 7, 8, 5, 2, 1, 9, 5], lo=0, hi=7  ->  3
#     массив стал [3, 2, 1, 5, 7, 8, 9, 5]
# =============================================================================

def partition(nums, lo, hi):
    pass


# =============================================================================
# quick_sort — LeetCode 912
#
# Отсортировать список НА МЕСТЕ, без нового списка, и вернуть его же.
# Пивот брать случайный, иначе отсортированный вход даёт O(n^2).
#
#     [5, 2, 4, 1]  ->  [1, 2, 4, 5]
# =============================================================================

def quick_sort(nums):
    pass


# =============================================================================
# quick_select — LeetCode 215
#
# Дан список и k (нумерация С ЕДИНИЦЫ). Вернуть k-й элемент в порядке
# неубывания, не сортируя весь список. k вне диапазона — None.
# Исходный список не менять.
#
#     [3, 2, 1, 5, 6, 4], k = 2  ->  2
#     [1, 2, 3], k = 4           ->  None
# =============================================================================

def quick_select(nums, k):
    pass


# =============================================================================
# ТЕСТЫ
# check_partition уже написан — его дриллить не надо.
# =============================================================================

def check_partition(nums):
    p = partition(nums, 0, len(nums) - 1)
    pivot = nums[p]
    return (all(x < pivot for x in nums[:p]) and
            all(x >= pivot for x in nums[p + 1:]))


def test_partition():
    a = [3, 7, 8, 5, 2, 1, 9, 5]
    assert partition(a, 0, 7) == 3
    assert a[3] == 5
    assert check_partition([3, 7, 8, 5, 2, 1, 9, 5])
    a = [1, 2, 3]
    assert partition(a, 0, 2) == 2
    assert a == [1, 2, 3]
    a = [3, 2, 1]
    assert partition(a, 0, 2) == 0
    assert a[0] == 1
    a = [4, 4, 4, 4]
    assert partition(a, 0, 3) == 0
    a = [9, 3, 1, 2, 9]
    assert partition(a, 1, 3) == 2
    assert a == [9, 1, 2, 3, 9]
    a = [5]
    assert partition(a, 0, 0) == 0
    assert check_partition([2, 1])
    assert check_partition([1, 2])
    assert check_partition([5, 1, 4, 2, 3])
    assert check_partition([-3, 0, -7, 2])


def test_quick_sort():
    assert quick_sort([5, 2, 4, 1]) == [1, 2, 4, 5]
    assert quick_sort([]) == []
    assert quick_sort([7]) == [7]
    assert quick_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]
    assert quick_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]
    assert quick_sort([2, 2, 2, 2, 2]) == [2, 2, 2, 2, 2]
    assert quick_sort([3, 1, 3, 1, 3]) == [1, 1, 3, 3, 3]
    assert quick_sort([0, -3, 5, -3]) == [-3, -3, 0, 5]
    src = [3, 1, 2]
    assert quick_sort(src) is src
    assert src == [1, 2, 3]
    big = [(i * 37) % 101 for i in range(300)]
    assert quick_sort(big[:]) == sorted(big)
    assert quick_sort(sorted(big)) == sorted(big)


def test_quick_select():
    assert quick_select([3, 2, 1, 5, 6, 4], 2) == 2
    assert quick_select([3, 2, 1, 5, 6, 4], 1) == 1
    assert quick_select([3, 2, 1, 5, 6, 4], 6) == 6
    assert quick_select([3, 3, 3], 2) == 3
    assert quick_select([1, 2, 2, 3], 3) == 2
    assert quick_select([1, 2, 3], 0) is None
    assert quick_select([1, 2, 3], 4) is None
    assert quick_select([], 1) is None
    assert quick_select([42], 1) == 42
    src = [3, 1, 2]
    assert quick_select(src, 1) == 1
    assert src == [3, 1, 2]
    big = [(i * 37) % 101 for i in range(200)]
    ordered = sorted(big)
    assert all(quick_select(big, k) == ordered[k - 1] for k in range(1, 201))


# Закомментируй те, что сегодня не пишешь.
test_partition()
test_quick_sort()
test_quick_select()
print("ok")
