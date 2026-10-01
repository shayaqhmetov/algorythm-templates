"""
ШАБЛОН 16 — СВЯЗНЫЙ СПИСОК (указатели руками)

КОГДА ПРИМЕНЯТЬ
    В условии есть узлы и next: развернуть, слить, найти цикл, убрать
    k-й с конца, проверить палиндром, отсортировать список.
    Слова-маркеры: "linked list", "O(1) памяти", "без преобразования
    в массив", "голова списка".

ЗАЧЕМ ЭТО СПРАШИВАЮТ
    Списков в продакшене почти нет, а спрашивают их постоянно — потому что
    на них видно, умеешь ли ты держать в голове указатели: не потерять хвост,
    не зациклить, не обратиться к None. Массив всё прощает, список — нет.

ТРИ ПРИЁМА, КОТОРЫМИ ЗАКРЫВАЕТСЯ ПОЧТИ ВСЁ

    1. ТРИ УКАЗАТЕЛЯ — развернуть связи
           prev, cur = None, head
           while cur:
               nxt = cur.next          # запомнить ДО перезаписи
               cur.next = prev
               prev, cur = cur, nxt
           return prev                 # prev — новая голова

    2. ФИКТИВНАЯ ГОЛОВА (dummy) — собрать новый список
           dummy = ListNode()
           tail = dummy
           ... tail.next = нужный узел; tail = tail.next ...
           return dummy.next
       Избавляет от ветки "а если результат пуст" и "а если это первый узел".

    3. ДВА БЕГУНА (Флойд) — цикл, середина, k-й с конца
           slow, fast = head, head
           while fast and fast.next:
               slow, fast = slow.next, fast.next.next
               if slow is fast: ...

ЧЕТЫРЕ МЕСТА, ГДЕ ОШИБАЮТСЯ
    1. Потерять хвост: cur.next = prev до того, как сохранили cur.next.
       Список обрывается на втором узле, и это самая частая ошибка.
    2. Условие while fast and fast.next, а не только fast.
       На чётной длине fast.next.next обратится к None.next.
    3. Сравнивать узлы через ==, а не is. Равенство может быть переопределено
       или сравнить значения; цикл ищется по ТОЖДЕСТВУ узлов.
    4. Вернуть head вместо prev / dummy.next. После разворота head — хвост,
       и наружу уедет список из одного элемента.

ТРИ ВАРИАНТА, КОТОРЫЕ НАДО РАЗЛИЧАТЬ
    A) развернуть связи   — reverse_list     (три указателя)
    Б) собрать новый      — merge_two_lists  (dummy)
    В) найти цикл         — detect_cycle     (два бегуна)

ПОРЯДОК ДРИЛЛА (5 минут)
    В сессию берёшь ОДНУ функцию. Читаешь блок над ней в -drill.py как
    задание, пишешь тело, гоняешь её тесты, сверяешь с этим файлом.
    Ротация: 1) reverse_list  2) merge_two_lists  3) detect_cycle  4) с начала.
    ListNode и сборщики списков дриллить не надо — они уже написаны.

ПРИЗНАК, ЧТО ШАБЛОН СЕЛ
    Рука сама пишет nxt = cur.next первой строкой цикла, а думаешь только
    про то, что вернуть в конце.
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build_list(values):
    """Список из питоновского списка. Нужна только для тестов."""
    dummy = ListNode()
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def to_list(head):
    """Обратно в питоновский список. Только для НЕзациклённых списков."""
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def node_at(head, i):
    """i-й узел с нуля — чтобы сравнивать по тождеству, а не по значению."""
    for _ in range(i):
        head = head.next
    return head


def make_cycle(values, pos):
    """Список, у которого хвост замкнут на узел pos. pos = -1 — без цикла."""
    head = build_list(values)
    if pos < 0 or head is None:
        return head
    tail = head
    while tail.next:
        tail = tail.next
    tail.next = node_at(head, pos)
    return head


# =============================================================================
# reverse_list — LeetCode 206, Reverse Linked List
# ВАРИАНТ A: три указателя
#
# УСЛОВИЕ
#     Дано: голова списка.
#     Вернуть: голову развёрнутого списка. НА МЕСТЕ, новых узлов не создавать.
#
# ПРИМЕР
#     1 -> 2 -> 3 -> None    =>    3 -> 2 -> 1 -> None
#
#     prev=None  cur=1        nxt=2   1.next=None   prev=1  cur=2
#     prev=1     cur=2        nxt=3   2.next=1      prev=2  cur=3
#     prev=2     cur=3        nxt=None 3.next=2     prev=3  cur=None
#     cur опустел -> новая голова это prev = 3
#
# ПОЧЕМУ НУЖЕН ТРЕТИЙ УКАЗАТЕЛЬ
#     cur.next = prev затирает единственную ссылку на остаток списка.
#     Если не сохранить её заранее, продолжать будет некуда — хвост потерян.
#     Отсюда порядок: сначала nxt, потом переворот, потом сдвиг.
#
# ЧТО ВЕРНУТЬ
#     prev, а не head и не cur. В момент выхода cur is None,
#     а head стал последним узлом.
# =============================================================================

def reverse_list(head):
    prev, cur = None, head

    while cur:
        nxt = cur.next                   # сохранить ДО перезаписи
        cur.next = prev
        prev, cur = cur, nxt

    return prev                          # новая голова


# =============================================================================
# merge_two_lists — LeetCode 21, Merge Two Sorted Lists
# ВАРИАНТ Б: фиктивная голова
#
# УСЛОВИЕ
#     Дано: две головы ОТСОРТИРОВАННЫХ списков.
#     Вернуть: голову общего отсортированного списка, переиспользуя узлы
#              (новых не создавать). Равные значения — сначала из первого.
#
# ПРИМЕР
#     a: 1 -> 2 -> 4
#     b: 1 -> 3 -> 4      =>    1 -> 1 -> 2 -> 3 -> 4 -> 4
#
# ЗАЧЕМ DUMMY
#     Без фиктивной головы первый шаг особенный: голову результата надо
#     выбрать отдельной веткой, а дальше дописывать в хвост. Dummy убирает
#     этот случай: пишем всегда в tail.next, а в конце отдаём dummy.next.
#     Тот же приём в "удалить узлы", "разбить список", "вставить в середину".
#
# ХВОСТ ОДНОЙ СТРОКОЙ
#     tail.next = a or b — остаток второго списка уже отсортирован
#     и уже связан, поэтому подцепляется целиком. Цикл для него не нужен.
#
# СВЯЗЬ С ШАБЛОНОМ 13
#     Это merge из сортировки слиянием, только на указателях,
#     и знак тот же: <= держит стабильность.
# =============================================================================

def merge_two_lists(a, b):
    dummy = ListNode()
    tail = dummy

    while a and b:
        if a.val <= b.val:               # <= — равные берём из первого
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next

    tail.next = a or b                   # остаток целиком
    return dummy.next


# =============================================================================
# detect_cycle — LeetCode 142, Linked List Cycle II
# ВАРИАНТ В: два бегуна, алгоритм Флойда
#
# УСЛОВИЕ
#     Дано: голова списка.
#     Вернуть: узел, с которого начинается цикл, или None, если цикла нет.
#     O(1) памяти — множество посещённых узлов не заводить.
#
# ПРИМЕР
#     3 -> 2 -> 0 -> -4
#          ^___________|      -> узел со значением 2
#
# ПОЧЕМУ ОНИ ВСТРЕТЯТСЯ
#     Внутри цикла быстрый приближается к медленному на один узел за шаг,
#     поэтому рано или поздно догоняет. Если цикла нет, быстрый упирается
#     в None — отсюда и условие выхода.
#
# ПОЧЕМУ ВТОРОЙ ПРОХОД ДАЁТ НАЧАЛО ЦИКЛА
#     Пусть до входа в цикл a шагов, а встреча произошла в b шагах от входа.
#     К моменту встречи медленный прошёл a + b, быстрый вдвое больше,
#     и разница a + b кратна длине цикла. Значит если один пойдёт от головы,
#     а второй от места встречи ОДИНАКОВЫМ шагом, они сойдутся ровно на входе.
#     Это то самое место, где на интервью ждут не код, а объяснение.
#
# ЛОВУШКА СО СРАВНЕНИЕМ
#     slow is fast, а не ==. Ищем один и тот же УЗЕЛ, а не равные значения:
#     в списке 1 -> 1 -> None значения равны, а цикла нет.
# =============================================================================

def detect_cycle(head):
    slow = fast = head

    while fast and fast.next:            # оба условия обязательны
        slow = slow.next
        fast = fast.next.next

        if slow is fast:                 # встретились — цикл есть
            slow = head
            while slow is not fast:      # шагаем в ногу до входа в цикл
                slow = slow.next
                fast = fast.next
            return slow

    return None                          # быстрый упёрся в конец


# =============================================================================
# ТЕСТЫ
# build_list, to_list, node_at и make_cycle уже написаны — их дриллить не надо.
# Помеченные (!) — ловушки.
# =============================================================================

def test_reverse_list():
    # базовый
    assert to_list(reverse_list(build_list([1, 2, 3]))) == [3, 2, 1]
    # (!) вырожденные
    assert reverse_list(None) is None
    assert to_list(reverse_list(build_list([1]))) == [1]
    # чётная длина
    assert to_list(reverse_list(build_list([1, 2]))) == [2, 1]
    # длиннее
    assert to_list(reverse_list(build_list([1, 2, 3, 4, 5]))) == [5, 4, 3, 2, 1]
    # (!) узлы переиспользуются, а не создаются заново
    head = build_list([1, 2])
    second = head.next
    new_head = reverse_list(head)
    assert new_head is second
    # (!) старая голова стала хвостом и её next обнулён
    assert new_head.next is head
    assert head.next is None
    # дубликаты значений
    assert to_list(reverse_list(build_list([1, 1, 2]))) == [2, 1, 1]


def test_merge_two_lists():
    # базовый
    assert to_list(merge_two_lists(build_list([1, 2, 4]),
                                   build_list([1, 3, 4]))) == [1, 1, 2, 3, 4, 4]
    # (!) один пустой — возвращаем второй как есть
    assert to_list(merge_two_lists(None, build_list([1, 2]))) == [1, 2]
    assert to_list(merge_two_lists(build_list([1, 2]), None)) == [1, 2]
    # (!) оба пустые
    assert merge_two_lists(None, None) is None
    # диапазоны не пересекаются — хвост подцепляется целиком
    assert to_list(merge_two_lists(build_list([1, 2]), build_list([8, 9]))) == [1, 2, 8, 9]
    assert to_list(merge_two_lists(build_list([8, 9]), build_list([1, 2]))) == [1, 2, 8, 9]
    # (!) при равных значениях первым идёт узел из ПЕРВОГО списка
    a, b = build_list([1]), build_list([1])
    assert merge_two_lists(a, b) is a
    # (!) новых узлов не создаём
    a, b = build_list([2]), build_list([1])
    merged = merge_two_lists(a, b)
    assert merged is b and merged.next is a
    # разной длины
    assert to_list(merge_two_lists(build_list([1]),
                                   build_list([2, 3, 4, 5]))) == [1, 2, 3, 4, 5]


def test_detect_cycle():
    # базовый: хвост замкнут на второй узел
    head = make_cycle([3, 2, 0, -4], 1)
    assert detect_cycle(head) is node_at(head, 1)
    # цикл на голове
    head = make_cycle([1, 2], 0)
    assert detect_cycle(head) is head
    # (!) сам на себя
    head = make_cycle([1], 0)
    assert detect_cycle(head) is head
    # (!) цикла нет
    assert detect_cycle(build_list([1, 2, 3])) is None
    assert detect_cycle(build_list([1])) is None
    assert detect_cycle(None) is None
    # (!) равные значения — не цикл: сравнивать надо узлы, а не val
    assert detect_cycle(build_list([1, 1, 1])) is None
    # цикл в самом конце длинного списка
    head = make_cycle(list(range(10)), 7)
    assert detect_cycle(head) is node_at(head, 7)
    # (!) чётная длина без цикла — на ней падает слишком слабое условие while
    assert detect_cycle(build_list([1, 2, 3, 4])) is None


test_reverse_list()
test_merge_two_lists()
test_detect_cycle()
print("ok — linked_list, все тесты прошли")
