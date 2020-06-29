import re
import urllib.request

from socket import timeout
from time import time
from urllib.error import (
    HTTPError,
    URLError,
)

from wsm.model import CheckResult


CHECK_MAX_TIMEOUT_SEC = 10


class Check(object):

    def __init__(self, url=None, regex=''):
        if not url:
            raise ValueError('url can not be null')
        self.url = url
        self.regex = None
        if regex:
            self.regex = re.compile(regex)

    def check_regex(self, body):
        if not self.regex:
            return True
        return self.regex.search(body) is not None

    def perform(self, check_timeout=CHECK_MAX_TIMEOUT_SEC):
        code = 0
        started = time()
        try:
            with urllib.request.urlopen(
                    self.url,
                    timeout=check_timeout,
            ) as response:
                code = response.code
                if not self.check_regex(
                    response.read().decode(
                        response.headers.get_content_charset() or 'utf-8',
                    ),
                ):
                    code = -2

        except HTTPError as e:
            # http error occurred
            code = e.code
        except URLError:
            # network error occurred
            code = -1
        except timeout:
            # http call reached CHECK_MAX_TIMEOUT_SEC
            # treat it as a network error
            code = -1

        now = time()
        elapsed = now - started

        return CheckResult(
            created=int(now),
            url=self.url,
            status=code,
            response_time_ms=int(elapsed * 1000),
        )

    @classmethod
    def parse_from_config(cls, cfg):
        checks = cfg.get('checks')
        if not checks:
            return []
        return [cls(c.get('url'), c.get('regex')) for c in checks]
