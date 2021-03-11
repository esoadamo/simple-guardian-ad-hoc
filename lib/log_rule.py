import re
from typing import List, Union, Optional, Dict


class LogRule:
    def __init__(self, rule: str):
        self.__regex_rule = re.escape(rule)
        self.__regex_group_names: List[Union[str, None]] = []

        # generate variable groups
        for find in re.finditer(r"\\%([a-zA-Z0-9_\-]+?)\\%", self.__regex_rule, re.IGNORECASE):
            variable = find.groups()[0]
            self.__regex_rule = self.__regex_rule.replace(f'\\%{variable}\\%', '(.+?)')
            if variable == '_':
                self.__regex_group_names.append(None)
            else:
                if variable in self.__regex_group_names:
                    raise ValueError(f'Variable {variable} already exists in this name')
                self.__regex_group_names.append(variable)

        self.__regex_rule = f'^{self.__regex_rule}$'

    @property
    def regex_rule(self) -> str:
        return self.__regex_rule

    def parse_record(self, record: str) -> Optional[Dict[str, str]]:
        match = re.fullmatch(self.regex_rule, record)
        if match is None:
            return None

        r = {}
        for i, g in enumerate(match.groups()):
            r[self.__regex_group_names[i]] = g

        return r

    def __hash__(self) -> int:
        return hash(self.__regex_rule)
