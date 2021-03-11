from typing import List, Set, Dict
from threading import Thread
from time import sleep

from lib import AppProfile, LogFile, LogRule, RecordsDatabase


def start_scan_profiles(profiles: List[AppProfile],
                        database: RecordsDatabase,
                        scan_time=180,
                        scan_range=1800,
                        ) -> None:
    logs: Dict[LogFile, Set[LogRule]] = {}

    for profile in profiles:
        if profile.log not in logs:
            logs[profile.log] = set()
        logs[profile.log].update(profile.rules)
    del profile

    threads = [Thread(daemon=True, target=__thread_log_scanner, args=[log, rules, scan_time, scan_range, database])
               for log, rules in logs]
    del logs
    for t in threads:
        t.join()


def __thread_log_scanner(log: LogFile, rules: Set[LogRule], scan_time: int, database: RecordsDatabase):
    while True:
        for record in log.find_new_matching_records(rules):
            database.add_record(record)
        sleep(scan_time)
