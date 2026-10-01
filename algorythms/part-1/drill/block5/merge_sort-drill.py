"""
ДРИЛЛ — MERGE SORT

Пиши тела функций. Объяснений здесь нет специально — они в
merge_sort-ethalon.py, туда заглядывать ТОЛЬКО после запуска тестов.

Одна функция за сессию, 5 минут.
Ротация: 1) merge  2) merge_sort  3) count_inversions  4) с начала.
merge пишется каждый раз, на нём стоят обе остальные.

Перед тем как писать, проговори вслух: ПОЧЕМУ В merge ЗНАК <=, А НЕ <.

Не уложился или тест упал — пометь шаблон и поставь на завтра вне очереди,
но не досиживай.
"""


# =============================================================================
# merge — слияние двух отсортированных
#
# Даны два списка, каждый отсортирован по неубыванию.
# Вернуть один отсортированный список из всех элементов.
# Равные элементы: сначала из ЛЕВОГО списка.
#
#     [1, 4, 7], [2, 4, 5]  ->  [1, 2, 4, 4, 5, 7]
#     [], [1, 2]            ->  [1, 2]
# =============================================================================

def merge(a, b):
    pass


# =============================================================================
# merge_sort — LeetCode 912
#
# Дан список. Вернуть НОВЫЙ отсортированный список, исходный не менять.
#
#     [5, 2, 4, 1]  ->  [1, 2, 4, 5]
#     []            ->  []
# =============================================================================

def merge_sort(nums):
    pass


# =============================================================================
# count_inversions
#
# Дан список. Вернуть число инверсий — пар индексов i < j,
# где nums[i] > nums[j]. За O(n log n), а не перебором пар.
#
#     [2, 4, 1, 3, 5]  ->  3     (пары (2,1), (4,1), (4,3))
#     [5, 4, 3, 2, 1]  ->  10
# =============================================================================

def count_inversions(nums):
    pass


# =============================================================================
# ТЕСТЫ
# Item и tags уже написаны — их дриллить не надо, они нужны,
# чтобы было видно стабильность.
# =============================================================================

class Item:
    def __init__(self, key, tag):
        self.key, self.tag = key, tag

    def __lt__(self, other):
        return self.key < other.key

    def __le__(self, other):
        return self.key <= other.key

    def __repr__(self):
        return f"{self.key}{self.tag}"


def tags(items):
    return "".join(x.tag for x in items)


def test_merge():
    assert merge([1, 4, 7], [2, 4, 5]) == [1, 2, 4, 4, 5, 7]
    assert merge([], [1, 2]) == [1, 2]
    assert merge([1, 2], []) == [1, 2]
    assert merge([], []) == []
    assert merge([1], [2, 3, 4, 5]) == [1, 2, 3, 4, 5]
    assert merge([2, 3, 4, 5], [1]) == [1, 2, 3, 4, 5]
    assert merge([1, 2], [8, 9]) == [1, 2, 8, 9]
    assert merge([8, 9], [1, 2]) == [1, 2, 8, 9]
    assert merge([2, 2], [2, 2]) == [2, 2, 2, 2]
    assert merge([-5, -1], [-3, 0]) == [-5, -3, -1, 0]
    assert tags(merge([Item(1, "a"), Item(2, "b")], [Item(1, "c")])) == "acb"


def test_merge_sort():
    assert merge_sort([5, 2, 4, 1]) == [1, 2, 4, 5]
    assert merge_sort([]) == []
    assert merge_sort([7]) == [7]
    assert merge_sort([1, 2, 3]) == [1, 2, 3]
    assert merge_sort([3, 2, 1]) == [1, 2, 3]
    assert merge_sort([2, 2, 1, 2]) == [1, 2, 2, 2]
    assert merge_sort([0, -3, 5, -3]) == [-3, -3, 0, 5]
    src = [3, 1, 2]
    assert merge_sort(src) == [1, 2, 3]
    assert src == [3, 1, 2]
    big = [(i * 37) % 101 for i in range(300)]
    assert merge_sort(big) == sorted(big)
    items = [Item(2, "a"), Item(1, "b"), Item(2, "c"), Item(1, "d")]
    assert tags(merge_sort(items)) == "bdac"


def test_count_inversions():
    assert count_inversions([2, 4, 1, 3, 5]) == 3
    assert count_inversions([1, 2, 3]) == 0
    assert count_inversions([3, 2, 1]) == 3
    assert count_inversions([5, 4, 3, 2, 1]) == 10
    assert count_inversions([2, 2, 2]) == 0
    assert count_inversions([]) == 0
    assert count_inversions([1]) == 0
    assert count_inversions([3, 4, 5, 1]) == 3
    big = [(i * 37) % 101 for i in range(120)]
    naive = sum(1 for i in range(len(big)) for j in range(i + 1, len(big)) if big[i] > big[j])
    assert count_inversions(big) == naive


# Закомментируй те, что сегодня не пишешь.
test_merge()
test_merge_sort()
test_count_inversions()
print("ok")
