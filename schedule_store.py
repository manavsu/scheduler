
from config import *
import math
import threading
import json
from schedule import PowerSchedule


class Store:
    lock = threading.Lock()

    @classmethod
    def get_all_schedules(cls):
        schedules = []
        if not os.path.exists(DB_PATH):
            return schedules
        with cls.lock:
            with open(DB_PATH) as file:
                data = json.load(file)
            for schedule in data:
                schedules.append(PowerSchedule.from_json(schedule))
        return schedules
    
    @classmethod
    def save_schedules(cls, schedules: list[PowerSchedule]):
        str_schedules = []
        for schedule in schedules:
            str_schedules.append(schedule.to_json())
        with cls.lock:
            with open(DB_PATH, 'w') as file:
                json.dump(str_schedules, file, indent=4)