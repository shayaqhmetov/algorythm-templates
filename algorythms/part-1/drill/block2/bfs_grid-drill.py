"""
ДРИЛЛ — BFS ПО СЕТКЕ

Пиши тела функций. Объяснений здесь нет специально — они в
bfs_grid-ethalon.py, туда заглядывать ТОЛЬКО после запуска тестов.

Одна функция за сессию, 5 минут.
Ротация: 1) num_islands  2) oranges_rotting  3) shortest_path  4) update_matrix.
Направления (4 стороны, 8 сторон) пишутся с нуля каждый раз — готовых нет.

Не уложился или тест упал — пометь шаблон и поставь на завтра вне очереди,
но не досиживай.
"""

from collections import deque


# =============================================================================
# num_islands — LeetCode 200
#
# Дана сетка из символов "1" (суша) и "0" (вода).
# Остров — группа клеток суши, соединённых по горизонтали или вертикали
# (по диагонали НЕ считается). Посчитать число островов.
#
#     [["1","1","0","0"],
#      ["1","1","0","0"],
#      ["0","0","1","0"],
#      ["0","0","0","1"]]   -> 3
# =============================================================================

def num_islands(grid):
    if not grid or not grid[0]:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    count = 0
    seen = set()
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != "1" or (r,c) in seen:
                continue
            
            count+=1
            seen.add((r,c))
            q = deque([(r,c)])
            while q:
                cr, cc = q.popleft()
                for dr, dc in DIRS4:
                    nr, nc = cr+dr, cc+dc
                    if (
                        0 <= nr < rows and 0 <= nc < cols
                        and grid[nr][nc] == "1"
                        and (nr, nc) not in seen
                    ):
                        seen.add((nr,nc))
                        q.append((nr,nc))
    return count



# =============================================================================
# oranges_rotting — LeetCode 994
#
# Сетка: 0 — пусто, 1 — свежий апельсин, 2 — гнилой.
# Каждую минуту гнилой заражает соседей по горизонтали и вертикали.
# Вернуть, за сколько минут сгниют все.
# Если какой-то свежий недостижим — вернуть -1.
#
#     [[2,1,1],
#      [1,1,0],
#      [0,1,1]]   -> 4
#
#     [[0,2]]     -> 0    (свежих нет)
#     [[1,1]]     -> -1   (гнилых нет)
# =============================================================================

def oranges_rotting(grid):
    if not grid or not grid[0]:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    
    fresh = 0
    q = deque()
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                q.append((r,c))
            if grid[r][c] == 1:
                fresh += 1
    minutes = 0     
    while q and fresh:
        for _ in range(len(q)):
            cr, cc = q.popleft()
            for dr, dc in DIRS4:
                nr, nc = cr + dr, cc + dc
                if(
                    0 <= nr < rows and 0 <= nc < cols
                    and grid[nr][nc] == 1
                ):
                    grid[nr][nc] = 2
                    q.append((nr,nc))
                    fresh -= 1
        minutes += 1
            
    return minutes if fresh == 0 else -1


# =============================================================================
# shortest_path — LeetCode 1091
#
# Квадратная сетка n x n из 0 (проходимо) и 1 (стена).
# Пройти из левого верхнего угла в правый нижний, двигаясь в ЛЮБУЮ
# из 8 сторон (включая диагонали).
# Вернуть длину пути В КЛЕТКАХ (стартовая и конечная включены).
# Пути нет — вернуть -1.
#
#     [[0,0,0],
#      [1,1,0],
#      [1,1,0]]   -> 4
#
#     [[0,1],
#      [1,0]]     -> 2    (диагональ)
#
#     [[0]]       -> 1
# =============================================================================

def shortest_path(grid):
    n = len(grid)
    if n == 0 or grid[0][0] == 1 or grid[n-1][n-1] == 1:
        return -1
    
    dist = 1
    q = deque([(0,0)])
    seen = {(0,0)}
    while q:
        for _ in range(len(q)):
            r,c = q.popleft()
            if r == n-1 and c == n -1:
                return dist
            for dr, dc in DIRS8:
                nr, nc = r+dr, c+dc
            
                if (
                    0 <= nr < n and 0 <= nc < n
                    and grid[nr][nc] == 0
                    and (nr, nc) not in seen
                ):
                    q.append((nr, nc))
                    seen.add((nr, nc))
        dist += 1
    return -1


