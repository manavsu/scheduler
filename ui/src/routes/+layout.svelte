<script lang="ts">
    import "$lib/app.css";
    import { page } from '$app/stores';

    let path;
    $: path = $page.url.pathname
</script>

<style lang="postcss">
    :global(html) {
      @apply bg-black text-white caret-white;
    }
</style>

<div class="flex-grow h-dvh overflow-auto w-full border-2">
  <slot />
</div>