import re
import unittest

from wsm.checker import Check


class TestCheck(unittest.TestCase):

    def test_init_should_fail_if_no_url_provided(self):
        with self.assertRaises(ValueError):
            Check()

    def test_init_should_fail_if_malform_regex_provided(self):
        with self.assertRaises(Exception):
            Check('http://google.com', '[0-')

    def test_check_regex_should_work(self):
        for expected_rx, expected_result in [
            ('', True),
            ('[0-9].*?', True),
            ('foobar', False),
        ]:
            under_test = Check('http://google.com', expected_rx)
            self.assertEqual(
                expected_result,
                under_test.check_regex('foo 123 bar'),
                'failed on regex: {}'.format(expected_rx),
            )

    def test_parse_from_config_should_create_list_of_checks(self):
        cfg = {
            'checks': [
                {
                    'url': 'https://google.com',
                },
                {
                    'url': 'https://google.com/not_found',
                    'regex': 'ab',
                },
            ],
        }
        actual = Check.parse_from_config(cfg)
        self.assertEqual(2, len(actual))

        self.assertEqual('https://google.com', actual[0].url)
        self.assertIsNone(actual[0].regex)
        self.assertEqual('https://google.com/not_found', actual[1].url)
        self.assertEqual(re.compile('ab'), actual[1].regex)

    def test_parse_from_config_should_process_empy_config(self):
        actual = Check.parse_from_config({})
        self.assertEqual(actual, [])
        actual = Check.parse_from_config({'checks': []})
        self.assertEqual(actual, [])