# =============================================================================
# update_matrix — LeetCode 542
#
# Сетка из 0 и 1. Для КАЖДОЙ клетки найти расстояние до ближайшего нуля
# (шаги по горизонтали и вертикали). У самого нуля расстояние 0.
# Вернуть НОВУЮ сетку расстояний, вход не менять.
# Нулей нет вовсе — у всех клеток -1. Пустая сетка -> [].
#
#     [[0,0,0],        [[0,0,0],
#      [0,1,0],   ->    [0,1,0],
#      [1,1,1]]         [1,2,1]]
#
#     [[0,1,1,1,0]]  ->  [[0,1,2,1,0]]
# =============================================================================

def update_matrix(grid):
    pass


# =============================================================================
# ТЕСТЫ
# =============================================================================

def test_num_islands():
    assert num_islands([["1", "1", "0", "0"],
                        ["1", "1", "0", "0"],
                        ["0", "0", "1", "0"],
                        ["0", "0", "0", "1"]]) == 3
    assert num_islands([["1", "1", "1"],
                        ["1", "1", "1"]]) == 1
    assert num_islands([["1", "0"],
                        ["0", "1"]]) == 2
    assert num_islands([["1", "0", "1"],
                        ["0", "1", "0"],
                        ["1", "0", "1"]]) == 5
    assert num_islands([["0", "0"],
                        ["0", "0"]]) == 0
    assert num_islands([]) == 0
    assert num_islands([[]]) == 0
    assert num_islands([["1"]]) == 1
    assert num_islands([["1", "0", "1", "1"]]) == 2
    assert num_islands([["1"], ["0"], ["1"]]) == 2


def test_oranges_rotting():
    assert oranges_rotting([[2, 1, 1],
                            [1, 1, 0],
                            [0, 1, 1]]) == 4
    assert oranges_rotting([[2, 1, 1],
                            [0, 1, 1],
                            [1, 0, 1]]) == -1
    assert oranges_rotting([[0, 2]]) == 0
    assert oranges_rotting([[0, 0, 0]]) == 0
    assert oranges_rotting([[1, 1]]) == -1
    assert oranges_rotting([[2, 1, 1, 1, 2]]) == 2
    assert oranges_rotting([[2, 1, 1, 1]]) == 3
    assert oranges_rotting([[0]]) == 0
    assert oranges_rotting([[2]]) == 0
    assert oranges_rotting([[1]]) == -1


def test_shortest_path():
    assert shortest_path([[0, 0, 0],
                          [1, 1, 0],
                          [1, 1, 0]]) == 4
    assert shortest_path([[0, 1],
                          [1, 0]]) == 2
    assert shortest_path([[0]]) == 1
    assert shortest_path([[1, 0],
                          [0, 0]]) == -1
    assert shortest_path([[0, 0],
                          [0, 1]]) == -1
    assert shortest_path([[0, 0, 0],
                          [1, 1, 1],
                          [0, 0, 0]]) == -1
    assert shortest_path([[0, 0, 0],
                          [0, 0, 0],
                          [0, 0, 0]]) == 3
    assert shortest_path([[0, 0, 0, 0],
                          [1, 1, 1, 0],
                          [0, 0, 0, 0],
                          [0, 1, 1, 0]]) == 6


def test_update_matrix():
    assert update_matrix([[0, 0, 0],
                          [0, 1, 0],
                          [1, 1, 1]]) == [[0, 0, 0],
                                          [0, 1, 0],
                                          [1, 2, 1]]
    assert update_matrix([[0, 0, 0],
                          [0, 1, 0],
                          [0, 0, 0]]) == [[0, 0, 0],
                                          [0, 1, 0],
                                          [0, 0, 0]]
    assert update_matrix([[0, 1, 1, 1, 0]]) == [[0, 1, 2, 1, 0]]
    assert update_matrix([[0, 1, 1],
                          [1, 1, 1],
                          [1, 1, 1]]) == [[0, 1, 2],
                                          [1, 2, 3],
                                          [2, 3, 4]]
    assert update_matrix([[1], [1], [0]]) == [[2], [1], [0]]
    assert update_matrix([[0, 0]]) == [[0, 0]]
    assert update_matrix([[1, 1]]) == [[-1, -1]]
    assert update_matrix([]) == []
    assert update_matrix([[]]) == []
    assert update_matrix([[0]]) == [[0]]
    src = [[0, 1], [1, 1]]
    assert update_matrix(src) == [[0, 1], [1, 2]]
    assert src == [[0, 1], [1, 1]]


# Закомментируй те, что сегодня не пишешь.
# test_num_islands()
# test_oranges_rotting()
test_shortest_path()
test_update_matrix()
print("ok")
