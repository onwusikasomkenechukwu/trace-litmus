"""Repo-root import shim for `python -m tracelitmus.cli` before installation."""

from pathlib import Path

_SRC_PACKAGE = Path(__file__).resolve().parents[1] / "src" / "tracelitmus"
__path__ = [str(_SRC_PACKAGE)]

_init_file = _SRC_PACKAGE / "__init__.py"
if _init_file.exists():
    exec(_init_file.read_text(encoding="utf-8"))
