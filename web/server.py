#!/usr/bin/env python3
"""
Локальный веб-тренажёр по шаблонам алгоритмов.

    python3 web/server.py          # http://127.0.0.1:8765
    python3 web/server.py 9000     # другой порт

Читает файлы из algorythms/part-1/{ethalons,drill}/blockN/ — отдельной базы
нет, единственный источник правды это сами .py файлы.

Код из редактора выполняется настоящим python3 в отдельном процессе
с таймаутом. Сервер слушает только 127.0.0.1 и предназначен для запуска
на своей машине.
"""

import ast
import json
import os
import re
import subprocess
import sys
import tempfile
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

WEB = Path(__file__).resolve().parent
ROOT = WEB.parent
PART = ROOT / "algorythms" / "part-1"

RUN_TIMEOUT = 15          # секунд на прогон тестов
MAX_BODY = 512 * 1024     # ограничение на размер запроса


# ---------------------------------------------------------------------------
# разбор .py файлов
# ---------------------------------------------------------------------------

def leading_comment(lines, node):
    """Комментарий-шапка, приклеенный к узлу сверху."""
    i = node.lineno - 2
    block = []
    while i >= 0 and (lines[i].lstrip().startswith("#") or not lines[i].strip()):
        block.append(lines[i])
        i -= 1
    block.reverse()
    while block and not block[0].strip():
        block.pop(0)
    while block and not block[-1].strip():
        block.pop()
    return "\n".join(block)


def is_test(node):
    return isinstance(node, ast.FunctionDef) and node.name.startswith("test_")


def is_definition(node):
    return isinstance(node, (ast.FunctionDef, ast.ClassDef))


def parse_module(path):
    src = path.read_text(encoding="utf-8")
    tree = ast.parse(src)
    lines = src.splitlines()
    return src, tree, lines


def stub_of(node, src):
    """Сигнатура + pass (для классов — все методы с pass)."""
    if isinstance(node, ast.ClassDef):
        head = [f"class {node.name}:"]
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                sig = ast.get_source_segment(src, item).splitlines()[0].strip()
                head.append(f"    {sig}")
                head.append("        pass")
                head.append("")
        while head and not head[-1]:
            head.pop()
        return "\n".join(head) + "\n"

    sig = ast.get_source_segment(src, node).splitlines()[0].strip()
    return f"{sig}\n    pass\n"


def collect(path):
    """Определения верхнего уровня: имя -> {node, code, doc}."""
    src, tree, lines = parse_module(path)
    out = {}
    for node in tree.body:
        if is_definition(node):
            out[node.name] = {
                "node": node,
                "code": ast.get_source_segment(src, node),
                "doc": leading_comment(lines, node),
            }
    return src, tree, out


def constants_of(src, tree):
    """Константы верхнего уровня (DIRS4, DIRS8): имя -> исходник присваивания."""
    out = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    out[t.id] = ast.get_source_segment(src, node)
    return out


def needs_of(target, tree):
    """
    Что пишется с нуля ВМЕСТЕ с целевой функцией: другие цели дрилла, которые
    она вызывает (bs, build_adj, DSU), и константы верхнего уровня (DIRS4).
    Из собранного файла они выбрасываются — их место в редакторе.
    Вспомогательный код без теста (ListNode, build) остаётся готовым.
    Имена идут в порядке файла.
    """
    defs = {n.name: n for n in tree.body if is_definition(n)}
    tested = {n for n in defs if f"test_{n.lower()}" in defs}
    consts = {t.id: n for n in tree.body if isinstance(n, ast.Assign)
              for t in n.targets if isinstance(t, ast.Name)}
    pool = {**{n: defs[n] for n in tested}, **consts}

    found, todo = set(), [defs[target]]
    while todo:
        for sub in ast.walk(todo.pop()):
            if isinstance(sub, ast.Name) and sub.id in pool and sub.id != target \
                    and sub.id not in found:
                found.add(sub.id)
                todo.append(pool[sub.id])                  # bs сам может что-то звать
    return sorted(found, key=lambda n: pool[n].lineno)


