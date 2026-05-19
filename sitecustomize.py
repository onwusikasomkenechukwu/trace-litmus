"""Make the src layout importable for repo-root `python -m` smoke tests."""

from pathlib import Path
import sys

SRC = Path(__file__).resolve().parent / "src"
if SRC.exists():
    sys.path.insert(0, str(SRC))
