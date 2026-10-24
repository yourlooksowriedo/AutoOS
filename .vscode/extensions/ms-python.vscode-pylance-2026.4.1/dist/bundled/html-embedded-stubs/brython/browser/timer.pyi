# Generated from Brython 3.14.3 (a0ffdd8dfd9725604439c0f35d64c4adff0d6292).
# Regenerate with packages/pylance-internal/stub-generation/generate_brython_stubs.py.
# pyright: reportIncompatibleMethodOverride=false

from __future__ import annotations
from typing import Any
from browser import self as window

clear_interval: Any

clear_timeout: Any

def set_interval(func: Any, interval: Any, *args: Any) -> Any: ...

def set_timeout(func: Any, interval: Any, *args: Any) -> Any: ...

def request_animation_frame(func: Any) -> Any: ...

def cancel_animation_frame(int_id: Any) -> Any: ...

def set_loop_timeout(x: Any) -> Any: ...
