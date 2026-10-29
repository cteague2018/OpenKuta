"""Pytest bootstrap: keep run-time state out of the source tree.

``ClassroomStore`` persists classrooms and submissions as JSON files in
``backend/app/data``. Both files are tracked by git, so without a redirect every test
run appends fixture rows and leaves the working tree dirty.

This module runs before any test module (and therefore before the API's module-level
``ClassroomStore`` instances are created), points ``OPENKUTA_DATA_DIR`` at a throwaway
directory and removes it when the session ends. A CI-provided ``OPENKUTA_DATA_DIR``
still wins, and the store seeds the same default class it would create on a fresh
checkout.
"""

from __future__ import annotations

import atexit
import os
import pathlib
import shutil
import tempfile

_TEMP_DATA_DIR = pathlib.Path(tempfile.mkdtemp(prefix="openkuta-test-data-"))
os.environ.setdefault("OPENKUTA_DATA_DIR", str(_TEMP_DATA_DIR))
atexit.register(shutil.rmtree, _TEMP_DATA_DIR, True)
