import os
import sys
import tempfile
from pathlib import Path

# Free, deterministic runs: stub model, throwaway logs, known secret. Set before any import.
os.environ["TRIAGE_BACKEND"] = "stub"
os.environ["LOG_DIR"] = tempfile.mkdtemp(prefix="afyaplus-test-logs-")
os.environ["JWT_SECRET"] = "test-secret-" + "x" * 40
os.environ["REDIS_URL"] = ""              # tests use the in-process cache
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest  # noqa: E402

import rate_limit  # noqa: E402
import response_cache  # noqa: E402


@pytest.fixture(autouse=True)
def fresh_rate_limits():
    rate_limit.reset()
    response_cache.reset()                  # one test's cached answer must not leak into the next
    yield
    rate_limit.reset()
    response_cache.reset()