def title_of(docstring):
    first = (docstring or "").strip().splitlines()
    if not first:
        return 999, "без названия"
    head = first[0].strip()
    m = re.match(r"ШАБЛОН\s+(\d+)\s*[—-]\s*(.+)", head)
    if m:
        return int(m.group(1)), m.group(2).strip()
    return 999, head


def load_template(block, name):
    ethalon_path = PART / "ethalons" / block / f"{name}-ethalon.py"
    drill_path = PART / "drill" / block / f"{name}-drill.py"
    if not ethalon_path.exists():
        return None

    esrc, etree, edefs = collect(ethalon_path)
    number, title = title_of(ast.get_docstring(etree))

    dsrc, ddefs = "", {}
    if drill_path.exists():
        dsrc, _dtree, ddefs = collect(drill_path)

    tests = {n: d for n, d in edefs.items() if n.startswith("test_")}
    consts = constants_of(esrc, etree)

    def stub(fname):                                   # заглушка — из дрилла, если она там есть
        drill = ddefs.get(fname)
        return stub_of((drill or edefs[fname])["node"], dsrc if drill else esrc)

    functions = []
    for fname, d in edefs.items():
        if fname.startswith("test_"):
            continue
        if f"test_{fname.lower()}" not in tests:
            continue                                   # без теста — вспомогательный код
        drill = ddefs.get(fname)
        needs = needs_of(fname, etree)
        # константы в заглушку не идут: их пишут с нуля, и имя у них любое
        parts = [n for n in needs if n in edefs] + [fname]
        functions.append({
            "name": fname,
            "kind": "class" if isinstance(d["node"], ast.ClassDef) else "function",
            "doc": d["doc"],
            "needs": needs,
            # эталон для спойлера и сравнения — вместе со всем, что пишется с нуля
            "full": "\n\n\n".join(consts.get(n) or edefs[n]["code"] for n in needs + [fname]),
            "code": d["code"],
            "task": (drill or {}).get("doc") or d["doc"],
            "stub": "\n\n".join(stub(n) for n in parts),
            "test": f"test_{fname.lower()}" if f"test_{fname.lower()}" in tests else None,
        })

    return {
        "id": f"{block}/{name}",
        "block": block,
        "name": name,
        "number": number,
        "title": title,
        "theory": ast.get_docstring(etree) or "",
        "drill_intro": _module_doc(drill_path) if drill_path.exists() else "",
        "functions": functions,
        "ethalon_source": esrc,
        "drill_source": dsrc,
    }


def _module_doc(path):
    return ast.get_docstring(ast.parse(path.read_text(encoding="utf-8"))) or ""


def discover():
    blocks = []
    root = PART / "ethalons"
    if not root.exists():
        return blocks

    for bdir in sorted(p for p in root.iterdir() if p.is_dir()):
        items = []
        for f in sorted(bdir.glob("*-ethalon.py")):
            t = load_template(bdir.name, f.name[: -len("-ethalon.py")])
            if t:
                items.append({
                    "id": t["id"],
                    "name": t["name"],
                    "number": t["number"],
                    "title": t["title"],
                    "functions": [fn["name"] for fn in t["functions"]],
                })
        items.sort(key=lambda x: x["number"])
        if items:
            blocks.append({"block": bdir.name, "templates": items})
    return blocks


# ---------------------------------------------------------------------------
# отчёт по кейсам, как на LeetCode
# ---------------------------------------------------------------------------

