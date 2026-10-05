"""
ДРИЛЛ — BACKTRACKING

Пиши тела функций. Объяснений здесь нет специально — они в
backtracking-ethalon.py, туда заглядывать ТОЛЬКО после запуска тестов.

Одна функция за сессию, 5 минут.
Ротация: 1) subsets  2) permutations  3) combination_sum
         4) generate_parentheses.

Перед тем как писать, проговори вслух: ЧТО ПЕРЕДАЁТСЯ В РЕКУРСИЮ —
i + 1, i или ничего. Это единственное, чем первые три задачи отличаются.
В четвёртой массива нет вовсе — в рекурсию идут два счётчика.
И не забудь, что в res кладётся КОПИЯ пути.

Не уложился или тест упал — пометь шаблон и поставь на завтра вне очереди,
но не досиживай.
"""


# =============================================================================
# subsets — LeetCode 78
#
# Дан массив РАЗЛИЧНЫХ чисел. Вернуть все подмножества, включая пустое
# и полное. Порядок ответов любой, всего их 2^n.
#
#     [1, 2, 3]  ->  [], [1], [2], [3], [1,2], [1,3], [2,3], [1,2,3]
#     []         ->  [[]]
# =============================================================================

def subsets(nums):
    pass


# =============================================================================
# permutations — LeetCode 46
#
# Дан массив РАЗЛИЧНЫХ чисел. Вернуть все перестановки.
# Порядок ответов любой, всего их n!.
# [2,1] и [1,2] — РАЗНЫЕ ответы.
#
#     [1, 2, 3]  ->  [1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]
# =============================================================================

def permutations(nums):
    pass


# =============================================================================
# combination_sum — LeetCode 39
#
# Дан массив РАЗЛИЧНЫХ ПОЛОЖИТЕЛЬНЫХ чисел и target.
# Вернуть все наборы с суммой target. Одно число можно брать сколько угодно
# раз. Наборы, отличающиеся только порядком, считаются одинаковыми.
#
#     [2, 3, 6, 7], target = 7  ->  [[2,2,3], [7]]
#     [2],          target = 1  ->  []
# =============================================================================

def combination_sum(candidates, target):
    pass


# =============================================================================
# generate_parentheses — LeetCode 22
#
# Дано число n. Вернуть все ПРАВИЛЬНЫЕ скобочные последовательности
# из n пар скобок — списком строк. Порядок ответов любой.
#
#     n = 1  ->  "()"
#     n = 2  ->  "(())", "()()"
#     n = 3  ->  "((()))", "(()())", "(())()", "()(())", "()()()"
#     n = 0  ->  [""]
# =============================================================================

def generate_parentheses(n):
    pass


# =============================================================================
# ТЕСТЫ
# Порядок ответов не фиксирован, поэтому сравниваем нормализованные списки.
# norm_sets и norm_seqs уже написаны — их дриллить не надо.
# =============================================================================

def norm_sets(res):
    """Порядок внутри набора не важен (подмножества, комбинации)."""
    return sorted(tuple(sorted(x)) for x in res)


def norm_seqs(res):
    """Порядок внутри последовательности важен (перестановки)."""
    return sorted(tuple(x) for x in res)


def test_subsets():
    assert norm_sets(subsets([1, 2, 3])) == norm_sets(
        [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]])
    assert len(subsets([1, 2, 3, 4])) == 16
    assert len(subsets([1, 2, 3, 4, 5])) == 32
    assert [] in subsets([1, 2])
    assert len({tuple(x) for x in subsets([1, 2, 3])}) == 8
    assert subsets([]) == [[]]
    assert norm_sets(subsets([7])) == norm_sets([[], [7]])
    assert norm_sets(subsets([0, -1])) == norm_sets([[], [0], [-1], [-1, 0]])


def test_permutations():
    assert norm_seqs(permutations([1, 2, 3])) == norm_seqs(
        [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]])
    assert len(permutations([1, 2, 3, 4])) == 24
    assert len(permutations([1, 2, 3, 4, 5])) == 120
    assert norm_seqs(permutations([1, 2])) == norm_seqs([[1, 2], [2, 1]])
    assert len({tuple(x) for x in permutations([1, 2, 3, 4])}) == 24
    assert all(sorted(p) == [1, 2, 3] for p in permutations([1, 2, 3]))
    assert permutations([]) == [[]]
    assert permutations([7]) == [[7]]


def test_combination_sum():
    assert norm_sets(combination_sum([2, 3, 6, 7], 7)) == norm_sets([[2, 2, 3], [7]])
    assert norm_sets(combination_sum([2, 3, 5], 8)) == norm_sets(
        [[2, 2, 2, 2], [2, 3, 3], [3, 5]])
    assert norm_sets(combination_sum([2], 6)) == norm_sets([[2, 2, 2]])
    assert combination_sum([2], 1) == []
    assert combination_sum([3, 5], 1) == []
    assert norm_sets(combination_sum([7], 7)) == norm_sets([[7]])
    assert len(combination_sum([2, 3], 5)) == 1
    assert combination_sum([2, 3], 0) == [[]]
    assert combination_sum([], 5) == []
    assert norm_sets(combination_sum([7, 2, 3], 7)) == norm_sets([[2, 2, 3], [7]])


def test_generate_parentheses():
    assert sorted(generate_parentheses(3)) == sorted(
        ["((()))", "(()())", "(())()", "()(())", "()()()"])
    assert sorted(generate_parentheses(2)) == ["(())", "()()"]
    assert generate_parentheses(1) == ["()"]
    assert generate_parentheses(0) == [""]
    assert ")(" not in generate_parentheses(1)
    assert "())(" not in generate_parentheses(2)
    assert all(len(s) == 8 for s in generate_parentheses(4))
    assert len(generate_parentheses(4)) == 14
    assert len(generate_parentheses(5)) == 42
    assert len(set(generate_parentheses(4))) == 14


# Закомментируй те, что сегодня не пишешь.
test_subsets()
test_permutations()
test_combination_sum()
test_generate_parentheses()
print("ok")
