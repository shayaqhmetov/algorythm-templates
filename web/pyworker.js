/*
 * Гоняет тесты питоном в браузере — нужен статической версии на GitHub Pages,
 * где ответить на /api/run некому.
 *
 * Живёт в воркере по одной причине: бесконечный цикл в дрилле — обычное дело,
 * а прервать его иначе нельзя. Главный поток просто убивает воркер по таймауту.
 */

const PYODIDE = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/";

/* запускаем код питоном же — тогда трейсбек получается такой, как в консоли,
   без кадров самого pyodide: tb_next отрезает кадр этой обёртки */
const RUNNER = `
import traceback

def __run(src):
    ns = {"__name__": "__main__"}
    try:
        exec(compile(src, "твой код", "exec"), ns)
    except BaseException as e:
        tb = e.__traceback__.tb_next or e.__traceback__
        return "".join(traceback.format_exception(type(e), e, tb))
    return ""
`;

let booting = null;

async function boot() {
  importScripts(PYODIDE + "pyodide.js");
  const py = await loadPyodide({ indexURL: PYODIDE });
  py.runPython(RUNNER);
  return py;
}

self.onmessage = async ({ data }) => {
  let out = "";
  try {
    booting = booting || boot();
    const py = await booting;

    py.setStdout({ batched: s => { out += s + "\n"; } });
    py.setStderr({ batched: s => { out += s + "\n"; } });

    const trace = py.globals.get("__run")(data.source);
    postMessage({ ok: !trace, stdout: out, stderr: trace || "" });
  } catch (e) {
    postMessage({ ok: false, stdout: out, stderr: (e && e.message) || String(e) });
  }
};
