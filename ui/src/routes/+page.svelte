<script lang="ts">
    import DailySchedule from "./daily_schedule.svelte";
    import PowerSchedule from "./schedule";
    import Weekday from "./weekday";
    import { TimeInterval } from "$lib/time_intervals";
    import {available_days, chart_schedule} from "$lib/store";
    import {BaseUrl as BASE_URL} from "$lib/config";
    import Time from "./time";
    import Chart from "./chart.svelte";
	import { onMount } from "svelte";

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
            schedule.interval = schedules[schedules.length - 1].interval;
            schedule.schedule = schedules[schedules.length - 1].schedule;
        }
        schedules.push(schedule);
        schedules = [...schedules];
        console.log(schedules);
    }

    async function load() {
        try {
            const response = await fetch(`${BASE_URL}/schedule/`);
            if (!response.ok) {
                throw new Error('Network response was not ok, status: ' + response.status + ' ' + await response.text());
            }
            const result = await response.json();
            console.log('Success:', result);
            for (let i = 0; i < result.length; i++) {
                let sch: {time: Time, value: number}[] = []
                result[i].schedule.forEach((s:any) => {
                    sch.push({time: new Time(s.time.hour, s.time.minute), value: s.value});
                });
                schedules.push(new PowerSchedule(sch, result[i].interval, result[i].days));
                $available_days = $available_days.filter((day) => !schedules[i].days.includes(day));
            }
            console.log(schedules);
            schedules = [...schedules];
        } catch (error) {
            console.error('Error:', error);
        }
    }

    async function save() {
        console.log((await fetch(`${BASE_URL}/`)).text());
        try {
            const response = await fetch(`${BASE_URL}/schedule/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(schedules)
            });

            if (!response.ok) {
                throw new Error('Network response was not ok, status: ' + response.status + ' ' + await response.text());
            }
            const result = await response.text();
            console.log('Success:', result);
        } catch (error) {
            console.error('Error:', error);
        }
    }

    onMount(() => {
        load();
    });
</script>

{#if $chart_schedule == null}
<div class="flex flex-col w-5/6 mx-auto gap-8 h-full">
    <div class="w-full flex flex-row place-content-center p-4 mt-10 border-2 text-2xl">Weekly Schedule</div>
    {#each schedules as schedule, index}
        <div class="w-full h-fit flex flex-col gap-4">
            <DailySchedule schedule={schedule} on_delete={() => remove_schedule(index)}/>
        </div>
    {/each}
    <div class="flex flex-row gap-4">
        <button on:click={add_schedule} class="text-center text-2xl border-2 p-4 w-fit hover:text-black hover:bg-white">Add Schedule</button>
        <button on:click={save} class="text-center text-2xl border-2 p-4 w-fit hover:text-black hover:bg-white">Save</button>
    </div>
</div>
{:else}
<div class="w-5/6 mx-auto h-full">
    <Chart power_schedule={$chart_schedule}/>
</div>
{/if}