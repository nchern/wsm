import asyncio
import aiohttp
import re

from aiohttp.client_exceptions import ClientConnectorError
from concurrent.futures import TimeoutError
from time import time

from wsm.model import CheckResult


CHECK_MAX_TIMEOUT_SEC = 3


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

    @classmethod
    def parse_from_config(cls, cfg):
        checks = cfg.get('checks')
        if not checks:
            return []
        return [cls(c.get('url'), c.get('regex')) for c in checks]


async def fetch(check, loop):
    code = 0
    body = ''
    started = time()

    try:
        timeout = aiohttp.ClientTimeout(total=CHECK_MAX_TIMEOUT_SEC)
        async with aiohttp.ClientSession(loop=loop, timeout=timeout) as session:
            async with session.get(check.url) as resp:
                code = resp.status
                body = await resp.text()
    except ClientConnectorError:
        code = -1
    except TimeoutError:
        code = -1

    now = time()
    elapsed = now - started
    if not check.check_regex(body):
        code = -2
    return CheckResult(
        status=code,
        url=check.url,
        created=int(now),
        response_time_ms=int(elapsed * 1000),
    )


def perform_checks(checks):
    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(fetch(check, loop)) for check in checks]
    results = loop.run_until_complete(asyncio.gather(*tasks))
    for r in results:
        print(r.to_json())
    return results
