from time_interval import TimeIntervals
from weekday import Weekday
import json
from datetime import *

class PowerSetPoint:
    def __init__(self, time: datetime.time, value:float|int):
        self.time:datetime.time = time
        self.value:float|int = value

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
    def __init__(self, schedule: list[PowerSetPoint], interval: TimeIntervals, days: list[Weekday]):
        self.schedule:list[PowerSetPoint] = schedule
        self.interval:TimeIntervals = interval
        self.days:list[Weekday] = days
        
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
        schedule = [PowerSetPoint.from_json(sp) for sp in data['schedule']]
        interval = TimeIntervals(data['interval'])
        days = [Weekday[day] for day in data['days']]
        return cls(schedule, interval, days)
   
    @classmethod 
    def default(cls):
        return cls([PowerSetPoint(time(hour=0, minute=0), 0)], TimeIntervals.ONE_HOUR, [Weekday.Default])
    
