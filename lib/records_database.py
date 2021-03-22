from json import dumps, loads
from pathlib import Path
from typing import Optional, Iterator
from datetime import datetime

from sqlitedb import SQLiteDB

from lib import MatchingRecord


class RecordsDatabase:
    def __init__(self, file: Optional[Path]) -> None:
        self.__db = SQLiteDB(f"{file.absolute()}" if file is not None else '::memory::')
        self.__init_tables()

    def add_record(self, record: MatchingRecord) -> None:
        self.__db.execute('''
        INSERT INTO `record` (`scope`,`date`,`line`,`data`) VALUES (?, ?, ?, ?);
        ''', (record.scope, int(record.date.timestamp()), record.record, dumps(record.data)))

    def get_records_in_time_range_with_attacks(self, time_range: int, max_attacks: int) -> Iterator[MatchingRecord]:
        for d in self.__db.execute('SELECT MAX(`date`) FROM `record`'):
            max_date: int = d[0]
            break
        else:
            return

        min_date = max_date - time_range
        for r in self.__db.execute('SELECT `scope`, `date`, `line`, `data`'
                                   'FROM `record` WHERE `date` >= ? AND COUNT(*) >= ? GROUP BY `scope`',
                                   (min_date, max_attacks)):
            yield MatchingRecord(scope=r[0],
                                 date=datetime.fromtimestamp(r[1]),
                                 record=r[1],
                                 data=loads(r[2]) if r[2] is not None else None
                                 )

    def __init_tables(self) -> None:
        self.__db.execute('''CREATE TABLE IF NOT EXISTS `record` (
                                `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                `scope`	TEXT NOT NULL,
                                `date`	INTEGER NOT NULL,
                                `line`	TEXT,
                                `data`	TEXT
                            );''')
