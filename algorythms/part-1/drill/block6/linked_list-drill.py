"""
ДРИЛЛ — СВЯЗНЫЙ СПИСОК

Пиши тела функций. Объяснений здесь нет специально — они в
linked_list-ethalon.py, туда заглядывать ТОЛЬКО после запуска тестов.

Одна функция за сессию, 5 минут.
Ротация: 1) reverse_list  2) merge_two_lists  3) detect_cycle  4) с начала.
ListNode и сборщики списков дриллить не надо, они уже написаны.

Перед тем как писать, проговори вслух: ЧТО ВЕРНУТЬ В КОНЦЕ.
После разворота это не head, а после слияния — не dummy.

Не уложился или тест упал — пометь шаблон и поставь на завтра вне очереди,
но не досиживай.
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build_list(values):
    dummy = ListNode()
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def node_at(head, i):
    for _ in range(i):
        head = head.next
    return head


def make_cycle(values, pos):
    head = build_list(values)
    if pos < 0 or head is None:
        return head
    tail = head
    while tail.next:
        tail = tail.next
    tail.next = node_at(head, pos)
    return head


# =============================================================================
# reverse_list — LeetCode 206
#
# Дана голова списка. Вернуть голову развёрнутого списка.
# На месте, новых узлов не создавать.
#
#     1 -> 2 -> 3 -> None    =>    3 -> 2 -> 1 -> None
# =============================================================================

def reverse_list(head):
    pass


# =============================================================================
# merge_two_lists — LeetCode 21
#
# Даны головы двух ОТСОРТИРОВАННЫХ списков. Слить в один отсортированный,
# переиспользуя узлы (новых не создавать). Равные значения — сначала
# из первого списка.
#
#     1 -> 2 -> 4  и  1 -> 3 -> 4   =>   1 -> 1 -> 2 -> 3 -> 4 -> 4
# =============================================================================

def merge_two_lists(a, b):
    pass


# =============================================================================
# detect_cycle — LeetCode 142
#
# Дана голова списка. Вернуть узел, с которого начинается цикл,
# или None, если цикла нет. O(1) памяти — без множества посещённых.
#
#     3 -> 2 -> 0 -> -4
#          ^___________|      -> узел со значением 2
# =============================================================================

def detect_cycle(head):
    pass


# =============================================================================
# ТЕСТЫ
# =============================================================================

def test_reverse_list():
    assert to_list(reverse_list(build_list([1, 2, 3]))) == [3, 2, 1]
    assert reverse_list(None) is None
    assert to_list(reverse_list(build_list([1]))) == [1]
    assert to_list(reverse_list(build_list([1, 2]))) == [2, 1]
    assert to_list(reverse_list(build_list([1, 2, 3, 4, 5]))) == [5, 4, 3, 2, 1]
    head = build_list([1, 2])
    second = head.next
    new_head = reverse_list(head)
    assert new_head is second
    assert new_head.next is head
    assert head.next is None
    assert to_list(reverse_list(build_list([1, 1, 2]))) == [2, 1, 1]


def test_merge_two_lists():
    assert to_list(merge_two_lists(build_list([1, 2, 4]),
                                   build_list([1, 3, 4]))) == [1, 1, 2, 3, 4, 4]
    assert to_list(merge_two_lists(None, build_list([1, 2]))) == [1, 2]
    assert to_list(merge_two_lists(build_list([1, 2]), None)) == [1, 2]
    assert merge_two_lists(None, None) is None
    assert to_list(merge_two_lists(build_list([1, 2]), build_list([8, 9]))) == [1, 2, 8, 9]
    assert to_list(merge_two_lists(build_list([8, 9]), build_list([1, 2]))) == [1, 2, 8, 9]
    a, b = build_list([1]), build_list([1])
    assert merge_two_lists(a, b) is a
    a, b = build_list([2]), build_list([1])
    merged = merge_two_lists(a, b)
    assert merged is b and merged.next is a
    assert to_list(merge_two_lists(build_list([1]),
                                   build_list([2, 3, 4, 5]))) == [1, 2, 3, 4, 5]


def test_detect_cycle():
    head = make_cycle([3, 2, 0, -4], 1)
    assert detect_cycle(head) is node_at(head, 1)
    head = make_cycle([1, 2], 0)
    assert detect_cycle(head) is head
    head = make_cycle([1], 0)
    assert detect_cycle(head) is head
    assert detect_cycle(build_list([1, 2, 3])) is None
    assert detect_cycle(build_list([1])) is None
    assert detect_cycle(None) is None
    assert detect_cycle(build_list([1, 1, 1])) is None
    head = make_cycle(list(range(10)), 7)
    assert detect_cycle(head) is node_at(head, 7)
    assert detect_cycle(build_list([1, 2, 3, 4])) is None


# Закомментируй те, что сегодня не пишешь.
test_reverse_list()
test_merge_two_lists()
test_detect_cycle()
print("ok")