# Кладётся в начало собранного файла. Каждый assert теста превращается
# в _DRILL.case(...): упавший кейс не обрывает прогон, а попадает в отчёт
# со вводом, ответом, ожидаемым и подсказкой. Отчёт — последняя строка stdout.
HARNESS = '''\
# ---- обвязка тренажёра: каждый assert теста — отдельный кейс, прогон не обрывается ----
import io as _io
import json as _json
import sys as _sys
import traceback as _tb
from contextlib import redirect_stdout as _redirect


class _Drill:
    OPS = {
        "==": lambda a, b: a == b, "!=": lambda a, b: a != b,
        "is": lambda a, b: a is b, "is not": lambda a, b: a is not b,
        "in": lambda a, b: a in b, "not in": lambda a, b: a not in b,
        "<": lambda a, b: a < b, "<=": lambda a, b: a <= b,
        ">": lambda a, b: a > b, ">=": lambda a, b: a >= b,
    }

    def __init__(self):
        self.first = self.last = 0
        self.cases = []

    def user_start(self):
        self.first = _sys._getframe(1).f_lineno + 1

    def user_end(self):
        self.last = _sys._getframe(1).f_lineno - 1

    @staticmethod
    def show(value):
        text = repr(value)
        return text if len(text) <= 500 else text[:500] + " …"

    def error(self, exc):
        where = None                       # строка ТВОЕГО кода, где всё упало
        for frame in reversed(_tb.extract_tb(exc.__traceback__)):
            if self.first <= frame.lineno <= self.last:
                where = frame.lineno - self.first + 1
                break
        return {"error": f"{type(exc).__name__}: {exc}"[:500], "where": where}

    def case(self, k, left, right):
        c = self.cases[k - 1]
        c["runs"] += 1
        out, fail = _io.StringIO(), None
        try:
            with _redirect(out):
                got = left()
                want = right() if right is not None else True
            ok = self.OPS[c["op"]](got, want) if c["op"] else bool(got)
            if not ok:
                fail = {"got": self.show(got), "want": self.show(want) if c["op"] else None}
        except Exception as exc:
            fail = self.error(exc)
        if c["stdout"] is None:
            c["stdout"] = out.getvalue()[-2000:]
        if fail is None:
            c["passed"] += 1
        elif c["fail"] is None:            # в цикле показываем первый провал
            fail["stdout"] = out.getvalue()[-2000:]
            c["fail"] = fail

    def run(self, tests):
        report = []
        for fn, plan in tests:
            self.cases = [dict(meta, runs=0, passed=0, fail=None, stdout=None) for meta in plan]
            entry = {"name": fn.__name__, "cases": self.cases, "crash": None}
            out = _io.StringIO()
            try:
                with _redirect(out):
                    fn()
            except Exception as exc:           # упало не в кейсе, а в подготовке теста
                entry["crash"] = dict(self.error(exc), stdout=out.getvalue()[-2000:])
            report.append(entry)
        cases = [c for t in report for c in t["cases"]]
        print("__DRILL_REPORT__" + _json.dumps({
            "tests": report,
            "total": len(cases),
            "passed": sum(1 for c in cases if c["runs"] and c["fail"] is None),
        }, ensure_ascii=False))


_DRILL = _Drill()'''

CMP_OPS = {
    ast.Eq: "==", ast.NotEq: "!=", ast.Is: "is", ast.IsNot: "is not",
    ast.In: "in", ast.NotIn: "not in", ast.Lt: "<", ast.LtE: "<=", ast.Gt: ">", ast.GtE: ">=",
}


def _flat(code):
    """Многострочный ввод — в одну строку, как на LeetCode."""
    code = re.sub(r"\s*\n\s*", " ", code)
    code = re.sub(r"([\[({])\s+", r"\1", code)
    return re.sub(r"\s+([\])}])", r"\1", code)


def _hint(lines, node):
    """Ближайший комментарий над assert-ом и хвостовой на той же строке — там ловушки (!)."""
    block, i = [], node.lineno - 2
    while i >= 1:                                   # строка 0 — сам def
        text = lines[i].strip()
        if text.startswith("#"):
            block.append(text.lstrip("#").strip())
        elif block:
            break
        i -= 1
    block.reverse()

    tail = lines[node.end_lineno - 1].encode()[node.end_col_offset:].decode().strip()
    parts = [" ".join(block)] if block else []
    if tail.startswith("#"):
        parts.append(tail.lstrip("#").strip())
    return " · ".join(parts) or None


