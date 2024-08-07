<script lang="ts">
    import ScheduleChart from "./schedule_chart.svelte";
    import CogIcon from "$lib/icons/cog_icon.svelte";
    import DeleteIcon from "$lib/icons/delete_icon.svelte";
    import {TimeInterval} from "$lib/time_intervals";
	import type PowerSchedule from "./schedule";
	import { chart_schedule } from "$lib/store";


    export let power_schedule:PowerSchedule;
    let propagate_drag_forward = true;
	let smart_propagation = true;
    let step_size = 5;
    let interval: TimeInterval;

    $: interval = power_schedule.interval;
    $: smart_propagation = propagate_drag_forward ? smart_propagation : false;
</script>

<div class="flex flex-col w-full h-full mx-auto transition text-nowrap gap-5">
    <div class="flex flex-row gap-5 mt-10 w-full">
        <div class="flex-grow text-2xl text-center border-2 border-white p-4">Daily Schedule</div>
        <button class="flex flex-row items-center justify-center border-2 border-gray-500 w-20 hover:border-white transition stroke-gray-500 hover:stroke-white" on:click={() => $chart_schedule = null}>
            <div class="w-10">
                <DeleteIcon />
            </div>
        </button>
    </div>
    <div class="flex flex-row h-fit gap-5 text-xl">
        <div class="flex flex-row w-fit">
            <div class="text-black bg-white text-center px-2">Step Size</div>
            <input class="border border-gray-600 hover:border-white focus:border-white focus:text-white hover:text-white text-gray-600 transition bg-transparent focus:outline-none w-12 text-center" type="text" bind:value={step_size}/>
            <div class="">
            </div>
        </div>
        <div class="flex flex-row w-fit text-gray-600">
            <div class="text-black text-center text-nowrap bg-white text-center px-2">Propagate Drag Forward</div>
            <button on:click={() => propagate_drag_forward = true} class="w-12 text-nowrap text-center border hover:border-white hover:text-white transition {propagate_drag_forward ? "border-white text-white" : "border-gray-500"}">On</button>
            <button on:click={() => propagate_drag_forward = false} class="w-12 text-nowrap text-center border hover:border-white hover:text-white transition {!propagate_drag_forward ? "border-white text-white" : "border-gray-500"}">Off</button>
        </div>
        <div class="flex flex-row w-fit text-gray-600">
            <div class="text-black text-center text-nowrap bg-white text-center px-2">Smart Propagation</div>
            <button on:click={() => smart_propagation = true} class="w-12 text-nowrap text-center border hover:border-white hover:text-white transition {smart_propagation ? "border-white text-white" : "border-gray-500"}">On</button>
            <button on:click={() => smart_propagation = false} class="w-12 text-nowrap text-center border hover:border-white hover:text-white transition {!smart_propagation ? "border-white text-white" : "border-gray-500"}">Off</button>
        </div>
    </div>
    <div class="w-full h-full border-2 border-white p-10 mb-10">
        <ScheduleChart propagate_drag_forward={propagate_drag_forward} smart_propagation={smart_propagation} step_size={step_size}/>
    </div>
</div>