"""
ШАБЛОН 17 — СТРУКТУРЫ ПОД ЗАКАЗ (напиши класс по спецификации)

КОГДА ПРИМЕНЯТЬ
    Просят не решить задачу, а НАПИСАТЬ СТРУКТУРУ с заданным набором
    операций и сложностью: "минимум за O(1)", "кэш на N элементов",
    "автодополнение по префиксу", "очередь на двух стеках".
    Слова-маркеры: "спроектируй", "реализуй класс", "все операции за O(1)".

ЧЕМ ЭТИ ЗАДАЧИ ОТЛИЧАЮТСЯ ОТ ОСТАЛЬНЫХ
    Алгоритма здесь нет — есть выбор внутреннего представления.
    Решается всё до первой строки кода, одним вопросом: что хранить, чтобы
    требуемая операция стала тривиальной. Дальше код пишется сам.
        минимум за O(1)      -> хранить минимум РЯДОМ с каждым элементом
        порядок обращений    -> хранить элементы В порядке обращений
        поиск по префиксу    -> хранить слова ПОБУКВЕННО, деревом

ЧЕТЫРЕ СКЕЛЕТА

    MinStack — стек пар (значение, минимум на этот момент)
        push: cur_min = min(x, текущий минимум)  и кладём пару
        остальное — обычный стек, всё за O(1)

    LRUCache — словарь, помнящий порядок (OrderedDict)
        get: есть -> move_to_end, отдаём; нет -> -1
        put: перезапись -> move_to_end; затем вставка;
             переполнение -> popitem(last=False), то есть самый старый

    Trie — вложенные словари, слово кончается маркером
        insert: node = node.setdefault(ch, {}) по каждой букве, в конце маркер
        search / starts_with: пройти по буквам; разница только в маркере

    MyQueue — два стека: в один кладём, из другого снимаем
        push: всегда во входной стек
        pop / peek: выходной пуст -> перелить в него ВЕСЬ входной,
                    затем работать с вершиной выходного

ЧЕТЫРЕ МЕСТА, ГДЕ ОШИБАЮТСЯ
    1. MinStack: хранить один общий минимум вместо минимума НА МОМЕНТ push.
       После pop этот минимум уже неверен, а восстановить его нечем.
    2. LRUCache: обновлять порядок только в put. get — это тоже обращение,
       после него элемент становится самым свежим, иначе выселяется живой.
    3. LRUCache: выселять последний вместо первого. popitem() без аргумента
       снимает самый СВЕЖИЙ — нужен popitem(last=False).
    4. Trie: обойтись без маркера конца слова. Тогда search("app") вернёт
       True после insert("apple") — префикс перепутан со словом.

ЕСЛИ ПРОСЯТ LRU БЕЗ OrderedDict
    Ждут dict + двусвязный список: словарь key -> узел, узлы связаны
    в порядке свежести, две фиктивные головы (head и tail) убирают все
    проверки на края. get = найти узел, вырезать, вставить после head;
    выселение = узел перед tail. Скажи это вслух — обычно этого достаточно,
    а писать разрешают через OrderedDict.

ЧЕТЫРЕ ВАРИАНТА, КОТОРЫЕ НАДО РАЗЛИЧАТЬ
    A) хранить ответ рядом с данными   — MinStack
    Б) хранить порядок обращений       — LRUCache
    В) хранить структуру ключа         — Trie
    Г) хранить в двух стеках, переливать лениво — MyQueue

ПОРЯДОК ДРИЛЛА (5 минут)
    В сессию берёшь ОДИН класс. Читаешь блок над ним в -drill.py как
    задание, пишешь целиком, гоняешь его тесты, сверяешь с этим файлом.
    Ротация: 1) MinStack  2) LRUCache  3) Trie  4) MyQueue.

ПРИЗНАК, ЧТО ШАБЛОН СЕЛ
    Прочитал спецификацию — сразу называешь внутреннее представление,
    и только потом начинаешь писать методы.
"""

from collections import OrderedDict


