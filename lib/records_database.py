from json import dumps
from pathlib import Path
from typing import Optional

from sqlitedb import SQLiteDB

from lib import MatchingRecord


class RecordsDatabase:
    def __init__(self, file: Optional[Path]) -> None:
        self.__db = SQLiteDB(f"{file.absolute()}" if file is not None else '::memory::')
        self.__init_tables()

    def add_record(self, record: MatchingRecord) -> None:
        self.__db.execute('''
        INSERT INTO `record`(`ip`,`date`,`line`,`data`) VALUES (?, ?, ?, ?);
        ''', (record.ip, int(record.date.timestamp()), record.record, dumps(record.data)))

    def __init_tables(self) -> None:
        self.__db.execute('''CREATE TABLE IF NOT EXISTS `record` (
                                `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                `ip`	TEXT NOT NULL,
                                `date`	INTEGER NOT NULL,
                                `line`	TEXT,
                                `data`	TEXT
                            );''')
