import { TimeInterval } from '$lib/time_intervals';
import  Time  from './time';
import Weekday from './weekday';

export default class PowerSchedule {
    schedule: { time: Time, value: number}[];
    interval: TimeInterval;
    days: Weekday[];
    
    constructor(schedules: { time: Time, value: number}[] = [], interval: TimeInterval = TimeInterval.ONE_HOUR, days: Weekday[] = []) {
        if (schedules.length == 0) {
            this.schedule = [{time: new Time(0,0), value: 0}];
        } else {
            this.schedule = schedules;
        }
        this.days = days;
        this.interval = interval;
        PowerSchedule.validate(this.schedule);
    }

    static from_schedule(schedule: PowerSchedule) {
        let new_schedule = new PowerSchedule();
        new_schedule.schedule = schedule.schedule;
        new_schedule.days = schedule.days;
        return new_schedule;
    }

    reset() {
        this.schedule = [{time: new Time(0,0), value: 0}];
        this.days = [];
        this.interval = TimeInterval.ONE_HOUR;
    }

    static validate(schedule: { time: Time, value: number }[]) {
        let times:string[] = [];
        for (let i = 0; i < schedule.length; i++) {
            if (times.includes(schedule[i].time.time_str)) {
                throw new Error("Schedule has duplicate times");
            }
            times.push(schedule[i].time.time_str);
        }
        for (let i = 1; i < schedule.length; i++) {
            if (schedule[i].time.subtract(schedule[i-1].time) < 0) {
                throw new Error("Schedule is not in order");
            }
        }
        if (schedule[0].time.subtract(new Time(0,0)) != 0) {
            throw new Error("Schedule must start at 00:00");
        }
    }

    toggle_run_day(day: Weekday) {
        if (!this.days.includes(day)) {
            this.days.push(day);
        } else {
            this.days = this.days.filter(x => x != day);
        }
    }

    update_interval(interval: TimeInterval) {
        if (interval < this.interval) {
            this.interval = interval;
            return
        }
        this.interval = interval;
        this.schedule = this.schedule.map(x => { return {time: x.time.round(interval), value: x.value} });
        this.schedule = PowerSchedule.remove_copies_and_consolidate(this.schedule);
        PowerSchedule.validate(this.schedule);
    }

    static remove_copies_and_consolidate(schedule: { time: Time, value: number }[]) {
        console.log(schedule);
        let times:string[] = [];
        let unique_schedule = [];
        for (let i = 0; i < schedule.length; i++) {
            if (times.includes(schedule[i].time.time_str)) {
                continue;
            }
            times.push(schedule[i].time.time_str);
            unique_schedule.push(schedule[i]);
        }
        let consolidated_schedule = [];

        consolidated_schedule.push(unique_schedule[0]);
        for (let i = 1; i < unique_schedule.length; i++) {
            if (unique_schedule[i].value != unique_schedule[i-1].value) {
                consolidated_schedule.push(unique_schedule[i]);
            }
        }
        PowerSchedule.validate(consolidated_schedule);
        console.log(consolidated_schedule);
        return consolidated_schedule;
    }

    get_setpoint(time: Time) { 
        return this.schedule.slice().sort(x => x.time.subtract(time))[0].value;
    }
}