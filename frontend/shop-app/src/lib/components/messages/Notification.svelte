<script>
    import { messageStore } from '../../../stores/global_stores.js';
    let messages = [];

    $: messageStore.subscribe(value => {
        messages = value;
    });

</script>

<div class="fixed top-4 left-1/2 transform -translate-x-1/2 z-50 space-y-2">
    {#each messages as message}
        <div class="p-4 rounded-lg shadow-lg text-white text-center {message.type === 'success' ? 'bg-green-400' : message.type === 'error' ? 'bg-red-400' : 'bg-blue-400'}">
            {message.text}
        </div>
    {/each}
</div>
