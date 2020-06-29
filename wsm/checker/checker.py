from kafka import KafkaProducer
from time import sleep
from wsm.settings import (
    get_producer_config,
    TOPIC_NAME,
)


CHECK_WAIT_TIMEOUT_SEC = 5


def do_checks(checks, producer):
    for check in checks:
        res = check.perform()
        producer.send(TOPIC_NAME, res.to_json().encode('utf-8'))


def run_forever(checks, producer=None):
    if not producer:
        producer = KafkaProducer(**get_producer_config())

    while True:
        do_checks(checks, producer)
        sleep(CHECK_WAIT_TIMEOUT_SEC)
