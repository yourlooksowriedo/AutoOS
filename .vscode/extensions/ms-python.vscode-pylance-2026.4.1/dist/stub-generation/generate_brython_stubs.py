"""Generate type stubs for Brython's browser-only modules."""

from __future__ import annotations

import argparse
import ast
import re
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Iterable, Sequence
from pathlib import Path

BRYTHON_VERSION = "3.14.3"
BRYTHON_REVISION = "a0ffdd8dfd9725604439c0f35d64c4adff0d6292"
GENERATED_HEADER = f"""\
# Generated from Brython {BRYTHON_VERSION} ({BRYTHON_REVISION}).
# Regenerate with packages/pylance-internal/stub-generation/generate_brython_stubs.py.
# pyright: reportIncompatibleMethodOverride=false

"""

CORE_BROWSER_STUB = """\
from collections.abc import Callable, Iterable
from typing import Any, Protocol, TypeVar

_T = TypeVar("_T")

class DOMEvent:
    target: DOMNode
    currentTarget: DOMNode
    type: str
    def preventDefault(self) -> None: ...
    def stopPropagation(self) -> None: ...

class DOMNode:
    attrs: dict[str, Any]
    children: list[DOMNode]
    class_name: str
    html: str
    id: str
    parent: DOMNode | None
    style: Any
    text: str
    value: Any
    def __getitem__(self, key: str | int) -> DOMNode: ...
    def __iter__(self) -> Iterable[DOMNode]: ...
    def __le__(
        self,
        other: DOMNode | str | int | float | Iterable[DOMNode | str | int | float],
    ) -> DOMNode: ...
    def __len__(self) -> int: ...
    def bind(
        self,
        event: str,
        callback: Callable[[DOMEvent], object],
        options: bool | dict[str, Any] | None = ...,
    ) -> None: ...
    def clear(self) -> None: ...
    def clone(self) -> DOMNode: ...
    def closest(self, selector: str) -> DOMNode | None: ...
    def focus(self) -> None: ...
    def get(self, selector: str | None = ...) -> list[DOMNode]: ...
    def remove(self, child: DOMNode | None = ...) -> None: ...
    def select(self, selector: str) -> list[DOMNode]: ...
    def unbind(
        self,
        event: str,
        callback: Callable[[DOMEvent], object] | None = ...,
    ) -> None: ...

class Window(Protocol):
    document: DOMNode
    def addEventListener(
        self,
        event: str,
        callback: Callable[[DOMEvent], object],
        options: bool | dict[str, Any] | None = ...,
    ) -> None: ...
    def alert(self, message: object = ...) -> None: ...
    def confirm(self, message: str = ...) -> bool: ...
    def setInterval(self, callback: Callable[[], object], milliseconds: int) -> int: ...
    def setTimeout(self, callback: Callable[[], object], milliseconds: int) -> int: ...

__BRYTHON__: Any
console: Any
document: DOMNode
doc: DOMNode
is_webworker: bool
scope: Any
self: Window
win: Window
window: Window

def alert(message: object = ...) -> None: ...
def bind(
    elt: DOMNode | str | Iterable[DOMNode],
    evt: str,
    options: bool | dict[str, Any] | None = ...,
) -> Callable[[_T], _T]: ...
def confirm(message: str = ...) -> bool: ...
def load(script_url: str) -> None: ...
def run_script(src: str, name: str = ...) -> None: ...
"""

JAVASCRIPT_STUB = """\
from typing import Any

class JSObject:
    def __getattr__(self, name: str) -> Any: ...
    def __getitem__(self, key: str | int) -> Any: ...
    def __setitem__(self, key: str | int, value: object) -> None: ...

class UndefinedType:
    def __bool__(self) -> bool: ...

NULL: None
UNDEFINED: UndefinedType

def JSONStringify(obj: object, replacer: object = ..., space: object = ...) -> str: ...
def JSConstructor(constructor: JSObject) -> type[JSObject]: ...
def load(url: str) -> None: ...
def py2js(src: str, module_name: str = ...) -> str: ...
def this() -> JSObject: ...
"""

