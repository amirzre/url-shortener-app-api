import threading
import time
from unittest import TestCase

from urlshortener.utils.snowflake import SnowflakeIDGenerator


class TestSnowflakeIDGenerator(TestCase):
    def setUp(self):
        self.datacenter_id = 1
        self.machine_id = 1
        self.generator = SnowflakeIDGenerator(self.datacenter_id, self.machine_id)

    def test_unique_ids(self):
        id1 = self.generator.generate_id()
        id2 = self.generator.generate_id()
        self.assertNotEqual(id1, id2, "Generated IDs should be unique")

    def test_sequential_ids_within_same_millisecond(self):
        ids = [self.generator.generate_id() for _ in range(SnowflakeIDGenerator.MAX_SEQUENCE + 1)]
        self.assertEqual(len(set(ids)), len(ids), "IDs within the same millisecond should be unique")

    def test_sequence_reset_on_new_millisecond(self):
        self.generator.last_timestamp = self.generator._current_time_millis() - 1
        id1 = self.generator.generate_id()
        time.sleep(0.001)  # Sleep for 1 millisecond
        id2 = self.generator.generate_id()
        self.assertTrue(id2 > id1, "ID should increase across milliseconds")

    def test_clock_backward_handling(self):
        with self.assertRaises(Exception, msg="Clock moved backwards. Refusing to generate id"):
            self.generator.last_timestamp = self.generator._current_time_millis() + 1
            self.generator.generate_id()

    def test_max_datacenter_id(self):
        with self.assertRaises(ValueError, msg="Datacenter ID must be between 0 and 31"):
            SnowflakeIDGenerator(SnowflakeIDGenerator.MAX_DATACENTER_ID + 1, self.machine_id)

    def test_max_machine_id(self):
        with self.assertRaises(ValueError, msg="Machine ID must be between 0 and 31"):
            SnowflakeIDGenerator(self.datacenter_id, SnowflakeIDGenerator.MAX_MACHINE_ID + 1)

    def test_thread_safety(self):
        ids = set()
        lock = threading.Lock()

        def generate_ids():
            for _ in range(1000):
                with lock:
                    ids.add(self.generator.generate_id())

        threads = [threading.Thread(target=generate_ids) for _ in range(10)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.assertEqual(len(ids), 10000, "All generated IDs should be unique even in a multithreaded context")

    def test_datacenter_id_zero(self):
        generator = SnowflakeIDGenerator(0, self.machine_id)
        id1 = generator.generate_id()
        self.assertTrue(id1 > 0, "Generated ID should be positive even with datacenter_id = 0")

    def test_machine_id_zero(self):
        generator = SnowflakeIDGenerator(self.datacenter_id, 0)
        id1 = generator.generate_id()
        self.assertTrue(id1 > 0, "Generated ID should be positive even with machine_id = 0")

    def test_edge_datacenter_and_machine_id(self):
        generator = SnowflakeIDGenerator(SnowflakeIDGenerator.MAX_DATACENTER_ID, SnowflakeIDGenerator.MAX_MACHINE_ID)
        id1 = generator.generate_id()
        self.assertTrue(id1 > 0, "Generated ID should be positive with max datacenter_id and machine_id")

    def test_timestamp_with_custom_epoch(self):
        custom_epoch = int(time.time() * 1000)  # Set custom epoch to current time
        SnowflakeIDGenerator.EPOCH = custom_epoch

        generator = SnowflakeIDGenerator(self.datacenter_id, self.machine_id)
        id1 = generator.generate_id()
        timestamp_part = (id1 >> SnowflakeIDGenerator.TIMESTAMP_SHIFT) + custom_epoch
        current_time = int(time.time() * 1000)
        self.assertAlmostEqual(timestamp_part, current_time, delta=10, msg="Timestamp should match the current time")

    def test_max_sequence(self):
        generator = SnowflakeIDGenerator(self.datacenter_id, self.machine_id)
        generator.last_timestamp = generator._current_time_millis()
        generator.sequence = SnowflakeIDGenerator.MAX_SEQUENCE
        id1 = generator.generate_id()
        self.assertTrue(id1 > 0, "Generated ID should be positive at max sequence number")

    def test_no_collision_in_multithreaded_environment(self):
        def generate_ids(generator, num_ids, results):
            for _ in range(num_ids):
                results.append(generator.generate_id())

        num_threads = 10
        num_ids = 1000
        threads = []
        results = []
        generator = SnowflakeIDGenerator(self.datacenter_id, self.machine_id)

        for _ in range(num_threads):
            thread = threading.Thread(target=generate_ids, args=(generator, num_ids, results))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        unique_results = set(results)
        self.assertEqual(
            len(unique_results), len(results), "There should be no duplicate IDs in a multithreaded environment"
        )
