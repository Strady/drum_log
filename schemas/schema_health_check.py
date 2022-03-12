import typing

import pydantic


class HealthCheck(pydantic.BaseModel):
    hostname: str
    status: str
    timestamp: float
    results: typing.List[typing.Dict]
