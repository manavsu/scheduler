
from config import *
import math
import threading
import json
from schedule import PowerSchedule


class ScheduleStore:
    lock = threading.Lock()
    latest_schedule:list[PowerSchedule]|None = None

    @classmethod
    def load_all_schedule(cls) -> list[PowerSchedule]:
        schedules = []
        if not os.path.exists(DB_PATH):
            return [PowerSchedule.default()]
        with cls.lock:
            with open(DB_PATH) as file:
                data = json.load(file)
            for schedule in data:
                schedules.append(PowerSchedule.from_json(schedule))
            cls.latest_schedule = schedules.copy()
        if len(schedules) == 0:
            schedules.append(PowerSchedule.default())
        return schedules
    
    @classmethod
    def save_schedule(cls, schedules: list[PowerSchedule]):
        str_schedules = []
        for schedule in schedules:
            str_schedules.append(schedule.to_json())
        with cls.lock:
            cls.latest_schedule = schedules.copy()
            with open(DB_PATH, 'w') as file:
                json.dump(str_schedules, file, indent=4)
    
    @classmethod
    def get_latest_schedule(cls) -> list[PowerSchedule]:
        with cls.lock:
            if cls.latest_schedule is not None:
                return cls.latest_schedule if cls.latest_schedule is not None else []
        return cls.load_all_schedule()
        
        
        