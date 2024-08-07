from jupiter_grpc import *
from amber_data_grpc import *
from amber_data import *
from schedule_store import ScheduleStore
from datetime import date, time
from schedule import PowerSchedule, PowerSetPoint
from weekday import Weekday
import logging
from time import sleep
import traceback
import threading
from typing import Callable

log = logging.getLogger("jupiter_main")

FALLBACK_POWER_SETPOINT = 0

KW_to_W = 1000

client = JupiterController(id=1)

def int_to_weekday(i: int) -> Weekday:
    match i:
        case 0:
            return Weekday.Mon
        case 1:
            return Weekday.Tue
        case 2:
            return Weekday.Wed
        case 3:
            return Weekday.Thu
        case 4:
            return Weekday.Fri
        case 5:
            return Weekday.Sat
        case 6:
            return Weekday.Sun
        case _:
            raise ValueError("Invalid weekday")
 
def get_scheduled_setpoint():
    current_time = time()
    today = int_to_weekday(date.today().weekday())
    schedule = ScheduleStore.get_latest_schedule()
    matched_schedules = [sch for sch in schedule if today in sch.days]
    if len(matched_schedules) == 0:
        matched_schedules = [sch for sch in schedule if Weekday.Default in sch.days]
        
    if len(matched_schedules) == 0:
        log.info(f"No schedules found for {today} using default.")
        return None
        
    if len(matched_schedules) > 1:
        log.warn(f"Multiple schedules found for {today}.")
        return None
    
    setpoints = matched_schedules[0].schedule
    try:
        return next(sp.value for sp in setpoints if sp.time <= current_time)
    except StopIteration:
        log.Error(f"No setpoint found for {current_time} in {schedule}. May be malformed.")
        return None


def get_current_power_setpoint(tick_info):
    for set_goal in tick_info.pipeline_state.goals:
        if set_goal.target.type == SiteElementType.GRPC_SITE_ELEMENT_TYPE_SITE_IDENTIFIER:
            typed_goal = getattr(set_goal.goal, set_goal.goal.WhichOneof('goal'))
            if typed_goal.category == JupiterGoalCategory.JUPITER_GOAL_CATEGORY_FUNCTION and isinstance(typed_goal, PowerTargetGoal):
                return typed_goal.setpoint
    return set_goal

def bound_power_setpoint(tick_info:TickInfo, setpoint):
    current_caps:PoweredElementCapabilities = [caps for caps in tick_info.site_snapshot.current_capabilities.power_capabilities if caps.identifier.type == SiteElementType.GRPC_SITE_ELEMENT_TYPE_SITE_IDENTIFIER][0]
    new_setpoint = min(setpoint, current_caps.max_charge_absolute)
    new_setpoint = max(new_setpoint, -current_caps.max_discharge_absolute)
    if new_setpoint != setpoint:
        log.warn(f"Setpoint {setpoint} W out of bounds. Adjusting to {new_setpoint} W.")
    return new_setpoint
    

def main_loop(cancel_event):
    while not cancel_event.is_set():
        tick_info = client.get_latest_tick_info()
        try:
            scheduled_setpoint = (get_scheduled_setpoint() or FALLBACK_POWER_SETPOINT) * KW_to_W
            scheduled_setpoint = bound_power_setpoint(tick_info, scheduled_setpoint)
            if get_current_power_setpoint(tick_info) == scheduled_setpoint:
                log.debug(f"Matching setpoint {scheduled_setpoint} W already active.")
            else:
                client.dispatch_goal(power_target_goal(tick_info.site_snapshot.identifier, scheduled_setpoint))
                log.debug(f"PowerTargetGoal({scheduled_setpoint} W) dispatched.")
        except Exception as e:
            log.error(f"Error: {e.with_traceback(None)}")
        cancel_event.wait(10)

if __name__ == '__main__':
    main_loop(threading.Event())