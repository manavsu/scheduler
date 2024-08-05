import { TimeInterval } from '$lib/time_intervals';
import  Time  from './time';
import Weekday from './weekday';

export default class PowerSchedule {
    Schedule: { time: Time, value: number}[];
    Interval: TimeInterval;
    Days: Weekday[];
    
    constructor() {
        this.Schedule = [{time: new Time(0,0), value: 0}];
        this.Days = [];
        this.Interval = TimeInterval.ONE_HOUR;
    }

    static from_schedule(schedule: PowerSchedule) {
        let new_schedule = new PowerSchedule();
        new_schedule.Schedule = schedule.Schedule;
        new_schedule.Days = schedule.Days;
        return new_schedule;
    }

    validate(schedule: { time: Time, value: number }[]) {
        let times:string[] = [];
        for (let i = 0; i < schedule.length; i++) {
            if (times.includes(schedule[i].time.time_str)) {
                throw new Error("Schedule has duplicate times");
            }
            times.push(schedule[i].time.time_str);
        }
        for (let i = 1; i < this.Schedule.length; i++) {
            if (this.Schedule[i].time.subtract(this.Schedule[i-1].time) < 0) {
                throw new Error("Schedule is not in order");
            }
        }
        if (this.Schedule[0].time.subtract(new Time(0,0)) != 0) {
            throw new Error("Schedule must start at 00:00");
        }
    }

    toggle_run_day(day: Weekday) {
        if (this.Days.indexOf(day) == -1) {
            this.Days.push(day);
            return;
        }
        this.Days = this.Days.filter(x => x != day);
    }

    update_interval(interval: TimeInterval) {
        if (interval < this.Interval) {
            this.Interval = interval;
            return
        }
        this.Interval = interval;
        this.Schedule = this.Schedule.map(x => { return {time: x.time.round(interval), value: x.value} });
        let times:string[] = [];
        let schedule = this.Schedule;
        let unique_schedule = [];
        for (let i = 0; i < schedule.length; i++) {
            if (times.includes(schedule[i].time.time_str)) {
                continue;
            }
            times.push(schedule[i].time.time_str);
            unique_schedule.push(schedule[i]);
        }
        this.Schedule = unique_schedule;
        console.log(this.Schedule);
        this.validate(this.Schedule);
    }
}