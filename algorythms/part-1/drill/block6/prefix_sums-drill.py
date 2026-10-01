"""
ДРИЛЛ — ПРЕФИКСНЫЕ СУММЫ

Пиши тела функций. Объяснений здесь нет специально — они в
prefix_sums-ethalon.py, туда заглядывать ТОЛЬКО после запуска тестов.

Одна функция за сессию, 5 минут.
Ротация: 1) prefix_sums  2) subarray_sum_k  3) product_except_self
         4) с начала.

Перед тем как писать, проговори вслух: ПОЧЕМУ ЗДЕСЬ НЕ ОКНО.
Ответ короткий — отрицательные числа.

Не уложился или тест упал — пометь шаблон и поставь на завтра вне очереди,
но не досиживай.
"""


# =============================================================================
# prefix_sums — LeetCode 303
#
# Дан список чисел. Вернуть массив префиксных сумм ДЛИНЫ n + 1,
# где p[i] — сумма первых i элементов, p[0] = 0.
# Тогда сумма nums[l..r] = p[r + 1] - p[l].
#
#     [2, 4, 1, 3]  ->  [0, 2, 6, 7, 10]
#     []            ->  [0]
# =============================================================================

def prefix_sums(nums):
    pass


# =============================================================================
# subarray_sum_k — LeetCode 560
#
# Дан список целых (могут быть отрицательные) и число k.
# Вернуть, сколько НЕПРЕРЫВНЫХ подмассивов имеют сумму ровно k.
# Пересекающиеся тоже считаются.
#
#     [1, 1, 1], k = 2   ->  2
#     [1, -1, 0], k = 0  ->  3
# =============================================================================

def subarray_sum_k(nums, k):
    pass


# =============================================================================
# product_except_self — LeetCode 238
#
# Дан список чисел. Вернуть массив, где на месте i стоит произведение всех
# элементов, кроме nums[i]. БЕЗ деления, за O(n).
#
#     [1, 2, 3, 4]        ->  [24, 12, 8, 6]
#     [-1, 1, 0, -3, 3]   ->  [0, 0, 9, 0, 0]
# =============================================================================

def product_except_self(nums):
    pass


# =============================================================================
# ТЕСТЫ
# =============================================================================

def test_prefix_sums():
    assert prefix_sums([2, 4, 1, 3]) == [0, 2, 6, 7, 10]
    assert prefix_sums([]) == [0]
    assert prefix_sums([5]) == [0, 5]
    nums = [2, 4, 1, 3]
    p = prefix_sums(nums)
    assert p[3] - p[1] == 5
    assert p[1] - p[0] == 2
    assert p[len(nums)] - p[0] == sum(nums)
    assert prefix_sums([-1, 1, -1]) == [0, -1, 0, -1]
    assert prefix_sums([0, 0]) == [0, 0, 0]
    big = [(i * 7) % 13 - 6 for i in range(200)]
    p = prefix_sums(big)
    assert all(p[i] == sum(big[:i]) for i in range(0, 201, 25))


def test_subarray_sum_k():
    assert subarray_sum_k([1, 1, 1], 2) == 2
    assert subarray_sum_k([1, 2, 3], 3) == 2
    assert subarray_sum_k([1, 2], 1) == 1
    assert subarray_sum_k([3], 3) == 1
    assert subarray_sum_k([1, -1, 0], 0) == 3
    assert subarray_sum_k([-1, -1, 1], 0) == 1
    assert subarray_sum_k([0, 0, 0], 0) == 6
    assert subarray_sum_k([1, 0, 1], 1) == 4
    assert subarray_sum_k([1, 2, 3], 100) == 0
    assert subarray_sum_k([], 0) == 0
    big = [(i * 7) % 5 - 2 for i in range(60)]
    naive = sum(1 for i in range(len(big)) for j in range(i, len(big))
                if sum(big[i:j + 1]) == 2)
    assert subarray_sum_k(big, 2) == naive


def test_product_except_self():
    assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]
    assert product_except_self([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]
    assert product_except_self([0, 0, 3]) == [0, 0, 0]
    assert product_except_self([]) == []
    assert product_except_self([5]) == [1]
    assert product_except_self([2, 3]) == [3, 2]
    assert product_except_self([-1, -2, -3]) == [6, 3, 2]
    assert product_except_self([1, 1, 1]) == [1, 1, 1]
    big = [(i % 5) - 2 or 3 for i in range(12)]
    naive = [
        [1 if j == i else big[j] for j in range(len(big))]
        for i in range(len(big))
    ]
    expected = []
    for row in naive:
        acc = 1
        for v in row:
            acc *= v
        expected.append(acc)
    assert product_except_self(big) == expected


# Закомментируй те, что сегодня не пишешь.
test_prefix_sums()
test_subarray_sum_k()
test_product_except_self()
print("ok")
