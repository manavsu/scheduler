<script lang="ts">
    import PowerSchedule from "./schedule";
    import Weekday from "./weekday";
    import ChartIcon from "$lib/icons/chart_icon.svelte";
    import TrashIcon from "$lib/icons/trach_icon.svelte";
	import Time from "./time";
	import { TimeInterval } from "$lib/time_intervals";
    import ResetIcon from "$lib/icons/reset_icon.svelte";

    export let schedule = new PowerSchedule();
    export let available_weekdays = [Weekday.Default, Weekday.Mon, Weekday.Tue, Weekday.Wed, Weekday.Thu, Weekday.Fri, Weekday.Sat, Weekday.Sun];
    export let on_delete: () => void;
    export let show_chart: () => void;
    
    let times: string[] = [];
    let power_values: string[] = [];

    function add_setpoint(index: number) {
        if (schedule.Schedule.length - 1 == index) {
            schedule.Schedule.push({time: new Time(23, 59).round(schedule.Interval), value: schedule.Schedule[index].value});
            schedule.Schedule = [...schedule.Schedule];
            return;
        }
        let prev_time = schedule.Schedule[index].time;
        let next_time = schedule.Schedule[index + 1].time;
        let new_hour, new_minute;

        if (next_time.hour - prev_time.hour === 1 && next_time.minute === prev_time.minute) {
            new_hour = prev_time.hour;
            new_minute = (prev_time.minute + 30) % 60;
        } else {
            new_hour = Math.floor((prev_time.hour + next_time.hour) / 2);
            new_minute = Math.floor((prev_time.minute + next_time.minute) / 2);
        }
        let new_time = new Time(new_hour, new_minute);
        new_time = new_time.round(schedule.Interval);

        schedule.Schedule = [
            ...schedule.Schedule.slice(0, index + 1),
            {time: new_time, value: schedule.Schedule[index].value},
            ...schedule.Schedule.slice(index + 1)
        ];
        schedule.Schedule = [...schedule.Schedule];
    }

    function remove_setpoint(index: number) {
        schedule.Schedule = [
            ...schedule.Schedule.slice(0, index),
            ...schedule.Schedule.slice(index + 1)
        ];
    }

    function get_add_setpoint_disabled(index: number) {
        if (schedule.Schedule.length - 1 == index) {
            if (schedule.Schedule[index].time.subtract(new Time(23, 59).round(schedule.Interval)) == 0) {
                return true;
            }
        } else {
            if (schedule.Schedule[index + 1].time.subtract(schedule.Schedule[index].time) <= schedule.Interval) {
                return true;
            }
        }
        return false;
    }

    function get_remove_setpoint_disabled(index: number) {
        if (index == 0) {
            return true;
        }
        return false;
    }

    function update_schedule_days(day: Weekday) {
        if (schedule.Days.includes(day)) {
            if (!available_weekdays.includes(day)) {
                available_weekdays.push(day);
            }
        } else {
            if (available_weekdays.includes(day)) {
                available_weekdays = available_weekdays.filter((weekday) => weekday !== day);
            }
        }
        schedule.toggle_run_day(day);
        available_weekdays = [...available_weekdays];
        schedule.Days = [...schedule.Days];
    }

    function update_times_and_values(schedule:{time: Time, value: number}[]) {
        times = schedule.map((setpoint) => setpoint.time.time_str);
        power_values = schedule.map((setpoint) => setpoint.value.toString());
    }

    function handle_power_input(event:any, index:number) {
        power_values[index] = event.target.value.replace(/[^0-9.-]/g, '');
    }

    function parse_and_update_power(index: number, power: string) {
        let new_power = parseFloat(power);
        if (isNaN(new_power)) {
            power_values[index] = schedule.Schedule[index].value.toString();
            return;
        }
        schedule.Schedule[index].value = new_power;
        schedule.Schedule = [...schedule.Schedule];
    }

    function handle_time_input(event:any, index:number) {
        let filtered_value = event.target.value.replace(/[^0-9:]/g, '');
        times[index] = filtered_value;
    }
    
    function parse_and_update_time(index: number, time: string) {
        let new_time = Time.from_string(time);
        if (new_time == null) {
            times[index] = schedule.Schedule[index].time.time_str;
            return;
        }
        let old_time = schedule.Schedule[index].time;
        schedule.Schedule[index].time = new_time.round(schedule.Interval);
        try {
            schedule.validate(schedule.Schedule);
        } finally {
            schedule.Schedule[index].time = old_time;
            schedule.Schedule = [...schedule.Schedule];
        }
    }

    function handle_keydown(event:any) {
        if (event.key === 'Enter') {
            event.target.blur();
        }
    }

    function update_interval(interval: TimeInterval) {
        schedule.update_interval(interval);
        schedule.Interval = interval;
        schedule.Schedule = [...schedule.Schedule];
    }

    function reset() {
        while (schedule.Days.length > 0) {
            update_schedule_days(schedule.Days[0]);
        }
        schedule.reset();
        schedule.Schedule = [...schedule.Schedule];
    }

    $: update_times_and_values(schedule.Schedule);
    $: remove_setpoint_disabled = schedule.Schedule.map((_, index) => get_remove_setpoint_disabled(index));
    $: add_setpoint_disabled = schedule.Schedule.map((_, index) => get_add_setpoint_disabled(index));
