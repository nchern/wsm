#!/usr/bin/env python3
import argparse
import logging
import json
import sys

import wsm.checker as checker
import wsm.consumer as consumer
import wsm.settings as settings

from wsm.checker import Check


logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
)


def main(args):
    sub_command = args.cmd[0]

    cfg = json.load(open(args.config))
    settings.update(cfg)

    if sub_command == 'check':
        checker.run_forever(Check.parse_from_config(cfg))
    elif sub_command == 'consume':
        consumer.run_forever()
    else:
        print('unknown command: {}'.format(sub_command))
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Web site monitor')
    parser.add_argument(
        '--config',
        default='cfg.dev.json',
        help='config file name. If empty the default configuration will be used',
    )
    parser.add_argument(
        'cmd',
        nargs=1,
        help='sub command. One of: (consume|check). consume - to read and store metrics. check - to perform checks and send them over', # noqa
    )
    args = parser.parse_args()

    try:
        main(args)
    except KeyboardInterrupt:
        logging.info('CTRL-C - terminating...')
        sys.exit(0)
    except Exception as e:
        logging.exception('%s: program terminated', e)
