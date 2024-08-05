from time_interval import TimeIntervals
from weekday import Weekday
import json
from datetime import *

class SetPoint:
    def __init__(self, time: time, value):
        self.time = time
        self.value = value

    def to_json(self):
        return {
            'time': {'hour': self.time.hour, 'minute': self.time.minute},
            'value': self.value
        }

    @classmethod
    def from_json(cls, data):
        if isinstance(data, str):
            data = json.loads(data)
        s_time = time(hour=data['time']['hour'], minute=data['time']['minute'])
        value = data['value']
        return cls(s_time, value)
                   
class PowerSchedule:
    def __init__(self, schedule: list[SetPoint], interval: TimeIntervals, days: list[Weekday]):
        self.schedule = schedule
        self.interval = interval
        self.days = days
        
    def to_json(self):
        return {
            'schedule': [sp.to_json() for sp in self.schedule],
            'interval': self.interval.value,
            'days': [day.name for day in self.days]
        }
        
    @classmethod
    def from_json(cls, data):
        if isinstance(data, str):
            data = json.loads(data)
        print(data)
        schedule = [SetPoint.from_json(sp) for sp in data['schedule']]
        interval = TimeIntervals(data['interval'])
        days = [Weekday[day] for day in data['days']]
        return cls(schedule, interval, days)
    
