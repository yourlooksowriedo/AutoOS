# Generated from Brython 3.14.3 (a0ffdd8dfd9725604439c0f35d64c4adff0d6292).
# Regenerate with packages/pylance-internal/stub-generation/generate_brython_stubs.py.
# pyright: reportIncompatibleMethodOverride=false

from __future__ import annotations
from typing import Any
import sys
from browser import window
from .local_storage import LocalStorage

has_session_storage: Any

class SessionStorage(LocalStorage):
    storage_type: str
    def __init__(self) -> None: ...

storage: Any
