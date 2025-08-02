import pytest
import uuid
import time
from typing import List
from uuid7gen import uuid7, batch_uuid7


class TestUuid7:
    def test_uuid7_basic_generation(self):
        result = uuid7()
        assert isinstance(result, uuid.UUID)
        assert result.version == 7

    def test_uuid7_with_timestamp(self):
        timestamp = 1609459200000  # 2021-01-01 00:00:00 UTC in ms
        result = uuid7(timestamp_ms=timestamp)
        assert isinstance(result, uuid.UUID)
        assert result.version == 7

    def test_uuid7_with_float_timestamp(self):
        timestamp = 1609459200000.5  # Include submillisecond precision
        result = uuid7(timestamp_ms=timestamp)
        assert isinstance(result, uuid.UUID)
        assert result.version == 7

    def test_uuid7_uniqueness(self):
        uuids = [uuid7() for _ in range(1000)]
        assert len(set(uuids)) == 1000

    def test_uuid7_temporal_ordering(self):
        timestamp_base = int(time.time() * 1000)
        uuid1 = uuid7(timestamp_ms=timestamp_base)
        uuid2 = uuid7(timestamp_ms=timestamp_base + 100)
        uuid3 = uuid7(timestamp_ms=timestamp_base + 200)
        
        assert str(uuid1) < str(uuid2) < str(uuid3)

    def test_uuid7_invalid_timestamp_type(self):
        with pytest.raises(TypeError, match="timestamp_ms must be an int or float"):
            uuid7(timestamp_ms="invalid")

    def test_uuid7_negative_timestamp(self):
        with pytest.raises(ValueError, match="timestamp_ms must be non-negative"):
            uuid7(timestamp_ms=-1)

    def test_uuid7_variant_bits(self):
        result = uuid7()
        # Check that variant bits are set correctly (10xx)
        variant_byte = result.bytes[8]
        assert (variant_byte & 0xC0) == 0x80

    def test_uuid7_version_bits(self):
        result = uuid7()
        # Check that version bits are set to 7
        version_byte = result.bytes[6]
        assert (version_byte & 0xF0) == 0x70

    def test_uuid7_timestamp_extraction(self):
        timestamp = 1609459200000
        result = uuid7(timestamp_ms=timestamp)
        
        # Extract timestamp from first 6 bytes
        timestamp_bytes = result.bytes[:6]
        extracted_timestamp = int.from_bytes(timestamp_bytes, 'big')
        
        assert extracted_timestamp == timestamp

    def test_uuid7_submillisecond_precision(self):
        # Test that submillisecond precision is properly encoded
        timestamp = 1609459200000.123  # 123 microseconds
        result = uuid7(timestamp_ms=timestamp)
        
        # The submillisecond part should be encoded in the first 12 bits of randomness
        rand_bytes = result.bytes[6:]
        # First 12 bits after timestamp should contain submillisecond data
        subms_bits = ((rand_bytes[0] & 0x0F) << 8) | rand_bytes[1]
        
        # Should be non-zero since we have submillisecond precision
        assert subms_bits > 0


