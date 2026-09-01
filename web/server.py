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

HELPERS = {"TreeNode", "build", "is_valid_order", "norm_sets", "norm_seqs"}

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


def is_stub(node):
    """
    В дрилле цель — это функция с телом pass. Всё, что написано целиком
    (TreeNode, build, is_valid_order, norm_sets), — вспомогательное
    и дриллить его не надо.
    """
    if isinstance(node, ast.ClassDef):
        methods = [b for b in node.body if isinstance(b, ast.FunctionDef)]
        return any(is_stub(m) for m in methods)

    body = [b for b in node.body
            if not (isinstance(b, ast.Expr) and isinstance(b.value, ast.Constant))]
    return len(body) == 1 and isinstance(body[0], ast.Pass)


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

    functions = []
    for fname, d in edefs.items():
        if fname.startswith("test_"):
            continue
        drill = ddefs.get(fname)
        if drill is not None and not is_stub(drill["node"]):
            continue                                   # вспомогательный код
        if drill is None and fname in HELPERS:
            continue
        functions.append({
            "name": fname,
            "kind": "class" if isinstance(d["node"], ast.ClassDef) else "function",
            "doc": d["doc"],
            "code": d["code"],
            "task": (drill or {}).get("doc") or d["doc"],
            "stub": stub_of((drill or d)["node"], dsrc if drill else esrc),
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
# сборка запускаемого файла
# ---------------------------------------------------------------------------

def compose(block, name, target, user_code):
    """
    Эталон, в котором целевая функция заменена кодом из редактора,
    плюс вызов её тестов. Всё остальное берётся из эталона рабочим —
    дриллим одну функцию, не спотыкаясь об остальные.
    """
    ethalon_path = PART / "ethalons" / block / f"{name}-ethalon.py"
    src, tree, _ = collect(ethalon_path)

    targets = [f["name"] for f in load_template(block, name)["functions"]] \
        if target == "__all__" else [target]

    chunks = []
    used_tests = []
    replaced = set()

    for i, node in enumerate(tree.body):
        if i == 0 and isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
            continue                                   # docstring модуля
        if isinstance(node, ast.Expr):                 # вызовы тестов и print
            continue
        if is_definition(node) and node.name in targets:
            if target != "__all__":
                chunks.append(user_code.rstrip() + "\n")
                replaced.add(node.name)
                continue
        if is_test(node):
            if node.name[len("test_"):] in [t.lower() for t in targets]:
                chunks.append(ast.get_source_segment(src, node))
                used_tests.append(node.name)
            continue
        chunks.append(ast.get_source_segment(src, node))

    if target != "__all__" and target not in replaced:
        chunks.insert(0, user_code.rstrip() + "\n")

    body = "\n\n\n".join(c for c in chunks if c)
    calls = "\n".join(f"{t}()" for t in used_tests)
    tail = f'\n\n\n{calls}\nprint("ok — тесты прошли")\n' if calls else \
           '\n\nprint("тестов для этой функции нет")\n'
    return body + tail


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
            source = compose(block, name, target, code)
        except SyntaxError as e:
            return self._json({
                "ok": False, "stdout": "",
                "stderr": f"SyntaxError: {e.msg} (строка {e.lineno})",
                "source": code,
            })

        return self._json(run_code(source))


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
