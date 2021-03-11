from typing import NamedTuple, Set

from lib import LogRule, IPBlocker, LogFile


class AppProfile(NamedTuple):
    profile_name: str
    log: LogFile
    blocker: IPBlocker
    rules: Set[LogRule]