AIO_STUB = """\
from collections.abc import Awaitable, Callable, Coroutine
from typing import Any, Generic, TypeVar

_T = TypeVar("_T")

class Future(Awaitable[_T], Generic[_T]):
    def done(self) -> bool: ...
    def set_exception(self, exception: BaseException) -> None: ...
    def set_result(self, value: _T) -> None: ...

async def ajax(method: str, url: str, **kwargs: Any) -> Any: ...
async def event(element: object, *names: str) -> Any: ...
async def get(url: str, **kwargs: Any) -> Any: ...
def iscoroutine(f: object) -> bool: ...
def iscoroutinefunction(f: object) -> bool: ...
async def post(url: str, **kwargs: Any) -> Any: ...
def run(
    coro: Coroutine[Any, Any, _T],
    onsuccess: Callable[[_T], object] = ...,
    onerror: Callable[[BaseException], object] = ...,
) -> None: ...
async def sleep(seconds: float) -> None: ...
"""

AJAX_STUB = """\
from collections.abc import Callable, Mapping
from typing import Any

class ajax:
    json: Any
    responseType: str
    text: str
    url: str
    withCredentials: bool
    xml: Any
    def bind(self, event: str, callback: Callable[[ajax], object]) -> None: ...
    def open(self, method: str, url: str, async_: bool = ...) -> None: ...
    def read(self) -> str | bytes | Any: ...
    def send(self, params: str | Mapping[str, object] | Any = ...) -> None: ...
    def set_header(self, key: str, value: str) -> None: ...
    def set_timeout(self, seconds: float, callback: Callable[[], object]) -> None: ...

Ajax = ajax

def connect(url: str, blocking: bool = ..., **kwargs: Any) -> None: ...
def file_upload(url: str, file: Any, method: str = ..., **callbacks: Callable[[ajax], object]) -> None: ...
def form_data(form: object = ...) -> Any: ...
def get(url: str, blocking: bool = ..., **kwargs: Any) -> None: ...
def head(url: str, blocking: bool = ..., **kwargs: Any) -> None: ...
def options(url: str, blocking: bool = ..., **kwargs: Any) -> None: ...
def patch(url: str, blocking: bool = ..., **kwargs: Any) -> None: ...
def post(url: str, blocking: bool = ..., **kwargs: Any) -> None: ...
def put(url: str, blocking: bool = ..., **kwargs: Any) -> None: ...
def trace(url: str, blocking: bool = ..., **kwargs: Any) -> None: ...
"""

WEBCOMPONENT_STUB = """\
from typing import Any

from . import DOMNode

def define(
    tag_name: str,
    cls: type[DOMNode],
    options: dict[str, Any] | None = ...,
) -> None: ...
def get(name: str) -> type[DOMNode] | None: ...
"""

WORKER_STUB = """\
from collections.abc import Callable
from typing import Any

class Worker:
    def __init__(
        self,
        id: str,
        onmessage: Callable[[object], object] | None = ...,
        onerror: Callable[[BaseException], object] | None = ...,
    ) -> None: ...
    def send(self, message: object, *args: object) -> Any: ...

def create_worker(
    id: str,
    onready: Callable[[Worker], object] | None = ...,
    onmessage: Callable[[object], object] | None = ...,
    onerror: Callable[[BaseException], object] | None = ...,
) -> None: ...
"""

README = f"""\
# Brython stubs

These stubs describe Brython's browser-only Python APIs. Pylance makes them
available only to Python virtual documents extracted from Brython HTML scripts.

The generated surface is based on Brython {BRYTHON_VERSION}, revision
`{BRYTHON_REVISION}`. `browser/__init__.pyi`, `browser/html.pyi`,
`browser/aio.pyi`, `browser/ajax.pyi`, `browser/svg.pyi`,
`browser/webcomponent.pyi`, `browser/worker.pyi`, and `javascript.pyi` contain
curated types for APIs that Brython creates dynamically in JavaScript. The
remaining `browser` modules are generated structurally from Brython's Python
source.

See `LICENCE.txt` for Brython's BSD 3-Clause license.
"""


def _annotation(annotation: ast.expr | None, *, default: str = "Any") -> str:
    return ast.unparse(annotation) if annotation is not None else default


def _format_arg(
    arg: ast.arg, default: ast.expr | None, *, annotate: bool = True
) -> str:
    name = arg.arg
    if annotate:
        name += f": {_annotation(arg.annotation)}"
    if default is not None:
        name += " = ..."
    return name


