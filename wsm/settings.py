import os


TOPIC_NAME = 'wsm_checks'

KAFKA_CONN_CONFIG = {
    'bootstrap_servers': 'broker:9092',
    'security_protocol': 'PLAINTEXT',
}

KAFKA_SECURITY_CONFIG = {
    'ssl_cafile': '/ssl/ca.pem',
    'ssl_certfile': '/ssl/service.cert',
    'ssl_keyfile': '/ssl/service.key',
}

KAFKA_CONSUMER_CONFIG = {
    'group_id': 'wsm-group',
    'client_id': 'wsm-client-1',
    'auto_offset_reset': 'earliest',
}


DSN = {
    'host': 'db',
    'port': 5432,
    'dbname': 'devdb',
    'user': 'root',
    # read password from env var so that it is never kept in config
    'password': os.getenv('DB_PASSWORD', 'dev'),
}


def get_producer_config():
    cfg = dict(KAFKA_CONN_CONFIG)
    if cfg['security_protocol'] == 'SSL':
        cfg.update(KAFKA_SECURITY_CONFIG)

    return cfg


def get_consumer_config():
    cfg = get_producer_config()
    cfg.update(KAFKA_CONSUMER_CONFIG)

    return cfg


def _update_dict(section, cfg):
    for key in cfg:
        if key not in section or key == 'password':
            continue
        cfg[key] = section[key]


def update(cfg):
    _update_dict(cfg.get('kafka', {}), KAFKA_CONN_CONFIG)
    _update_dict(cfg.get('db', {}), DSN)
