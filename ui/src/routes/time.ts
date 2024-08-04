import { TimeInterval } from "$lib/time_intervals";

export default class Time {
    private static Regex = /^([01]?[0-9]|2[0-3]):[0-5][0-9]$/;

    time_str: string;
    hour: number;
    minute: number;
    
    constructor(hour: number, minute: number) {
        if (hour < 0 || hour > 23) throw new Error("Invalid hour. Expected range: 0-23");
        if (minute < 0 || minute > 59) throw new Error("Invalid minute. Expected range: 0-59");
        this.hour = hour;
        this.minute = minute;
        this.time_str = `${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`;
    }

    static from_string(time: string) : Time | null {
        if (!this.valid_time_string(time)) return null;
        let parts = time.split(":");
        let hour = parseInt(parts[0]);
        let minute = parseInt(parts[1]);
        return new Time(hour, minute);
    }

    static valid_time_string(time: string) : boolean {
        return Time.Regex.test(time);
    }

    subtract(other: Time): number {
        return this.hour * 60 + this.minute - other.hour * 60 - other.minute;
    }

    round(interval:TimeInterval) {
        const totalMinutes = this.hour * 60 + this.minute;
        const roundedMinutes = Math.floor(totalMinutes / interval) * interval;
        return new Time(Math.floor(roundedMinutes / 60), roundedMinutes % 60);
    }
}