class TestBatchUuid7:
    def test_batch_uuid7_basic(self):
        n = 10
        result = batch_uuid7(n)
        assert len(result) == n
        assert all(isinstance(u, uuid.UUID) for u in result)
        assert all(u.version == 7 for u in result)

    def test_batch_uuid7_uniqueness(self):
        result = batch_uuid7(100)
        assert len(set(result)) == 100

    def test_batch_uuid7_temporal_ordering(self):
        result = batch_uuid7(10, interval_ms=1)
        str_uuids = [str(u) for u in result]
        assert str_uuids == sorted(str_uuids)

    def test_batch_uuid7_with_start_timestamp(self):
        timestamp = 1609459200000
        result = batch_uuid7(5, timestamp_start_ms=timestamp)
        assert len(result) == 5
        
        # Check that first UUID has the correct timestamp
        first_uuid_timestamp = int.from_bytes(result[0].bytes[:6], 'big')
        assert first_uuid_timestamp == timestamp

    def test_batch_uuid7_with_interval(self):
        result = batch_uuid7(5, interval_ms=10)
        timestamps = []
        for u in result:
            timestamp = int.from_bytes(u.bytes[:6], 'big')
            timestamps.append(timestamp)
        
        # Check that timestamps are spaced by 10ms
        for i in range(1, len(timestamps)):
            assert timestamps[i] - timestamps[i-1] == 10

    def test_batch_uuid7_submillisecond_interval(self):
        result = batch_uuid7(3, interval_ms=0.5)
        assert len(result) == 3
        assert all(u.version == 7 for u in result)

    def test_batch_uuid7_invalid_n_type(self):
        with pytest.raises(ValueError, match="n must be a positive integer"):
            batch_uuid7("invalid")

    def test_batch_uuid7_invalid_n_value(self):
        with pytest.raises(ValueError, match="n must be a positive integer"):
            batch_uuid7(0)
        
        with pytest.raises(ValueError, match="n must be a positive integer"):
            batch_uuid7(-5)

    def test_batch_uuid7_invalid_timestamp_type(self):
        with pytest.raises(TypeError, match="timestamp_start_ms must be an int or float"):
            batch_uuid7(5, timestamp_start_ms="invalid")

    def test_batch_uuid7_negative_timestamp(self):
        with pytest.raises(ValueError, match="timestamp_start_ms must be non-negative"):
            batch_uuid7(5, timestamp_start_ms=-1)

    def test_batch_uuid7_invalid_interval_type(self):
        with pytest.raises(TypeError, match="interval_ms must be an int or float"):
            batch_uuid7(5, interval_ms="invalid")

    def test_batch_uuid7_negative_interval(self):
        with pytest.raises(ValueError, match="interval_ms must be non-negative"):
            batch_uuid7(5, interval_ms=-1)

    def test_batch_uuid7_large_batch(self):
        result = batch_uuid7(1000)
        assert len(result) == 1000
        assert len(set(result)) == 1000


class TestUuid7Integration:
    def test_uuid7_rfc_compliance(self):
        # Test that generated UUIDs comply with RFC 9562 structure
        result = uuid7()
        
        # Check overall format
        assert len(result.bytes) == 16
        assert result.version == 7
        
        # Check variant (should be 10xx in binary)
        variant_byte = result.bytes[8]
        assert (variant_byte >> 6) == 0b10

    def test_uuid7_monotonicity_stress_test(self):
        # Generate UUIDs with explicit timestamps to ensure ordering
        base_timestamp = int(time.time() * 1000)
        uuids = []
        
        for i in range(100):
            # Use incrementing timestamps to guarantee monotonicity
            uuids.append(uuid7(timestamp_ms=base_timestamp + i))
            
        # Convert to strings for lexicographic comparison
        uuid_strings = [str(u) for u in uuids]
        
        # Should be strictly ordered since we control timestamps
        assert uuid_strings == sorted(uuid_strings)

    def test_batch_vs_individual_consistency(self):
        # Compare batch generation with individual generation
        timestamp = int(time.time() * 1000)
        
        # Generate batch
        batch_result = batch_uuid7(5, timestamp_start_ms=timestamp, interval_ms=1)
        
        # Generate individually
        individual_result = []
        for i in range(5):
            individual_result.append(uuid7(timestamp_ms=timestamp + i))
        
        # Both should have same structure and ordering
        assert len(batch_result) == len(individual_result)
        
        # Extract timestamps and verify they match
        for batch_uuid, individual_uuid in zip(batch_result, individual_result):
            batch_ts = int.from_bytes(batch_uuid.bytes[:6], 'big')
            individual_ts = int.from_bytes(individual_uuid.bytes[:6], 'big')
            assert batch_ts == individual_ts

    def test_uuid7_edge_cases(self):
        # Test edge cases
        
        # Very large timestamp (year 2100+)
        future_timestamp = 4102444800000  # 2100-01-01
        result = uuid7(timestamp_ms=future_timestamp)
        assert result.version == 7
        
        # Timestamp with maximum submillisecond precision
        precise_timestamp = 1609459200000.999
        result = uuid7(timestamp_ms=precise_timestamp)
        assert result.version == 7
        
        # Zero timestamp (Unix epoch)
        result = uuid7(timestamp_ms=0)
        assert result.version == 7
        extracted_ts = int.from_bytes(result.bytes[:6], 'big')
        assert extracted_ts == 0