import logging

from kafka import KafkaConsumer
from wsm.model import CheckResult
from wsm.settings import (
    TOPIC_NAME,
    get_consumer_config,
)

from .db import save_to_db


POLL_TIMEOUT_MS = 1000


def consume(consumer):
    raw_msgs = consumer.poll(timeout_ms=POLL_TIMEOUT_MS)
    for _, msgs in raw_msgs.items():
        for msg in msgs:
            try:
                res = CheckResult.from_json(msg.value.decode('utf-8'))
                save_to_db([res])
            except Exception as e:
                # Just log any exception.
                # In this scenario we basically lose metrics read from kafka topic
                # in case of any errror. Chose this option for sake of simplicity.
                logging.exception(e)

    consumer.commit()


def run_forever(consumer=None):
    if not consumer:
        consumer = KafkaConsumer(
            TOPIC_NAME,
            **get_consumer_config(),
        )

    while True:
        consume(consumer)
        consumer.commit()