# =============================================================================
# MinStack — LeetCode 155, Min Stack
# ВАРИАНТ A: хранить ответ рядом с данными
#
# УСЛОВИЕ
#     Стек с четырьмя операциями, каждая за O(1):
#         push(x)   положить
#         pop()     снять и вернуть верхний
#         top()     посмотреть верхний
#         get_min() минимум среди всех, что сейчас в стеке
#     На пустом стеке pop, top и get_min возвращают None.
#
# ПРИМЕР
#     push(-2) push(0) push(-3)
#     get_min() -> -3
#     pop()     -> -3
#     top()     -> 0
#     get_min() -> -2        <- минимум обязан восстановиться
#
# ИДЕЯ
#     Кладём не значение, а пару (значение, минимум на этот момент).
#     Тогда минимум всего стека — это всегда второй элемент верхней пары,
#     а pop восстанавливает предыдущий минимум сам собой.
#
# ПОЧЕМУ НЕ ХРАНИТЬ ОДИН МИНИМУМ
#     Одно число работает до первого pop: если сняли как раз минимальный
#     элемент, узнать следующий минимум неоткуда — придётся идти по стеку,
#     а это уже O(n).
#
# ЧТО ЭТО СТОИТ
#     O(n) памяти вместо O(n) — те же порядки, просто пара вместо числа.
#     Экономный вариант — второй стек, куда минимум кладут только когда он
#     обновился; на интервью достаточно упомянуть.
# =============================================================================

class MinStack:
    def __init__(self):
        self.stack = []                      # пары (значение, минимум)

    def push(self, x):
        cur_min = x if not self.stack else min(x, self.stack[-1][1])
        self.stack.append((x, cur_min))

    def pop(self):
        return self.stack.pop()[0] if self.stack else None

    def top(self):
        return self.stack[-1][0] if self.stack else None

    def get_min(self):
        return self.stack[-1][1] if self.stack else None


# =============================================================================
# LRUCache — LeetCode 146, LRU Cache
# ВАРИАНТ Б: хранить порядок обращений
#
# УСЛОВИЕ
#     Кэш на capacity элементов, обе операции за O(1):
#         get(key)        значение или -1, если ключа нет
#         put(key, value) положить; если места нет, выселить тот ключ,
#                         к которому дольше всего не обращались
#     Обращение — это И get, И put.
#
# ПРИМЕР
#     c = LRUCache(2)
#     put(1,1) put(2,2)
#     get(1)    -> 1          теперь свежий — 1, старый — 2
#     put(3,3)  -> выселяется 2
#     get(2)    -> -1
#
# ИДЕЯ
#     OrderedDict помнит порядок вставки и умеет двигать ключ в конец
#     за O(1). Договоримся: конец — самый свежий, начало — кандидат
#     на выселение. Тогда весь класс — шесть строк.
#
# ТРИ МЕСТА, ГДЕ РЕШАЕТСЯ ПРАВИЛЬНОСТЬ
#     1. get: move_to_end, иначе порядок отражает вставки, а не обращения.
#     2. put существующего ключа: тоже move_to_end — это обращение.
#     3. Выселение: popitem(last=False) — с начала. По умолчанию popitem
#        снимает с конца, то есть самый свежий, и кэш превращается в мусор.
#
# ЛОВУШКА С РАЗМЕРОМ
#     Проверять переполнение надо ПОСЛЕ вставки и сравнивать с capacity
#     через >. Так и capacity = 0 работает: элемент кладётся и тут же
#     выселяется.
# =============================================================================

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.data = OrderedDict()            # начало — самый старый

    def get(self, key):
        if key not in self.data:
            return -1
        self.data.move_to_end(key)           # обращение освежает
        return self.data[key]

    def put(self, key, value):
        if key in self.data:
            self.data.move_to_end(key)
        self.data[key] = value

        if len(self.data) > self.capacity:
            self.data.popitem(last=False)    # самый старый, не самый свежий


# =============================================================================
# Trie — LeetCode 208, Implement Trie
# ВАРИАНТ В: хранить структуру ключа
#
# УСЛОВИЕ
#     Префиксное дерево с тремя операциями:
#         insert(word)        добавить слово
#         search(word)        True, если ТАКОЕ СЛОВО добавляли
#         starts_with(prefix) True, если есть слово с таким префиксом
#
# ПРИМЕР
#     insert("apple")
#     search("apple")      -> True
#     search("app")        -> False      <- это только префикс
#     starts_with("app")   -> True
#     insert("app")
#     search("app")        -> True
#
# ИДЕЯ
#     Узел — обычный словарь: буква -> следующий узел. Слово кладётся
#     побуквенно, общие префиксы хранятся один раз. Поиск по префиксу
#     стоит O(длины префикса) и не зависит от числа слов — ради этого
#     структура и нужна.
#
# МАРКЕР КОНЦА СЛОВА
#     Без него search и starts_with неразличимы. Кладём в узел ключ "$"
#     (любой символ, который не встречается в алфавите слов) — он и означает
#     "здесь слово кончается".
#
# ПОЧЕМУ ВНУТРИ ОДИН ОБЩИЙ ПРОХОД
#     search и starts_with отличаются одной последней проверкой,
#     поэтому спуск по буквам вынесен в _walk. Это же место потом
#     переиспользуется в "все слова с префиксом" и в поиске с джокером.
# =============================================================================

