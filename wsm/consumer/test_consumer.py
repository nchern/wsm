import unittest

from psycopg2 import Error
from unittest.mock import (
    MagicMock,
    Mock,
    patch,
)

from .db import INSERT_SQL_STMT
from .consumer import consume


def create_mock_messages(*args):
    return [
        (
            '',
            [Mock(value=m.encode('utf-8')) for m in args],
        )
    ]


class TestConsumer(unittest.TestCase):

    def setUp(self):
        self.consumer = Mock()
        self.cursor_obj_mock = MagicMock()
        self.connection_mock = MagicMock()
        self.connection_mock.cursor.return_value.__enter__ = MagicMock(
            return_value=self.cursor_obj_mock,
        )

    @patch('psycopg2.connect')
    def test_consume_should_read_and_save_check_results(self, connect_mock):
        in_message = create_mock_messages(
            'bad_json',
            '{"id": "8acd8611-7a49-488b-8e68-a089ee534851", "response_time_ms": 42, "url": "http://localhost", "status": 200, "created": 123}', # noqa
        )
        self.consumer.poll = MagicMock(
            return_value=Mock(**{'items.return_value': in_message})
        )

        connect_mock.return_value.__enter__.return_value = self.connection_mock

        consume(self.consumer)

        self.cursor_obj_mock.execute.assert_called_once_with(
            INSERT_SQL_STMT,
            ('8acd8611-7a49-488b-8e68-a089ee534851', 123, "http://localhost", 200, 42),
        )

        self.consumer.commit.assert_called_once_with()

    @patch('psycopg2.connect')
    def test_consume_should_not_fail_on_db_error(self, connect_mock):
        in_message = create_mock_messages(
            '{"id": "000", "response_time_ms": 1, "url": "http://localhost", "status": 1, "created": 1}', # noqa
        )
        self.consumer.poll = MagicMock(
            return_value=Mock(**{'items.return_value': in_message})
        )

        connect_mock.return_value.__enter__.return_value = self.connection_mock
        self.cursor_obj_mock.execute.side_effect = Error

        consume(self.consumer)

        self.cursor_obj_mock.execute.assert_called_once_with(
            INSERT_SQL_STMT,
            ('000', 1, 'http://localhost', 1, 1),
        )

        self.consumer.commit.assert_called_once_with()
