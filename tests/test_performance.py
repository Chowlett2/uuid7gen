import pytest
import time
from uuid7gen import uuid7, batch_uuid7


class TestPerformance:
    def test_uuid7_generation_speed(self):
        # Test that UUID generation is reasonably fast
        start_time = time.time()
        for _ in range(1000):
            uuid7()
        end_time = time.time()
        
        # Should be able to generate 1000 UUIDs in less than 1 second
        assert (end_time - start_time) < 1.0

    def test_batch_uuid7_efficiency(self):
        # Test that batch generation is more efficient than individual calls
        n = 1000
        
        # Time individual generation
        start_time = time.time()
        individual_uuids = [uuid7() for _ in range(n)]
        individual_time = time.time() - start_time
        
        # Time batch generation
        start_time = time.time()
        batch_uuids = batch_uuid7(n)
        batch_time = time.time() - start_time
        
        assert len(individual_uuids) == n
        assert len(batch_uuids) == n
        
        # Batch should be faster or at least not significantly slower
        # Allow some tolerance for measurement variance
        assert batch_time <= individual_time * 1.5

    @pytest.mark.parametrize("batch_size", [10, 100, 1000, 10000])
    def test_batch_scaling(self, batch_size):
        # Test that batch generation scales reasonably
        start_time = time.time()
        result = batch_uuid7(batch_size)
        end_time = time.time()
        
        assert len(result) == batch_size
        
        # Should complete within reasonable time (adjust threshold as needed)
        time_per_uuid = (end_time - start_time) / batch_size
        assert time_per_uuid < 0.001  # Less than 1ms per UUID