def _instrument(test_src):
    """assert-ы теста -> _DRILL.case(...). Возвращает новый исходник и план кейсов."""
    fn = ast.parse(test_src).body[0]
    lines = test_src.split("\n")
    asserts = sorted((n for n in ast.walk(fn) if isinstance(n, ast.Assert)),
                     key=lambda n: (n.lineno, n.col_offset))

    def pos(lineno, col):                           # col у ast — в байтах utf-8
        head = sum(len(line) + 1 for line in lines[:lineno - 1])
        return head + len(lines[lineno - 1].encode()[:col].decode())

    seg = lambda n: ast.get_source_segment(test_src, n)
    plan, edits = [], []
    for k, node in enumerate(asserts, 1):
        t = node.test
        if isinstance(t, ast.Compare) and len(t.ops) == 1 and type(t.ops[0]) in CMP_OPS:
            op, left, right = CMP_OPS[type(t.ops[0])], seg(t.left), seg(t.comparators[0])
            call = f"_DRILL.case({k}, lambda: ({left}), lambda: ({right}))"
        else:
            op, left, right = None, seg(t), None
            call = f"_DRILL.case({k}, lambda: ({left}), None)"
        plan.append({"input": _flat(left), "expect": _flat(right) if right else None,
                     "op": op, "hint": _hint(lines, node)})
        edits.append((pos(node.lineno, node.col_offset),
                      pos(node.end_lineno, node.end_col_offset), call))

    for start, end, call in reversed(edits):
        test_src = test_src[:start] + call + test_src[end:]
    return test_src, plan


# ---------------------------------------------------------------------------
# сборка запускаемого файла
# ---------------------------------------------------------------------------

def compose_parts(block, name, target):
    """
    Разбирает эталон на две половины: то, что идёт до целевой функции,
    и то, что после, вместе с тестами и отчётом по кейсам.
    Готовый файл = prefix + твой код + suffix; твой код начинается
    ровно на строке prefix.count("\\n") + 1.
    """
    ethalon_path = PART / "ethalons" / block / f"{name}-ethalon.py"
    src, tree, _ = collect(ethalon_path)

    targets = [f["name"] for f in load_template(block, name)["functions"]] \
        if target == "__all__" else [target]
    lowered = [t.lower() for t in targets]
    # то, что пишется с нуля вместе с целью, в собранный файл не попадает
    scratch = set(needs_of(target, tree)) if target != "__all__" else set()

    before, after, used_tests = [], [], []
    seen_target = target == "__all__"

    for i, node in enumerate(tree.body):
        if i == 0 and isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
            continue                                   # docstring модуля
        if isinstance(node, ast.Expr):                 # вызовы тестов и print
            continue

        if is_definition(node) and node.name in targets and target != "__all__":
            seen_target = True                         # тут будет код из редактора
            continue

        if is_definition(node) and node.name in scratch:
            continue
        if isinstance(node, ast.Assign) and \
                any(isinstance(t, ast.Name) and t.id in scratch for t in node.targets):
            continue

        if is_test(node):
            if node.name[len("test_"):] in lowered:
                test_src, plan = _instrument(ast.get_source_segment(src, node))
                (after if seen_target else before).append(test_src)
                used_tests.append((node.name, plan))
            continue

        (after if seen_target else before).append(ast.get_source_segment(src, node))

    if used_tests:
        tail = "_DRILL.run([\n" + "".join(
            f"    ({test}, {plan!r}),\n" for test, plan in used_tests) + "])\n"
    else:
        tail = 'print("тестов для этой функции нет")\n'

    join = lambda parts: "\n\n\n".join(x for x in parts if x)
    prefix = join([HARNESS] + before) + \
        "\n\n\n_DRILL.user_start()                       # ниже — твой код\n"
    suffix = "\n_DRILL.user_end()                         # выше — твой код\n\n\n" + \
        join(after + [tail])
    return prefix, suffix


