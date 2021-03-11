from typing import List, Set, Dict
from threading import Thread
from time import time, sleep

from lib import AppProfile, LogFile, LogRule, RecordsDatabase


def start_scan_profiles(profiles: List[AppProfile],
                        database: RecordsDatabase,
                        scan_range=1800,
                        ) -> None:
    logs: Dict[LogFile, Set[LogRule]] = {}

    for profile in profiles:
        if profile.log not in logs:
            logs[profile.log] = set()
        logs[profile.log].update(profile.rules)
    del profile

    threads = [Thread(daemon=True, target=__thread_log_scanner, args=[log, rules, scan_range, database])
               for log, rules in logs]
    del logs
    for t in threads:
        t.join()


def __thread_log_scanner(log: LogFile, rules: Set[LogRule], database: RecordsDatabase):
    while True:
        time_start = time()

        for record in log.find_new_matching_records(rules):
            database.add_record(record)

        # max 10 Hz
        time_taken_min = 0.1  # s
        time_taken = time() - time_start
        if time_taken < time_taken_min:
            sleep(time_taken_min - time_taken)
