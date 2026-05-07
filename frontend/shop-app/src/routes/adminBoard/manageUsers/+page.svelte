<script>
    import "../../../input.css";
    import { onMount } from "svelte";
    import { getAllUsers, patchUser, getUserInfo } from "../../../api/auth/auth.js";
    import { setCsrfToken } from "$lib";
    import { formatDate } from "$lib/globalFunctions/timeFormatting.js";
    import Notification from "$lib/components/messages/Notification.svelte";
    import { addMessage } from "../../../stores/global_stores";
    import Header from "$lib/components/Header.svelte";

    let users = [];
    let filteredUsers = [];
    let searchQuery = '';
    let isSuperuser;

    let isLoading = true;
    let isError = false;

    async function collectAllUsers() {
        users = await getAllUsers();
        filterUsers();
    }

    function filterUsers() {
        if (searchQuery === '') {
            filteredUsers = users;
        } else {
            filteredUsers = users.filter(user =>
                user.email.toLowerCase().includes(searchQuery.toLowerCase()) ||
                user.first_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                user.last_name.toLowerCase().includes(searchQuery.toLowerCase())
            );
        }
    }

    function clearSearch() {
        searchQuery = '';
        filterUsers();
    }

    async function updateIsStaff(userId, valueStaff, valueActive, firstName, lastName, email) {
        let isStaff = !valueStaff;
        try {
            await patchUser(userId, isStaff, valueActive, firstName, lastName, email);
            addMessage({ text: `Updated user: "${userId}" with new staff value: "${isStaff}"` });
        } catch (error) {
            addMessage({ type: 'error', text: error.message || 'Not enough permission or failed request' });
        }
        await collectAllUsers();
        filterUsers();
    }

    async function updateIsActive(userId, valueStaff, valueActive, firstName, lastName, email) {
        let isActive = !valueActive;
        try {
            await patchUser(userId, valueStaff, isActive, firstName, lastName, email);
            addMessage({ text: `Updated user: "${userId}" with new active value: "${isActive}"` });
        } catch (error) {
            addMessage({ type: 'error', text: error.message || 'Not enough permission or failed request' });
        }
        await collectAllUsers();
        filterUsers();
    }

    onMount(async () => {
        setCsrfToken();
        let tmpUser = await getUserInfo();
        isSuperuser = tmpUser.is_superuser;
        try {
            await collectAllUsers();
            isLoading = false;
            addMessage({ type: 'success', text: 'All users are loaded' });
        } catch (error) {
            isLoading = false;
            isError = true;
            addMessage({ type: 'error', text: error.message || 'Failed to load users' });
        }
    });

</script>

<head>
    <title>Admin Board - Manage users</title>
</head>

<Notification />
<Header title="Manage users"/>
<div id="content" class="bg-white w-full min-h-screen">
    <div id="Header" class="text-center">
        <div class="pt-2 mt-4">
            <input
                    type="text"
                    class="w-8/12 bg-gray-200 rounded-lg px-4 py-3"
                    placeholder="Search by email, first name or last name..."
                    bind:value={searchQuery}
                    on:input={filterUsers}
            />
            {#if searchQuery}
                <button
                        class="ml-2 text-black font-bold text-xl focus:outline-none"
                        on:click={clearSearch}
                >
                    ⨉
                </button>
            {/if}
        </div>

        <div class="pb-2 m-10 flex flex-col">
            {#if isLoading}
                <div class="flex space-x-2 justify-center items-center mt-10">
                    <div class='h-5 w-5 bg-black rounded-full animate-bounce [animation-delay:-0.3s]'></div>
                    <div class='h-5 w-5 bg-black rounded-full animate-bounce [animation-delay:-0.15s]'></div>
                    <div class='h-5 w-5 bg-black rounded-full animate-bounce'></div>
                </div>
            {:else if isError}
                <p class="text-center mt-10 font-bold text-xl text-red-600">Oops, something went wrong..</p>
            {:else if filteredUsers.length === 0}
                <p class="text-center mt-10 font-bold text-xl">No Users yet</p>
            {:else}
                {#each filteredUsers as user}
                    <div class="bg-gray-200 mb-2 rounded-xl p-4 grid grid-cols-1 xs:grid-cols-2 sm:grid-cols-6 gap-4 text-center items-center">
                        <div class="flex flex-col">
                            <span class="text-m">ID</span>
                            <span class="font-bold">{user.id}</span>
                        </div>
                        <div class="flex flex-col">
                            <span class="text-m">Email</span>
                            <span class="font-bold">{user.email}</span>
                        </div>
                        <div class="flex flex-col">
                            <span class="text-m">Name</span>
                            <span class="font-bold">{user.first_name} {user.last_name}</span>
                        </div>
                        <div class="flex flex-col">
                            <span class="text-m">Date of birth</span>
                            <span class="font-bold">{formatDate(user.date_of_birth)}</span>
                        </div>
                        <div class="flex flex-col">
                            <span class="text-m">Staff</span>
                            {#if isSuperuser}
                                {#if user.is_staff}
                                    <button on:click={() => updateIsStaff(user.id, user.is_staff, user.is_active, user.first_name, user.last_name, user.email)} class="font-bold p-2 pr-1 pl-1 bg-green hover:bg-green-hover rounded-xl">{user.is_staff}</button>
                                {:else}
                                    <button on:click={() => updateIsStaff(user.id, user.is_staff, user.is_active, user.first_name, user.last_name, user.email)} class="font-bold p-2 pr-1 pl-1 bg-red hover:bg-red-hover rounded-xl">{user.is_staff}</button>
                                {/if}
                            {:else}
                                <span class="font-bold">{user.is_staff}</span>
                            {/if}
                        </div>
                        <div class="flex flex-col">
                            <span class="text-m">Active</span>
                            {#if user.is_active}
                                <button on:click={() => updateIsActive(user.id, user.is_staff, user.is_active, user.first_name, user.last_name, user.email)} class="font-bold p-2 pr-1 pl-1 bg-green hover:bg-green-hover rounded-xl">{user.is_active}</button>
                            {:else}
                                <button on:click={() => updateIsActive(user.id, user.is_staff, user.is_active, user.first_name, user.last_name, user.email)} class="font-bold p-2 pr-1 pl-1 bg-red hover:bg-red-hover rounded-xl">{user.is_active}</button>
                            {/if}
                        </div>
                    </div>
                {/each}
            {/if}
        </div>
    </div>
</div>
