import typing

import pydantic


class OSInfo(pydantic.BaseModel):
    platform: str


class PythonInfo(pydantic.BaseModel):
    version: str
    executable: str
    pythonpath: typing.List[str]
    version_info: typing.Dict


class ProcessInfo(pydantic.BaseModel):
    argv: typing.List[str]
    cwd: str
    user: str
    pid: int
    environ: typing.Dict


class EnvironmentState(pydantic.BaseModel):
    os: OSInfo
    python: PythonInfo
    process: ProcessInfo
