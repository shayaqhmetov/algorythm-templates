"""
ДРИЛЛ — СОРТИРОВКА ПОДСЧЁТОМ И ПО КЛЮЧУ

Пиши тела функций. Объяснений здесь нет специально — они в
key_sort-ethalon.py, туда заглядывать ТОЛЬКО после запуска тестов.

Одна функция за сессию, 5 минут.
Ротация: 1) counting_sort  2) sort_by_freq  3) largest_number
         4) merge_intervals.

Перед тем как писать, проговори вслух: ЧТО ЗДЕСЬ ЗАДАЁТ ПОРЯДОК —
счётчик, ключ или правило на паре.

Не уложился или тест упал — пометь шаблон и поставь на завтра вне очереди,
но не досиживай.
"""

from functools import cmp_to_key


# =============================================================================
# counting_sort — сортировка подсчётом
#
# Дан список НЕОТРИЦАТЕЛЬНЫХ целых. Вернуть новый отсортированный список
# за O(n + k), где k — максимальное значение. Без sorted() и сравнений.
#
#     [3, 1, 0, 3, 1]  ->  [0, 1, 1, 3, 3]
#     []               ->  []
# =============================================================================

def counting_sort(nums):
    pass


# =============================================================================
# sort_by_freq — LeetCode 451
#
# Дана строка. Вернуть её же, сгруппировав символы по УБЫВАНИЮ частоты.
# Частоты равны — по ВОЗРАСТАНИЮ символа.
#
#     "tree"    ->  "eert"
#     "cccaaa"  ->  "aaaccc"
# =============================================================================

def sort_by_freq(s):
    pass


# =============================================================================
# largest_number — LeetCode 179
#
# Дан список неотрицательных чисел. Склеить их в таком порядке, чтобы
# получилось наибольшее число. Вернуть строку.
#
#     [10, 2]            ->  "210"
#     [3, 30, 34, 5, 9]  ->  "9534330"
#     [0, 0]             ->  "0"      (не "00")
# =============================================================================

def largest_number(nums):
    pass


# =============================================================================
# merge_intervals — LeetCode 56
#
# Дан список отрезков [начало, конец] в произвольном порядке.
# Слить все пересекающиеся. Касание концами — тоже пересечение.
# Ответ упорядочен по началу. Список intervals не менять.
#
#     [[1,3], [2,6], [8,10], [15,18]]  -> [[1,6], [8,10], [15,18]]
#     [[1,4], [4,5]]                   -> [[1,5]]
#     [[1,10], [2,3]]                  -> [[1,10]]
# =============================================================================

def merge_intervals(intervals):
    pass


# =============================================================================
# ТЕСТЫ
# =============================================================================

def test_counting_sort():
    assert counting_sort([3, 1, 0, 3, 1]) == [0, 1, 1, 3, 3]
    assert counting_sort([]) == []
    assert counting_sort([5]) == [5]
    assert counting_sort([0]) == [0]
    assert counting_sort([2, 2, 2]) == [2, 2, 2]
    assert counting_sort([5, 1, 3]) == [1, 3, 5]
    assert counting_sort([1, 2, 3]) == [1, 2, 3]
    assert counting_sort([3, 2, 1]) == [1, 2, 3]
    big = [(i * 37) % 101 for i in range(300)]
    assert counting_sort(big) == sorted(big)


def test_sort_by_freq():
    assert sort_by_freq("tree") == "eert"
    assert sort_by_freq("cccaaa") == "aaaccc"
    assert sort_by_freq("ab") == "ab"
    assert sort_by_freq("Aabb") == "bbAa"
    assert sort_by_freq("") == ""
    assert sort_by_freq("a") == "a"
    assert sorted(sort_by_freq("aabbbcc")) == sorted("aabbbcc")
    assert sort_by_freq("aabbbcc") == "bbbaacc"
    assert sort_by_freq("abab") == "aabb"


def test_largest_number():
    assert largest_number([10, 2]) == "210"
    assert largest_number([3, 30, 34, 5, 9]) == "9534330"
    assert largest_number([3, 30]) == "330"
    assert largest_number([3, 34]) == "343"
    assert largest_number([0, 0]) == "0"
    assert largest_number([0]) == "0"
    assert largest_number([0, 1]) == "10"
    assert largest_number([121, 12]) == "12121"
    assert largest_number([432, 43243]) == "43243432"
    assert largest_number([1]) == "1"
    assert largest_number([]) == ""
    assert largest_number([5, 5, 5]) == "555"


def test_merge_intervals():
    assert merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]) == [
        [1, 6], [8, 10], [15, 18]]
    assert merge_intervals([[1, 4], [4, 5]]) == [[1, 5]]
    assert merge_intervals([[1, 10], [2, 3]]) == [[1, 10]]
    assert merge_intervals([[8, 10], [1, 3], [2, 6]]) == [[1, 6], [8, 10]]
    assert merge_intervals([[1, 2], [2, 3], [3, 4]]) == [[1, 4]]
    assert merge_intervals([[1, 2], [3, 4]]) == [[1, 2], [3, 4]]
    assert merge_intervals([[1, 2], [1, 2]]) == [[1, 2]]
    assert merge_intervals([]) == []
    assert merge_intervals([[1, 2]]) == [[1, 2]]
    src = [[2, 6], [1, 3]]
    assert merge_intervals(src) == [[1, 6]]
    assert src == [[2, 6], [1, 3]]


# Закомментируй те, что сегодня не пишешь.
test_counting_sort()
test_sort_by_freq()
test_largest_number()
test_merge_intervals()
print("ok")
