import time
import os
import uuid
from typing import List, Optional

__all__ = ["uuid7", "batch_uuid7"]

_UUID_VERSION: int = 7
_UUID_VARIANT: int = 0b10  # RFC 4122 variant bits
_EPOCH_START: int = 0  # Unix epoch start


def _get_timestamp_ms() -> int:
    """
    Return current Unix timestamp in milliseconds.
    """
    return int(time.time() * 1000)


def uuid7(timestamp_ms: Optional[int] = None) -> uuid.UUID:
    """
    Generate a UUIDv7 according to draft spec.

    Args:
        timestamp_ms: Optional[int] — milliseconds since Unix epoch.
                      If None, current time is used.

    Returns:
        uuid.UUID instance representing the UUIDv7.
    """
    if timestamp_ms is None:
        timestamp_ms = _get_timestamp_ms()

    # Mask timestamp to 48 bits
    ts48: int = timestamp_ms & ((1 << 48) - 1)

    # Convert timestamp to 6-byte big-endian bytes
    ts_bytes: bytes = ts48.to_bytes(6, "big")

    # Generate 10 random bytes for randomness component
    rand_bytes: bytes = os.urandom(10)

    # Combine timestamp and random parts
    uuid_bytes: bytearray = bytearray(ts_bytes + rand_bytes)

    # Set UUID version (7) in the upper nibble of byte 6 (index 6)
    uuid_bytes[6] &= 0x0F
    uuid_bytes[6] |= (_UUID_VERSION << 4) & 0xF0

    # Set UUID variant bits (10xx) in byte 8 (index 8)
    uuid_bytes[8] &= 0x3F
    uuid_bytes[8] |= (_UUID_VARIANT << 6) & 0xC0

    return uuid.UUID(bytes=bytes(uuid_bytes))


def batch_uuid7(
    n: int,
    timestamp_start_ms: Optional[int] = None,
    interval_ms: int = 1,
) -> List[uuid.UUID]:
    """
    Generate a batch of n UUIDv7s spaced by interval_ms milliseconds.

    Args:
        n: number of UUIDs to generate
        timestamp_start_ms: optional starting timestamp in ms (current time if None)
        interval_ms: time spacing between UUID timestamps in ms

    Returns:
        List of uuid.UUID objects
    """
    if timestamp_start_ms is None:
        timestamp_start_ms = _get_timestamp_ms()

    uuids: List[uuid.UUID] = []
    for i in range(n):
        ts = timestamp_start_ms + i * interval_ms
        uuids.append(uuid7(timestamp_ms=ts))

    return uuids