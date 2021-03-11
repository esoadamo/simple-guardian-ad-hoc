from datetime import datetime
from os import stat, path
from typing import Dict, Optional, Iterator


class LogParser:
    def __init__(self, log_context: str):
        self.__log_context = log_context

    def get_new_records(self) -> Iterator[str]:
        raise NotImplemented('Override this')

    # noinspection PyUnusedLocal
    @staticmethod
    def parse_line_time(parsed_rule: Dict[str, str]) -> Optional[datetime]:
        return datetime.now()

    @staticmethod
    def parse_line_scope(parsed_rule: Dict[str, str]) -> Optional[str]:
        return None


class LinuxLineLogParser(LogParser):
    def __init__(self, log_context: str):
        super().__init__(log_context)
        self.__file_pos = 0
        self.__file_modification_time = self.__get_m_time()

    def get_new_records(self) -> Iterator[str]:
        from time import sleep

        m_time = self.__get_m_time()
        if m_time == self.__file_modification_time:
            sleep(1)
            return []

        if m_time is None:
            self.__file_pos = 0
            return []

        with open(self.__log_context, 'r') as f:
            f.seek(self.__file_pos)
            lines = f.read().splitlines()
            self.__file_pos = f.tell()
            return lines

    def __get_m_time(self) -> Optional[float]:
        if not path.isfile(self.__log_context):
            return None
        return stat(self.__log_context).st_mtime

    @staticmethod
    def parse_line_scope(parsed_rule: Dict[str, str]) -> Optional[str]:
        import re
        if 'IP' not in parsed_rule:
            return None

        # find IPv4 IP
        re_match = re.finditer(r'[0-9]{0,3}\.[0-9]{0,3}\.[0-9]{0,3}\.[0-9]{0,3}', parsed_rule['IP'])
        if re_match:
            return next(re_match).group()

        # find IPv6 IP TODO
        return parsed_rule['IP']
