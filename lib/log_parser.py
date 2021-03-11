from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


class LogParser:
    def __init__(self, log_file: Path):
        self.__log_file = log_file

    def get_new_records(self) -> List[str]:
        raise NotImplemented('Override this')

    @staticmethod
    def parse_line_time(parsed_rule: Dict[str, str]) -> Optional[datetime]:
        return datetime.now()

    @staticmethod
    def parse_line_ip(parsed_rule: Dict[str, str]) -> Optional[str]:
        import re
        if 'IP' not in parsed_rule:
            return None

        # find IPv4 IP
        re_match = re.finditer(r'[0-9]{0,3}\.[0-9]{0,3}\.[0-9]{0,3}\.[0-9]{0,3}', parsed_rule['IP'])
        if re_match:
            return next(re_match).group()

        # find IPv6 IP TODO
        return parsed_rule['IP']


class LineLogParser(LogParser):
    def __init__(self, log_file: Path):
        super().__init__(log_file)
        self.__file_pos = 0

    def get_new_records(self) -> List[str]:
        with open(self.__log_file, 'r') as f:
            f.seek(self.__file_pos)
            lines = f.read().splitlines()
            self.__file_pos = f.tell()
            return lines