def compose(block, name, target, user_code):
    """Эталон, в котором целевая функция заменена кодом из редактора."""
    prefix, suffix = compose_parts(block, name, target)
    body = user_code.rstrip() + "\n" if target != "__all__" else ""
    return prefix + body + suffix


ANSI = re.compile(r"\x1b\[[0-9;]*m")


def run_code(source):
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False,
                                     encoding="utf-8") as fh:
        fh.write(source)
        tmp = fh.name

    env = os.environ.copy()
    env.update(PYTHON_COLORS="0", NO_COLOR="1", FORCE_COLOR="0", TERM="dumb")

    try:
        proc = subprocess.run([sys.executable, tmp],
                              capture_output=True, text=True, env=env,
                              timeout=RUN_TIMEOUT, cwd=tempfile.gettempdir())
        out, err, code = proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired:
        out, err, code = "", (f"Таймаут: код не уложился в {RUN_TIMEOUT} с.\n"
                              "Скорее всего бесконечный цикл или забытый сдвиг "
                              "указателя."), -1
    finally:
        Path(tmp).unlink(missing_ok=True)

    err = ANSI.sub("", err).replace(tmp, "твой код")
    out = ANSI.sub("", out)
    return {"ok": code == 0, "stdout": out, "stderr": err, "source": source}


# ---------------------------------------------------------------------------
# http
# ---------------------------------------------------------------------------

class Handler(BaseHTTPRequestHandler):
    server_version = "algodrill"

    def log_message(self, fmt, *args):
        sys.stderr.write("  %s\n" % (fmt % args))

    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        data = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _json(self, obj, code=200):
        self._send(code, json.dumps(obj, ensure_ascii=False))

    def do_GET(self):
        path = self.path.split("?")[0]

        if path in ("/", "/index.html"):
            return self._send(200, (WEB / "index.html").read_bytes(),
                              "text/html; charset=utf-8")

        if path == "/api/templates":
            return self._json({"blocks": discover()})

        if path.startswith("/api/template/"):
            parts = path[len("/api/template/"):].split("/")
            if len(parts) != 2:
                return self._json({"error": "плохой путь"}, 400)
            t = load_template(parts[0], parts[1])
            if t is None:
                return self._json({"error": "шаблон не найден"}, 404)
            return self._json(t)

        return self._json({"error": "не найдено"}, 404)

    def do_POST(self):
        if self.path != "/api/run":
            return self._json({"error": "не найдено"}, 404)

        length = int(self.headers.get("Content-Length") or 0)
        if length > MAX_BODY:
            return self._json({"error": "слишком большой запрос"}, 413)

        try:
            req = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            return self._json({"error": "невалидный json"}, 400)

        block = req.get("block", "")
        name = req.get("name", "")
        target = req.get("target", "")
        code = req.get("code", "")

        if not (PART / "ethalons" / block / f"{name}-ethalon.py").exists():
            return self._json({"error": "шаблон не найден"}, 404)

        try:
            prefix, suffix = compose_parts(block, name, target)
        except SyntaxError as e:
            return self._json({
                "ok": False, "stdout": "",
                "stderr": f"SyntaxError: {e.msg} (строка {e.lineno})",
                "source": code,
            })

        body = code.rstrip() + "\n" if target != "__all__" else ""
        result = run_code(prefix + body + suffix)
        result["user_start"] = prefix.count("\n") + 1     # чтобы перевести номера строк в твои
        return self._json(result)


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    server = HTTPServer(("127.0.0.1", port), Handler)
    print(f"тренажёр: http://127.0.0.1:{port}")
    print(f"шаблоны:  {PART}")
    print("Ctrl+C — остановить")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nостановлен")


if __name__ == "__main__":
    main()