</script>

<div class="flex flex-col text-xl text-nowrap gap-3 py-1">
    <div class="flex flex-row gap-2">
        {#each Object.values(Weekday) as day}
            <button on:click={() => update_schedule_days(day)} disabled={!(schedule.Days.includes(day) || available_weekdays.includes(day))} class="text-center border-2 {schedule.Days.includes(day) ? "text-black bg-white hover:bg-black hover:text-white" : available_weekdays.includes(day) ? "text-white border-white hover:text-black hover:bg-white" : "text-gray-500 border-gray-500"} py-1 px-4 transition">{day}</button>
        {/each}
    </div>
    <div class="flex flex-row gap-2 items-center">
        <button on:click={() => update_interval(TimeInterval.FIVE_MINUTES)} disabled={schedule.Interval == TimeInterval.FIVE_MINUTES} class="border-2 {schedule.Interval == TimeInterval.FIVE_MINUTES ? "text-black bg-white" : "text-white border-white hover:text-black hover:bg-white"} py-1 px-4 transition">5 min</button>
        <button on:click={() => update_interval(TimeInterval.FIFTEEN_MINUTES)} disabled={schedule.Interval == TimeInterval.FIFTEEN_MINUTES} class="border-2 {schedule.Interval == TimeInterval.FIFTEEN_MINUTES ? "text-black bg-white" : "text-white border-white hover:text-black hover:bg-white"} py-1 px-4 transition">15 min</button>
        <button on:click={() => update_interval(TimeInterval.ONE_HOUR)} disabled={schedule.Interval == TimeInterval.ONE_HOUR} class="border-2 {schedule.Interval == TimeInterval.ONE_HOUR ? "text-black bg-white" : "text-white border-white hover:text-black hover:bg-white"} py-1 px-4 transition">1 hr</button>
    </div>
    <div class="flex flex-row gap-2 items-center">
        {#each schedule.Schedule as setpoint, index}
            <input type="text" bind:value={times[index]} on:input={(event) => handle_time_input(event, index)} on:blur={() => parse_and_update_time(index, times[index])} on:keydown={handle_keydown} class="focus:outline-none caret-black bg-white text-black border-2 py-1 px-2 w-20 text-center"/>
            <div class="flex flex-row border-2 items-center py-1 px-4">
                <input type="text" on:keydown={handle_keydown} bind:value={power_values[index]} on:blur={() => parse_and_update_power(index, power_values[index])} on:input={event => handle_power_input(event, index)} class="focus:outline-none bg-black text-white text-center w-12"/>
                <div class="">kWh</div>
            </div>
            <div class="flex flex-col gap-1">
                <button on:click={() => add_setpoint(index)} disabled={add_setpoint_disabled[index]} class="bg-white hover:bg-amber-700 disabled:bg-gray-500 disabled:hover:bg-gray-500 min-h-4 min-w-4"/>
                <button on:click={() => remove_setpoint(index)} disabled={remove_setpoint_disabled[index]} class="bg-white rounded-xl hover:bg-amber-700 disabled:bg-gray-500 disabled:hover:bg-gray-500 min-h-4 min-w-4"/>
            </div>
        {/each}
    </div>
    <div class="flex flex-row gap-2 items-center">
        <!-- <button on:click={show_chart} class="stroke-white transition w-8 hover:stroke-amber-700 transition"><ChartIcon /></button> -->
        <button on:click={on_delete} class="fill-white transition w-8 hover:fill-amber-700 transition"><TrashIcon /></button>
        <button on:click={reset} class="fill-white transition w-8 hover:fill-amber-700 transition"><ResetIcon /></button>
    </div>
</div>