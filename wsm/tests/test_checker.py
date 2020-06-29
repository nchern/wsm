import time
import unittest

from unittest.mock import (
    MagicMock,
)
from http.server import BaseHTTPRequestHandler

from wsm.model import CheckResult
from wsm.checker import (
    do_checks,
    Check,
    CHECK_MAX_TIMEOUT_SEC,
)

from .httpd import serve_http


class TestHander(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        return  # mute logging

    def do_GET(self):
        if self.path.endswith('timeout'):
            time.sleep(CHECK_MAX_TIMEOUT_SEC + 1)
        elif self.path.endswith('bad_request'):
            self.send_response(400)
        else:
            self.send_response(200)

        self.send_header('Content-type', 'text/html')
        self.end_headers()

        self.wfile.write('OK'.encode('utf-8'))


class TestChecker(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        serve_http(TestHander)

    def test_do_checks_should_check_and_send_results(self):
        checks = [
            (Check(url='http://fake-server:65002/'), -1),
            (Check(url='http://localhost:65001/ok'), 200),
            (Check(url='http://localhost:65001/ok', regex='html'), -2),
            (Check(url='http://localhost:65001/bad_request'), 400),
            (Check(url='http://localhost:65001/timeout'), -1),
        ]

        producer_mock = MagicMock()

        do_checks([c for c, _ in checks], producer_mock)

        self.assertEqual(producer_mock.send.call_count, len(checks))

        call_args = producer_mock.send.call_args_list
        for i, item in enumerate(checks):
            check, expected_status = item

            actual = CheckResult.from_json(call_args[i][0][1].decode('utf-8'))
            self.assertEqual(check.url, actual.url)
            self.assertEqual(expected_status, actual.status)
            self.assertTrue(actual.response_time_ms > 0)
