import pytest
import sys
import os

# Add the parent directory to the Python path so we can import uuid7gen
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def sample_timestamp():
    """Provide a consistent timestamp for testing."""
    return 1609459200000  # 2021-01-01 00:00:00 UTC in milliseconds


@pytest.fixture
def sample_timestamps():
    """Provide a list of timestamps for batch testing."""
    base = 1609459200000
    return [base + i * 1000 for i in range(10)]  # 10 timestamps, 1 second apart