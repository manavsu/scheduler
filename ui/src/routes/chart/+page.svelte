<script lang="ts">
    import ScheduleChart from "./schedule_chart.svelte";
    import CogIcon from "$lib/icons/cog_icon.svelte";
    import DeleteIcon from "$lib/icons/delete_icon.svelte";
    import {TimeInterval} from "$lib/time_intervals";

    let settings_visible = false;
    let propagate_drag_forward = true;
	let smart_propagation = true;
    let step_size = 5;
    let interval = TimeInterval.ONE_HOUR;
    $: smart_propagation = propagate_drag_forward ? smart_propagation : false;
</script>


<div class:blur-sm={settings_visible} class="flex flex-col w-2/3 h-full items-center mx-auto transition">
    <div class="flex flex-rol w-full h-40 items-center">
        <div class="text-3xl flex-grow text-center pl-10">Daily Schedule</div>
        <button class="h-10 w-10 fill-gray-500 hover:fill-white" on:click={() => settings_visible = true}>
            <CogIcon />
        </button>
    </div>
    <div class="w-full">
        <ScheduleChart propagate_drag_forward={propagate_drag_forward} smart_propagation={smart_propagation} step_size={step_size} intervals={interval}/>
    </div>
</div>

{#if settings_visible}
    <div class="fixed inset-0 z-10"></div>
    <div class="fixed inset-40 flex flex-col overflow-auto bg-black border-white border-2 z-20 mx-auto gap-5 pl-10">
        <div class="flex flex-row items-center justify-between m-5">
            <div class="text-2xl flex-grow text-center pl-15">Settings</div>
            <button class="w-5 h-5 stroke-gray-500 hover:stroke-white" on:click={() => settings_visible = false}>
                <DeleteIcon />
            </button>
        </div>
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
        <div class="flex flex-row w-fit text-gray-600">
            <div class="text-black text-center text-nowrap bg-white text-center px-2">Interval</div>
            <button on:click={() => interval = TimeInterval.ONE_HOUR} class="w-24 text-nowrap text-center border hover:border-white hover:text-white transition {interval == TimeInterval.ONE_HOUR ? "border-white text-white" : "border-gray-500"}">1 Hour</button>
            <button on:click={() => interval = TimeInterval.FIFTEEN_MINUTES} class="w-24 text-nowrap text-center border hover:border-white hover:text-white transition {interval == TimeInterval.FIFTEEN_MINUTES ? "border-white text-white" : "border-gray-500"}">15 Minutes</button>
            <button on:click={() => interval = TimeInterval.FIVE_MINUTES} class="w-24 text-nowrap text-center border hover:border-white hover:text-white transition {interval == TimeInterval.FIVE_MINUTES ? "border-white text-white" : "border-gray-500"}">5 Minutes</button>
        </div>
    </div>
{/if}