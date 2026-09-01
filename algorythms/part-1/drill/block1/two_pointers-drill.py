"""
ДРИЛЛ — TWO POINTERS

Пиши тела функций. Объяснений здесь нет специально — они в
two_pointers-ethalon.py, туда заглядывать ТОЛЬКО после запуска тестов.

Одна функция за сессию, 5 минут.
Ротация: 1) two_sum_sorted  2) move_zeroes  3) is_palindrome
         4) remove_duplicates  5) с начала.
Чередуй формы А и Б через раз — закрепляется именно различие между ними.

Перед тем как писать, проговори вслух: КАКАЯ ЭТО ФОРМА.
А — с двух концов навстречу. Б — оба слева, в одну сторону.

Не уложился или тест упал — пометь шаблон и поставь на завтра вне очереди,
но не досиживай.
"""


# =============================================================================
# two_sum_sorted — LeetCode 167
# (форма А)
#
# Дан ОТСОРТИРОВАННЫЙ массив nums и число target.
# Найти два РАЗНЫХ индекса l < r такие, что nums[l] + nums[r] == target.
# Вернуть [l, r]; если такой пары нет — вернуть [].
#
#     [2, 7, 11, 15], target = 9    -> [0, 1]
#     [2, 7, 11, 15], target = 100  -> []
# =============================================================================

def two_sum_sorted(nums, target):
    pass


# =============================================================================
# is_palindrome
# (форма А)
#
# Дана строка s. Определить, читается ли она одинаково слева направо
# и справа налево. Вернуть True или False.
# Пустая строка и строка из одного символа — палиндромы.
#
#     "abcba" -> True
#     "abca"  -> False
# =============================================================================

def is_palindrome(s):
    pass


# =============================================================================
# move_zeroes — LeetCode 283
# (форма Б)
#
# Дан массив nums. Переместить все нули в конец, СОХРАНИВ относительный
# порядок ненулевых элементов. На месте, без создания копии.
# Вернуть тот же массив.
#
#     [0, 2, 5, 0, 9]  -> [2, 5, 9, 0, 0]
#     [0, 3, 0, 1, 2]  -> [3, 1, 2, 0, 0]   (сдвиг, а не обмен!)
# =============================================================================

def move_zeroes(nums):
    pass


# =============================================================================
# remove_duplicates — LeetCode 26
# (форма Б)
#
# Дан ОТСОРТИРОВАННЫЙ массив nums. Удалить дубликаты на месте так,
# чтобы каждое уникальное значение встречалось ровно один раз, сохранив
# порядок. Вернуть количество уникальных элементов k; первые k элементов
# массива должны содержать эти значения. Что лежит дальше — неважно.
#
#     [1, 2, 2, 3, 4, 5, 6, 7, 7]  -> k = 7, массив [1,2,3,4,5,6,7, ...]
#
# Дополнительной памяти быть не должно: множество здесь — уже не этот шаблон.
# =============================================================================

def remove_duplicates(nums):
    pass


# =============================================================================
# ТЕСТЫ
# =============================================================================

def test_two_sum_sorted():
    assert two_sum_sorted([2, 7, 11, 15], 9) == [0, 1]
    assert two_sum_sorted([2, 7, 11, 15], 100) == []
    assert two_sum_sorted([2, 7, 11, 15], 3) == []
    assert two_sum_sorted([1, 2, 3, 4], 5) == [0, 3]
    assert two_sum_sorted([1, 2, 3, 4, 4, 9, 56, 90], 8) == [3, 4]
    assert two_sum_sorted([0, 0, 3, 4], 0) == [0, 1]
    assert two_sum_sorted([-3, -1, 0, 2, 5], -4) == [0, 1]
    assert two_sum_sorted([-3, -1, 0, 2, 5], 2) == [0, 4]
    assert two_sum_sorted([5], 10) == []
    assert two_sum_sorted([], 0) == []
    assert two_sum_sorted([1, 2], 3) == [0, 1]


def test_is_palindrome():
    assert is_palindrome("abcba") is True
    assert is_palindrome("abba") is True
    assert is_palindrome("racecar") is True
    assert is_palindrome("abca") is False
    assert is_palindrome("ab") is False
    assert is_palindrome("") is True
    assert is_palindrome("a") is True
    assert is_palindrome("aa") is True
    assert is_palindrome("abcda") is False
    assert is_palindrome("aabaa") is True


def test_move_zeroes():
    assert move_zeroes([0, 1, 0, 3, 12]) == [1, 3, 12, 0, 0]
    assert move_zeroes([0, 0]) == [0, 0]
    assert move_zeroes([1, 2, 3]) == [1, 2, 3]
    assert move_zeroes([0, 3, 0, 1, 2]) == [3, 1, 2, 0, 0]
    assert move_zeroes([0, 1]) == [1, 0]
    assert move_zeroes([1, 0]) == [1, 0]
    assert move_zeroes([0, 0, 1]) == [1, 0, 0]
    assert move_zeroes([]) == []
    assert move_zeroes([0]) == [0]
    assert move_zeroes([1]) == [1]


def test_remove_duplicates():
    a = [1, 1, 2, 2, 3]
    assert remove_duplicates(a) == 3
    assert a[:3] == [1, 2, 3]
    a = [1, 1, 1]
    assert remove_duplicates(a) == 1
    assert a[:1] == [1]
    a = [1, 2, 3]
    assert remove_duplicates(a) == 3
    assert a[:3] == [1, 2, 3]
    a = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
    assert remove_duplicates(a) == 5
    assert a[:5] == [0, 1, 2, 3, 4]
    a = [1, 2, 3, 3]
    assert remove_duplicates(a) == 3
    assert a[:3] == [1, 2, 3]
    a = [-3, -3, -1, 0, 0]
    assert remove_duplicates(a) == 3
    assert a[:3] == [-3, -1, 0]
    assert remove_duplicates([]) == 0
    assert remove_duplicates([1]) == 1


# Закомментируй те, что сегодня не пишешь.
test_two_sum_sorted()
test_is_palindrome()
test_move_zeroes()
test_remove_duplicates()
print("ok")
