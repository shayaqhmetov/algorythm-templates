"""
ДРИЛЛ — ОБХОД ДЕРЕВА

Пиши тела функций. Объяснений здесь нет специально — они в
tree_traversal-ethalon.py, туда заглядывать ТОЛЬКО после запуска тестов.

Одна функция за сессию, 5 минут.
Ротация: 1) max_depth  2) level_order  3) inorder  4) is_valid_bst
         5) с начала.
TreeNode и build дриллить не надо, они уже написаны ниже.

Перед тем как писать, проговори вслух: ЧТО ИДЁТ СНИЗУ ВВЕРХ,
А ЧТО ТАЩИТСЯ СВЕРХУ ВНИЗ.

Не уложился или тест упал — пометь шаблон и поставь на завтра вне очереди,
но не досиживай.
"""

from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build(values):
    """Формат LeetCode: значения по уровням, None вместо отсутствующего узла."""
    if not values or values[0] is None:
        return None

    root = TreeNode(values[0])
    q = deque([root])
    i = 1

    while q and i < len(values):
        node = q.popleft()

        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            q.append(node.left)
        i += 1

        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            q.append(node.right)
        i += 1

    return root


# =============================================================================
# max_depth — LeetCode 104
#
# Вернуть число узлов на самом длинном пути от корня до листа.
# Пустое дерево — 0.
#
#         3
#        / \
#       9  20
#          / \
#         15  7      -> 3
# =============================================================================

def max_depth(root):
    pass


# =============================================================================
# level_order — LeetCode 102
#
# Вернуть список уровней: [[корень], [второй уровень], ...].
# Пустое дерево — пустой список.
#
#         3
#        / \
#       9  20
#          / \
#         15  7      -> [[3], [9, 20], [15, 7]]
# =============================================================================

def level_order(root):
    pass


# =============================================================================
# inorder — LeetCode 94
#
# Вернуть значения в порядке "левое поддерево, узел, правое поддерево".
# БЕЗ РЕКУРСИИ — стеком.
#
#         1
#          \
#           2
#          /
#         3          -> [1, 3, 2]
# =============================================================================

def inorder(root):
    pass


# =============================================================================
# is_valid_bst — LeetCode 98
#
# Проверить, что дерево — корректное BST: в ЛЕВОМ поддереве узла ВСЕ
# значения строго меньше, в ПРАВОМ — строго больше. Дубликаты запрещены.
#
#         5
#        / \
#       1   4        -> False
#          / \
#         3   6
#
# (4 и 3 лежат в правом поддереве пятёрки, но меньше пяти)
# =============================================================================

def is_valid_bst(root):
    pass


# =============================================================================
# ТЕСТЫ
# =============================================================================

def test_max_depth():
    assert max_depth(build([3, 9, 20, None, None, 15, 7])) == 3
    assert max_depth(None) == 0
    assert max_depth(build([])) == 0
    assert max_depth(build([1])) == 1
    assert max_depth(build([1, None, 2, None, 3])) == 3
    assert max_depth(build([0, 0, 0])) == 2
    assert max_depth(build([1, 2, None, 3])) == 3


def test_level_order():
    assert level_order(build([3, 9, 20, None, None, 15, 7])) == [[3], [9, 20], [15, 7]]
    assert level_order(None) == []
    assert level_order(build([])) == []
    assert level_order(build([1])) == [[1]]
    assert level_order(build([1, 2, 3, None, 5, None, 7])) == [[1], [2, 3], [5, 7]]
    assert level_order(build([1, None, 2, None, 3])) == [[1], [2], [3]]
    assert level_order(build([0, -1, 1])) == [[0], [-1, 1]]


def test_inorder():
    assert inorder(build([1, None, 2, 3])) == [1, 3, 2]
    assert inorder(None) == []
    assert inorder(build([1])) == [1]
    assert inorder(build([4, 2, 6, 1, 3, 5, 7])) == [1, 2, 3, 4, 5, 6, 7]
    assert inorder(build([3, 2, None, 1])) == [1, 2, 3]
    assert inorder(build([1, None, 2, None, 3])) == [1, 2, 3]
    assert inorder(build([1, 2, 3])) == [2, 1, 3]


def test_is_valid_bst():
    assert is_valid_bst(build([2, 1, 3])) is True
    assert is_valid_bst(build([5, 1, 4, None, None, 3, 6])) is False
    assert is_valid_bst(build([10, 5, 15, None, None, 6, 20])) is False
    assert is_valid_bst(build([2, 2, None])) is False
    assert is_valid_bst(build([2, None, 2])) is False
    assert is_valid_bst(None) is True
    assert is_valid_bst(build([1])) is True
    assert is_valid_bst(build([4, 2, 6, 1, 3, 5, 7])) is True
    assert is_valid_bst(build([0, -1, 1])) is True
    assert is_valid_bst(build([1, None, 2, None, 3])) is True


# Закомментируй те, что сегодня не пишешь.
test_max_depth()
test_level_order()
test_inorder()
test_is_valid_bst()
print("ok")
