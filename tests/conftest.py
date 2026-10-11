import os
import sys
import tempfile
from pathlib import Path

# Same free, deterministic setup as api/tests/conftest.py. Set before any import.
os.environ["TRIAGE_BACKEND"] = "stub"
os.environ["LOG_DIR"] = tempfile.mkdtemp(prefix="afyaplus-test-logs-")
os.environ["JWT_SECRET"] = "test-secret-" + "x" * 40
os.environ["REDIS_URL"] = ""
ROOT = Path(__file__).resolve().parent.parent
for sub in ("api", "levers", "cost", "deploy"):
    sys.path.insert(0, str(ROOT / sub))

import pytest  # noqa: E402

import response_cache  # noqa: E402


@pytest.fixture(autouse=True)
def fresh_cache():
    response_cache.reset()
    yield
    response_cache.reset()
