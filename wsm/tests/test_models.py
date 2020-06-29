import unittest
from wsm.model import CheckResult


class TestCheckResult(unittest.TestCase):

    def setUp(self):
        self.under_test = CheckResult(
            status=200,
            url='http://localhost',
            created=123,
            response_time_ms=42,
        )

    def test_init(self):
        self.assertIsNotNone(self.under_test.id)
        self.assertEqual(self.under_test.status, 200)
        self.assertEqual(self.under_test.url, 'http://localhost')
        self.assertEqual(self.under_test.created, 123)
        self.assertEqual(self.under_test.response_time_ms, 42)

    def test_json_serializaton(self):
        deserialised = CheckResult.from_json(self.under_test.to_json())

        self.assertEqual(deserialised.id, self.under_test.id)
        self.assertEqual(deserialised.status, self.under_test.status)
        self.assertEqual(deserialised.url, self.under_test.url)
        self.assertEqual(deserialised.created, self.under_test.created)
        self.assertEqual(deserialised.response_time_ms, self.under_test.response_time_ms)
