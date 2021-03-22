from typing import List, Set, Dict
from threading import Thread, Lock
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

    notification = Lock()

    threads = [Thread(target=__thread_attacks_processor, daemon=True, args=[notification, database, scan_range])]
    threads.extend([Thread(daemon=True, target=__thread_log_scanner, args=[log, rules, database, notification])
                    for log, rules in logs])
    del logs
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def __thread_attacks_processor(notification: Lock, database: RecordsDatabase, scan_range: int):
    while True:
        notification.acquire()
        notification.acquire()

        # process database


def __thread_log_scanner(log: LogFile, rules: Set[LogRule], database: RecordsDatabase, process_notification: Lock):
    while True:
        time_start = time()

        new_record = False
        for record in log.find_new_matching_records(rules):
            new_record = True
            database.add_record(record)

        if new_record:
            process_notification.release()

        # max 10 Hz
        time_taken_min = 0.1  # s
        time_taken = time() - time_start
        if time_taken < time_taken_min:
            sleep(time_taken_min - time_taken)