class Trie:
    END = "$"                                # маркер конца слова

    def __init__(self):
        self.root = {}

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})   # нет буквы — заводим узел
        node[self.END] = True

    def search(self, word):
        node = self._walk(word)
        return node is not None and self.END in node

    def starts_with(self, prefix):
        return self._walk(prefix) is not None

    def _walk(self, s):
        node = self.root
        for ch in s:
            if ch not in node:
                return None
            node = node[ch]
        return node


# =============================================================================
# MyQueue — LeetCode 232, Implement Queue using Stacks
# ВАРИАНТ Г: очередь из двух стеков, перенос только по необходимости
#
# УСЛОВИЕ
#     Реализовать очередь (первым пришёл — первым ушёл), используя только
#     два стека: у списка разрешены append, pop() с конца и взгляд на [-1].
#         push(x)  — положить в хвост очереди
#         pop()    — снять и вернуть голову; очередь пуста — None
#         peek()   — вернуть голову, не снимая; очередь пуста — None
#         empty()  — True, если элементов нет
#
# ПРИМЕР
#     q = MyQueue()
#     q.push(1); q.push(2)       inbox [1, 2]   outbox []
#     q.peek()   -> 1            inbox []       outbox [2, 1]   перелили
#     q.pop()    -> 1            inbox []       outbox [2]
#     q.push(3)                  inbox [3]      outbox [2]
#     q.pop()    -> 2            inbox [3]      outbox []       переливать не надо
#     q.pop()    -> 3            inbox []       outbox []       перелили 3 и сняли
#
# ИДЕЯ
#     Стек отдаёт элементы в обратном порядке. Перелить один стек в другой —
#     значит развернуть порядок ещё раз, то есть получить исходный.
#     inbox принимает, outbox отдаёт; между ними — перелив.
#
# ЕДИНСТВЕННОЕ ПРАВИЛО: ПЕРЕЛИВАТЬ ТОЛЬКО В ПУСТОЙ outbox
#     В outbox элементы уже лежат в порядке выдачи, старые сверху.
#     Досыпать на них новые — значит поставить новые впереди старых.
#     Поэтому перелив идёт, только когда outbox опустел, и сразу ВЕСЬ inbox.
#
# ПОЧЕМУ ЭТО O(1), ХОТЯ ВНУТРИ ЦИКЛ
#     Каждый элемент за всю жизнь перекладывается один раз: inbox -> outbox.
#     n операций суммарно стоят O(n), то есть O(1) на операцию в среднем
#     (амортизированно). Это слово на интервью и ждут.
#
# ЧТО ОБЩЕГО С ОСТАЛЬНЫМИ КЛАССАМИ ФАЙЛА
#     Снова всё решает представление: порядок выдачи хранится не в одном
#     контейнере, а в двух, и каждый отвечает за свой конец очереди.
# =============================================================================

class MyQueue:
    def __init__(self):
        self.inbox = []                      # сюда кладём
        self.outbox = []                     # отсюда снимаем

    def push(self, x):
        self.inbox.append(x)

    def pop(self):
        self._shift()
        return self.outbox.pop() if self.outbox else None

    def peek(self):
        self._shift()
        return self.outbox[-1] if self.outbox else None

    def empty(self):
        return not self.inbox and not self.outbox   # смотреть надо в оба

    def _shift(self):
        if not self.outbox:                  # ТОЛЬКО в пустой, иначе порядок сломан
            while self.inbox:
                self.outbox.append(self.inbox.pop())


# =============================================================================
# ТЕСТЫ
# Помеченные (!) — ловушки. Кривая версия проходит простые тесты
# и падает именно на них.
# =============================================================================