def _format_arguments(arguments: ast.arguments) -> str:
    parts: list[str] = []
    positional = [*arguments.posonlyargs, *arguments.args]
    defaults: list[ast.expr | None] = [None] * (
        len(positional) - len(arguments.defaults)
    ) + list(arguments.defaults)

    for index, (arg, default) in enumerate(zip(positional, defaults)):
        parts.append(_format_arg(arg, default, annotate=arg.arg not in {"self", "cls"}))
        if arguments.posonlyargs and index + 1 == len(arguments.posonlyargs):
            parts.append("/")

    if arguments.vararg is not None:
        parts.append(f"*{_format_arg(arguments.vararg, None)}")
    elif arguments.kwonlyargs:
        parts.append("*")

    for arg, default in zip(arguments.kwonlyargs, arguments.kw_defaults):
        parts.append(_format_arg(arg, default))

    if arguments.kwarg is not None:
        parts.append(f"**{_format_arg(arguments.kwarg, None)}")

    return ", ".join(parts)


def _return_annotation(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    if node.returns is not None:
        return ast.unparse(node.returns)
    if node.name == "__init__":
        return "None"
    if node.name in {"__bool__", "__contains__", "__eq__", "__ne__"}:
        return "bool"
    if node.name in {"__len__", "__index__", "__hash__"}:
        return "int"
    return "Any"


def _decorators(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
    supported = {"abstractmethod", "classmethod", "property", "staticmethod"}
    return [
        f"@{text}"
        for decorator in node.decorator_list
        if (text := ast.unparse(decorator)).split(".")[-1] in supported
        or text.endswith(".setter")
    ]


def _assignment(node: ast.Assign | ast.AnnAssign) -> str | None:
    if isinstance(node, ast.AnnAssign):
        if not isinstance(node.target, ast.Name) or node.target.id.startswith("_"):
            return None
        return f"{node.target.id}: {_annotation(node.annotation)}"

    if len(node.targets) != 1 or not isinstance(node.targets[0], ast.Name):
        return None
    name = node.targets[0].id
    if name.startswith("_"):
        return None
    value = node.value
    if isinstance(value, ast.Constant):
        inferred = type(value.value).__name__ if value.value is not None else "None"
    elif isinstance(value, (ast.List, ast.ListComp)):
        inferred = "list[Any]"
    elif isinstance(value, (ast.Dict, ast.DictComp)):
        inferred = "dict[Any, Any]"
    elif isinstance(value, (ast.Set, ast.SetComp)):
        inferred = "set[Any]"
    elif isinstance(value, (ast.Tuple, ast.GeneratorExp)):
        inferred = "tuple[Any, ...]"
    else:
        inferred = "Any"
    return f"{name}: {inferred}"


def _public_nodes(nodes: Iterable[ast.stmt]) -> list[ast.stmt]:
    result: list[ast.stmt] = []
    seen: set[tuple[type[ast.stmt], str]] = set()

    def add(node: ast.stmt) -> None:
        if isinstance(node, ast.If):
            for child in [*node.body, *node.orelse]:
                add(child)
            return
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name.startswith("_") and not node.name.startswith("__"):
                return
            key = (type(node), node.name)
        elif isinstance(node, ast.ClassDef):
            key = (type(node), node.name)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            key = (type(node), node.target.id)
        elif (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
        ):
            key = (type(node), node.targets[0].id)
        else:
            return
        if key not in seen:
            seen.add(key)
            result.append(node)

    for node in nodes:
        add(node)
    return result


def _render_function(
    node: ast.FunctionDef | ast.AsyncFunctionDef, indent: str = ""
) -> list[str]:
    lines = [f"{indent}{decorator}" for decorator in _decorators(node)]
    prefix = "async " if isinstance(node, ast.AsyncFunctionDef) else ""
    lines.append(
        f"{indent}{prefix}def {node.name}({_format_arguments(node.args)}) -> {_return_annotation(node)}: ..."
    )
    return lines


def _render_class(node: ast.ClassDef) -> list[str]:
    bases = [ast.unparse(base) for base in node.bases]
    bases.extend(ast.unparse(keyword) for keyword in node.keywords)
    suffix = f"({', '.join(bases)})" if bases else ""
    lines = [f"class {node.name}{suffix}:"]
    members: list[str] = []
    for child in _public_nodes(node.body):
        if isinstance(child, (ast.Assign, ast.AnnAssign)):
            if assignment := _assignment(child):
                members.append(f"    {assignment}")
        elif isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
            members.extend(_render_function(child, "    "))
        elif isinstance(child, ast.ClassDef):
            members.extend(f"    {line}" for line in _render_class(child))
    lines.extend(members or ["    ..."])
    return lines


def generate_python_stub(source: str) -> str:
    tree = ast.parse(source)
    imports: list[str] = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            imports.append(ast.unparse(node))
        elif isinstance(node, ast.ImportFrom) and (
            node.level > 0 or all(alias.name != "*" for alias in node.names)
        ):
            imports.append(ast.unparse(node))

    lines = ["from __future__ import annotations", "from typing import Any"]
    lines.extend(dict.fromkeys(imports))

    definitions: list[str] = []
    public_nodes = _public_nodes(tree.body)
    declared_names = {
        node.name
        for node in public_nodes
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
    }
    for node in public_nodes:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            assignment_name = (
                node.target.id
                if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name)
                else (
                    node.targets[0].id
                    if isinstance(node, ast.Assign)
                    and len(node.targets) == 1
                    and isinstance(node.targets[0], ast.Name)
                    else None
                )
            )
            if assignment_name not in declared_names and (
                assignment := _assignment(node)
            ):
                definitions.append(assignment)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            definitions.extend(_render_function(node))
        elif isinstance(node, ast.ClassDef):
            definitions.extend(_render_class(node))
        definitions.append("")

    return (
        GENERATED_HEADER
        + "\n".join(lines)
        + "\n\n"
        + "\n".join(definitions).rstrip()
        + "\n"
    )


def _extract_tags(builtin_modules: str) -> list[str]:
    match = re.search(
        r"var tags = \[(?P<body>.*?)\]\s*// Object representing the module browser\.html",
        builtin_modules,
        re.DOTALL,
    )
    if match is None:
        raise ValueError("Could not find Brython's browser.html tag list")
    tags = re.findall(r"['\"]([A-Za-z][A-Za-z0-9]*)['\"]", match.group("body"))
    if len(tags) < 100 or "A" not in tags or "BUTTON" not in tags:
        raise ValueError(
            "Brython's browser.html tag list does not have the expected shape"
        )
    return tags


def _extract_svg_tags(svg_module: str) -> list[str]:
    match = re.search(
        r"var \$svg_tags = \[(?P<body>.*?)\]\s*// create classes", svg_module, re.DOTALL
    )
    if match is None:
        raise ValueError("Could not find Brython's browser.svg tag list")
    tags = re.findall(r"'([A-Za-z][A-Za-z0-9_]*)'", match.group("body"))
    if len(tags) < 30 or "circle" not in tags or "svg" not in tags:
        raise ValueError(
            "Brython's browser.svg tag list does not have the expected shape"
        )
    return tags


def _generate_tag_stub(tags: Sequence[str], module_name: str) -> str:
    definitions = "\n".join(
        f"class {tag}(_Tag):\n    def __init__(self, *children: object, **attrs: object) -> None: ..."
        for tag in tags
    )
    return (
        GENERATED_HEADER
        + """\
from typing import Any

from . import DOMNode

class _Tag(DOMNode):
    def __init__(self, *children: object, **attrs: object) -> None: ...

tags: dict[str, type[_Tag]]

"""
        + (
            "def maketag(tag_name: str, component_class: type[Any] | None = ...) -> type[_Tag]: ...\n\n"
            if module_name == "html"
            else ""
        )
        + definitions
        + "\n"
    )


def build_outputs(source_root: Path) -> dict[Path, str]:
    version_info = source_root / "www" / "src" / "version_info.js"
    builtin_modules = source_root / "www" / "src" / "builtin_modules.js"
    browser_root = source_root / "www" / "src" / "Lib" / "browser"
    ajax_module = source_root / "www" / "src" / "libs" / "_ajax.js"
    svg_module = source_root / "www" / "src" / "libs" / "_svg.js"
    webcomponent_module = source_root / "www" / "src" / "libs" / "_webcomponent.js"
    worker_module = source_root / "www" / "src" / "libs" / "_webworker.js"
    license_file = source_root / "LICENCE.txt"
    required = [
        version_info,
        builtin_modules,
        browser_root,
        ajax_module,
        svg_module,
        webcomponent_module,
        worker_module,
        license_file,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(
            f"Brython source checkout is missing: {', '.join(missing)}"
        )

    version_text = version_info.read_text(encoding="utf-8")
    if f"implementation = [{BRYTHON_VERSION.replace('.', ', ')}" not in version_text:
        raise ValueError(f"Expected Brython {BRYTHON_VERSION} source")

    builtin_modules_text = builtin_modules.read_text(encoding="utf-8")
    ajax_module_text = ajax_module.read_text(encoding="utf-8")
    svg_module_text = svg_module.read_text(encoding="utf-8")
    webcomponent_module_text = webcomponent_module.read_text(encoding="utf-8")
    worker_module_text = worker_module.read_text(encoding="utf-8")
    if "var ajax = $B.make_type('ajax')" not in ajax_module_text:
        raise ValueError(
            "Brython's browser.ajax module does not have the expected shape"
        )
    if "function define(tag_name, cls, options)" not in webcomponent_module_text:
        raise ValueError(
            "Brython's browser.webcomponent module does not have the expected shape"
        )
    if 'var wclass = $B.make_type("Worker")' not in worker_module_text:
        raise ValueError(
            "Brython's browser.worker module does not have the expected shape"
        )

    outputs: dict[Path, str] = {
        Path("browser/__init__.pyi"): GENERATED_HEADER + CORE_BROWSER_STUB,
        Path("browser/aio.pyi"): GENERATED_HEADER + AIO_STUB,
        Path("browser/ajax.pyi"): GENERATED_HEADER + AJAX_STUB,
        Path("browser/html.pyi"): _generate_tag_stub(
            _extract_tags(builtin_modules_text), "html"
        ),
        Path("browser/svg.pyi"): _generate_tag_stub(
            _extract_svg_tags(svg_module_text), "svg"
        ),
        Path("browser/webcomponent.pyi"): GENERATED_HEADER + WEBCOMPONENT_STUB,
        Path("browser/worker.pyi"): GENERATED_HEADER + WORKER_STUB,
        Path("javascript.pyi"): GENERATED_HEADER + JAVASCRIPT_STUB,
        Path("README.md"): README,
        Path("LICENCE.txt"): license_file.read_text(encoding="utf-8"),
    }

    curated_modules = {
        "__init__.py",
        "aio.py",
        "ajax.py",
        "html.py",
        "svg.py",
        "webcomponent.py",
        "worker.py",
    }
    for source_path in sorted(browser_root.rglob("*.py")):
        relative = source_path.relative_to(browser_root)
        if relative.as_posix() in curated_modules:
            continue
        output_path = Path("browser") / relative.with_suffix(".pyi")
        outputs[output_path] = generate_python_stub(
            source_path.read_text(encoding="utf-8")
        )
    return outputs


def _get_source_revision(source_root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(source_root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        raise ValueError("Expected --source to be a Brython Git checkout") from error
    return result.stdout.strip()


def _validate_source_revision(source_root: Path) -> None:
    actual_revision = _get_source_revision(source_root)
    if actual_revision != BRYTHON_REVISION:
        raise ValueError(
            f"Expected Brython revision {BRYTHON_REVISION}, got {actual_revision}"
        )


def _directory_contents(root: Path) -> dict[Path, str]:
    if not root.exists():
        return {}
    return {
        path.relative_to(root): path.read_text(encoding="utf-8")
        for path in root.rglob("*")
        if path.is_file()
    }


def write_outputs(outputs: dict[Path, str], output_root: Path, *, check: bool) -> bool:
    actual = _directory_contents(output_root)
    if check:
        return actual == outputs

    output_root.mkdir(parents=True, exist_ok=True)
    for stale_path in actual.keys() - outputs.keys():
        (output_root / stale_path).unlink()
    for relative, content in outputs.items():
        target = output_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")
    for directory in sorted(
        (path for path in output_root.rglob("*") if path.is_dir()),
        key=lambda path: len(path.parts),
        reverse=True,
    ):
        if not any(directory.iterdir()):
            directory.rmdir()
    return True


def _download_source() -> Path:
    temp_root = Path(tempfile.mkdtemp(prefix="brython-stubs-"))
    archive = temp_root / "brython.zip"
    url = f"https://github.com/brython-dev/brython/archive/{BRYTHON_REVISION}.zip"
    import urllib.request

    urllib.request.urlretrieve(url, archive)
    shutil.unpack_archive(archive, temp_root)
    return next(path for path in temp_root.iterdir() if path.is_dir())


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, help="Path to a Brython source checkout")
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Directory that receives generated stubs",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if the checked-in output is out of date",
    )
    args = parser.parse_args(argv)

    downloaded_root: Path | None = None
    try:
        source_root = args.source
        if source_root is None:
            downloaded_root = _download_source()
            source_root = downloaded_root
        else:
            _validate_source_revision(source_root)
        outputs = build_outputs(source_root)
        if not write_outputs(outputs, args.output, check=args.check):
            print("Brython stubs are out of date", file=sys.stderr)
            return 1
        return 0
    finally:
        if downloaded_root is not None:
            shutil.rmtree(downloaded_root.parent)


if __name__ == "__main__":
    raise SystemExit(main())
