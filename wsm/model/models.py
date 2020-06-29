import json
import uuid


class CheckResult(object):

    def __init__(self, id=None, url='', created=0, status=0, response_time_ms=0):
        if not id:
            id = uuid.uuid4()

        # As kafka consumer can read the same message more than once,
        # id is required to handle this situation,
        # so a single check result will not be recorded more than once.
        self.id = str(id)

        self.url = url

        self.created = created

        # if status > 0 then it contains http status code of a check.
        # two additional negative values are possible:
        # -1 means that a network problem happened during the check
        # -2 means that regexp check failed
        self.status = status

        self.response_time_ms = response_time_ms

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, s):
        return cls(**json.loads(s.strip()))
