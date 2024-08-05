<script lang="ts">
    import DailySchedule from "./daily_schedule.svelte";
    import PowerSchedule from "./schedule";
    import Weekday from "./weekday";
    import { TimeInterval } from "$lib/time_intervals";
    import {available_days} from "$lib/store";

    let schedules:PowerSchedule[] = [];
    $available_days = [Weekday.Default, Weekday.Mon, Weekday.Tue, Weekday.Wed, Weekday.Thu, Weekday.Fri, Weekday.Sat, Weekday.Sun];

    function remove_schedule(index: number) {
        schedules = [
            ...schedules.slice(0, index),
            ...schedules.slice(index + 1)
        ];
    }

    function add_schedule() {
        let schedule = new PowerSchedule();
        if (schedules.length > 0) {
            schedule.Interval = schedules[schedules.length - 1].Interval;
            schedule.Schedule = schedules[schedules.length - 1].Schedule;
        }
        schedules.push(schedule);
        schedules = [...schedules];
        console.log(schedules);
    }
</script>

<div class="flex flex-col w-5/6 mx-auto gap-8 h-full">
    <div class="w-full flex flex-row place-content-center p-4 mt-10 border-2 text-2xl">Weekly Schedule</div>
    {#each schedules as schedule, index}
        <div class="w-full h-fit flex flex-col gap-4">
            <DailySchedule schedule={schedule} on_delete={() => remove_schedule(index)}/>
        </div>
    {/each}
    <button on:click={add_schedule} class="text-center text-2xl border-2 p-4 w-fit">Add Schedule</button>
</div>