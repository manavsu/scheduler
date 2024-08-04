<script>
    import DailySchedule from "./daily_schedule.svelte";
    
</script>

<div class="flex flex-col w-5/6 mx-auto gap-8 h-full">
    <div class="w-full flex flex-row place-content-center p-4 mt-10 border-2 text-2xl">Weekly Schedule</div>
    <div class="w-full flex flex-col gap-4 pb-2 scrollbar-thin scrollbar-thumb-white scrollbar-track-black overflow-auto">
        <DailySchedule />
    </div>
</div>