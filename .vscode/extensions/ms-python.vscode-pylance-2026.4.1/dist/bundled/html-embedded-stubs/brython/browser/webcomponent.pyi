# Generated from Brython 3.14.3 (a0ffdd8dfd9725604439c0f35d64c4adff0d6292).
# Regenerate with packages/pylance-internal/stub-generation/generate_brython_stubs.py.
# pyright: reportIncompatibleMethodOverride=false

from typing import Any

from . import DOMNode

def define(
    tag_name: str,
    cls: type[DOMNode],
    options: dict[str, Any] | None = ...,
) -> None: ...
def get(name: str) -> type[DOMNode] | None: ...
