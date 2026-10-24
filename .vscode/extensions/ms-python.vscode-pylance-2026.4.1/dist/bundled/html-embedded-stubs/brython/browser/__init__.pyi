# Generated from Brython 3.14.3 (a0ffdd8dfd9725604439c0f35d64c4adff0d6292).
# Regenerate with packages/pylance-internal/stub-generation/generate_brython_stubs.py.
# pyright: reportIncompatibleMethodOverride=false

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