def test_minstack():
    s = MinStack()
    # (!) пустой стек не должен падать
    assert s.pop() is None and s.top() is None and s.get_min() is None
    # базовый сценарий из условия
    s.push(-2)
    s.push(0)
    s.push(-3)
    assert s.get_min() == -3
    assert s.pop() == -3
    assert s.top() == 0
    # (!) минимум обязан восстановиться после pop
    assert s.get_min() == -2
    # (!) дубликаты минимума: сняли один — второй ещё в стеке
    s = MinStack()
    s.push(1)
    s.push(1)
    s.push(2)
    assert s.get_min() == 1
    s.pop()
    s.pop()
    assert s.get_min() == 1
    # возрастающая последовательность — минимум не меняется
    s = MinStack()
    for x in [3, 4, 5]:
        s.push(x)
    assert s.get_min() == 3 and s.top() == 5
    # убывающая — минимум обновляется каждый раз
    s = MinStack()
    for x in [5, 4, 3]:
        s.push(x)
    assert s.get_min() == 3
    s.pop()
    assert s.get_min() == 4
    # (!) стек опустошили и наполнили заново
    s = MinStack()
    s.push(7)
    assert s.pop() == 7
    assert s.get_min() is None
    s.push(9)
    assert s.get_min() == 9


def test_lrucache():
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == 1
    # (!) выселяется тот, к кому дольше не обращались, а get — тоже обращение
    c.put(3, 3)
    assert c.get(2) == -1
    assert c.get(1) == 1 and c.get(3) == 3
    # (!) отсутствующий ключ
    assert c.get(42) == -1
    # (!) перезапись существующего: размер не растёт, ключ становится свежим
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    c.put(1, 10)
    c.put(3, 3)
    assert c.get(1) == 10
    assert c.get(2) == -1
    # (!) put тоже освежает: 2 обновили, значит вылететь должен 1
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    c.put(2, 22)
    c.put(3, 3)
    assert c.get(1) == -1 and c.get(2) == 22 and c.get(3) == 3
    # (!) вырожденные размеры
    c = LRUCache(1)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == -1 and c.get(2) == 2
    c = LRUCache(0)
    c.put(1, 1)
    assert c.get(1) == -1
    # длинная последовательность: держим последние три ключа
    c = LRUCache(3)
    for k in range(10):
        c.put(k, k * k)
    assert [c.get(k) for k in range(10)] == [-1] * 7 + [49, 64, 81]


def test_trie():
    t = Trie()
    t.insert("apple")
    assert t.search("apple") is True
    # (!) префикс — ещё не слово
    assert t.search("app") is False
    assert t.starts_with("app") is True
    t.insert("app")
    assert t.search("app") is True
    # (!) пустое дерево
    empty = Trie()
    assert empty.search("a") is False
    assert empty.starts_with("a") is False
    # (!) пустая строка: префикс есть всегда, слово — только если добавляли
    assert empty.starts_with("") is True
    assert empty.search("") is False
    empty.insert("")
    assert empty.search("") is True
    # (!) слово длиннее добавленного
    t = Trie()
    t.insert("app")
    assert t.search("apple") is False
    assert t.starts_with("apple") is False
    # общие префиксы не мешают друг другу
    t = Trie()
    for w in ["car", "card", "care", "cat"]:
        t.insert(w)
    assert all(t.search(w) for w in ["car", "card", "care", "cat"])
    assert t.search("ca") is False
    assert t.starts_with("car") is True
    assert t.starts_with("cab") is False
    # (!) повторная вставка ничего не ломает
    t.insert("car")
    assert t.search("car") is True and t.search("card") is True


def test_myqueue():
    q = MyQueue()
    assert q.empty() is True
    q.push(1)
    q.push(2)
    assert q.peek() == 1
    assert q.pop() == 1
    # (!) элемент остался только в одном из стеков — очередь не пуста
    assert q.empty() is False
    # (!) push между двумя pop — ловит перелив в непустой outbox
    q.push(3)
    assert q.pop() == 2
    assert q.pop() == 3
    assert q.empty() is True
    # (!) пустая очередь
    assert q.pop() is None
    assert q.peek() is None
    # (!) peek не снимает
    q.push(5)
    assert q.peek() == 5
    assert q.peek() == 5
    assert q.pop() == 5
    assert q.empty() is True
    # (!) только что положенный элемент лежит в inbox — очередь не пуста
    q.push(6)
    assert q.empty() is False
    # (!) порядок сохраняется при чередовании push и pop
    q = MyQueue()
    out = []
    for i in range(10):
        q.push(i)
        if i % 3 == 2:
            out.append(q.pop())
    while not q.empty():
        out.append(q.pop())
    assert out == list(range(10))


test_minstack()
test_lrucache()
test_trie()
test_myqueue()
print("ok — structures, все тесты прошли")
