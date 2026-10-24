# Generated from Brython 3.14.3 (a0ffdd8dfd9725604439c0f35d64c4adff0d6292).
# Regenerate with packages/pylance-internal/stub-generation/generate_brython_stubs.py.
# pyright: reportIncompatibleMethodOverride=false

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
