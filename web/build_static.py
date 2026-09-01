#!/usr/bin/env python3
"""
Собирает статическую версию тренажёра для GitHub Pages.

    python3 web/build_static.py           # -> docs/
    python3 web/build_static.py out/      # другая папка

Сервера на Pages нет, поэтому всё, что обычно отдают ручки /api/*,
запекается в JSON, а тесты в браузере гоняет python, собранный в wasm
(Pyodide). Разбор .py файлов остаётся здесь, в сборке, — в браузер
уезжает только результат.
"""

import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import server                                        # noqa: E402

WEB = Path(__file__).resolve().parent
ROOT = WEB.parent


def build(out: Path):
    data = out / "data"
    if out.exists():
        shutil.rmtree(out)
    data.mkdir(parents=True)

    blocks = server.discover()
    (data / "templates.json").write_text(
        json.dumps({"blocks": blocks}, ensure_ascii=False), encoding="utf-8")

    count = 0
    for block in blocks:
        for item in block["templates"]:
            b, name = item["id"].split("/")
            tpl = server.load_template(b, name)

            # то, что сервер считает на лету в /api/run
            tpl["run"] = {}
            for fn in tpl["functions"]:
                prefix, suffix = server.compose_parts(b, name, fn["name"])
                tpl["run"][fn["name"]] = {"prefix": prefix, "suffix": suffix}

            (data / f"{b}__{name}.json").write_text(
                json.dumps(tpl, ensure_ascii=False), encoding="utf-8")
            count += 1

    shutil.copy(WEB / "index.html", out / "index.html")
    shutil.copy(WEB / "pyworker.js", out / "pyworker.js")
    (out / ".nojekyll").touch()                       # иначе Jekyll съест служебные файлы

    size = sum(f.stat().st_size for f in out.rglob("*") if f.is_file())
    print(f"{out}: {count} шаблонов, {size / 1024:.0f} КБ")


if __name__ == "__main__":
    build(ROOT / (sys.argv[1] if len(sys.argv) > 1 else "docs"))
