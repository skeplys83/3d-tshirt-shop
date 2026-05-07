<script>
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    function handleDelete() {
        dispatch('deleteProductThroughPopUp');
    }

    function handleClosePopUp() {
        dispatch('closePopup');
    }

    function handleClickOutside(event) {
        if (event.target.classList.contains('popup-overlay')) {
            dispatch('closePopup');
        }
    }
</script>

<!-- svelte-ignore a11y-no-static-element-interactions -->
<!-- svelte-ignore a11y-click-events-have-key-events -->
<div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 popup-overlay" on:click={handleClickOutside}>
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <div class="bg-white p-6 rounded-lg shadow-lg w-full max-w-3xl mx-4" on:click|stopPropagation>
        <h2 class="text-xl font-inter font-bold mb-4">Are you sure you want to delete the product?</h2>
        <p class="mb-6 font-inter">This step cannot be reversed!</p>
        <div class="flex flex-col justify-center items-center">
            <button class="hover:bg-gray-300 font-bold px-4 py-2 rounded-full mb-4 w-48" on:click={handleClosePopUp}>
                Cancel
            </button>
            <button class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-3xl w-48" on:click={handleDelete}>
                Yes, actually delete
            </button>
        </div>
    </div>
</div>
