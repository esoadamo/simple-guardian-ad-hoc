from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Iterator, NamedTuple, Set

from lib import LogParser, LinuxLineLogParser, LogRule


class MatchingRecord(NamedTuple):
    scope: str
    date: datetime
    data: Dict[str, str]
    record: str


class LogFile:
    def __init__(self, path: Path,
                 parser: Optional[LogParser] = None):
        self.__path = path
        self.__parser = parser if parser is not None else LinuxLineLogParser(path)

    def find_new_matching_records(self, rules: Set[LogRule]) -> Iterator[MatchingRecord]:
        new_records = self.__parser.get_new_records()
        for record in new_records:
            for rule in rules:
                rule_match = rule.parse_record(record)
                if rule_match is not None:
                    matching_record = MatchingRecord(
                        scope=self.__parser.parse_line_scope(rule_match),
                        date=self.__parser.parse_line_time(rule_match),
                        data=rule_match,
                        record=record
                    )

                    assert matching_record.scope is not None
                    assert matching_record.date is not None

                    yield matching_record
                    break
