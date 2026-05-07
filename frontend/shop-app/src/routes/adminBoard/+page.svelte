<script>
    import "../../input.css";
    import { onMount } from "svelte";
    import { sendEmail} from "../../api/email/email.js";
    import {getAllUsers, getUserInfo} from "../../api/auth/auth.js";
    import {addMessage} from "../../stores/global_stores.js";
    import Notification from "$lib/components/messages/Notification.svelte";
    import {setCsrfToken, setUserInfo} from "$lib";
    import { user } from "../../stores/global_stores.js";
    import Header from "$lib/components/Header.svelte";

    let users = [];
    let selectedUserEmail = "";
    let subject = "";
    let message = "";
    let filteredUsers = [];
    let searchQuery = '';
    let isSuperuser = {isSuperuser: false, isStaff: false};

    async function collectAllUsers() {
        users = await getAllUsers();
        filteredUsers = users;
    }

    function filterUsers() {
        if (searchQuery === '') {
            filteredUsers = users;
        } else {
            filteredUsers = users.filter(user =>
                user.email.toLowerCase().includes(searchQuery.toLowerCase())
            );
        }
    }

    function clearSearch() {
        searchQuery = '';
        filterUsers();
    }

    async function handleSendEmail() {
        if (!selectedUserEmail || !subject || !message) {
            addMessage({text: 'Please fill out all required fields'});
            return;
        }

        try {
            await sendEmail(selectedUserEmail, subject, message);
            addMessage({ type: 'success', text: `Email was sent to ${selectedUserEmail}`});
            selectedUserEmail = "";
            subject = "";
            message = "";
        } catch (error) {
            addMessage({ type: 'error', text: 'Error while sending email ' + (error.message || 'Unknown error')});
        }
    }

    onMount(async () => {
        setCsrfToken();
        let tmpUser = await getUserInfo();
        isSuperuser.isSuperuser = tmpUser.is_superuser;
        isSuperuser.isStaff = tmpUser.is_staff;
        await collectAllUsers();
    });
</script>

<head>
    <title>Admin Board</title>
</head>

<Notification />
<Header title="Admin Board"/>
<div id="content" class="">
    <div class="m-5 pb-2 md:m-10">
        <h1 class="text-2xl font-bold pb-2">Management tools:</h1>
        <div class="flex flex-col md:flex-row space-y-4 md:space-y-0 md:space-x-8 p-4 relative place-content-around">
            <a href="/adminBoard/manageUsers" class="bg-gray-200 hover:bg-gray-300 font-bold py-2 px-4 rounded-3xl text-xl">
                Manage users
            </a>
            <a href="/adminBoard/manageProducts" class="bg-gray-200 hover:bg-gray-300 font-bold py-2 px-4 rounded-3xl text-xl">
                Manage products
            </a>
            <a href="/adminBoard/manageOrders" class="bg-gray-200 hover:bg-gray-300 font-bold py-2 px-4 rounded-3xl text-xl">
                Manage orders
            </a>
        </div>
        {#if isSuperuser.isSuperuser || isSuperuser.isStaff}
        <h1 class="text-2xl font-bold pb-2">New email:</h1>
        <div class="flex flex-col bg-gray-200 rounded-xl p-4 space-y-4">

            <div class="relative p-4 self-center w-10/12">
                <input
                    type="text"
                    class="bg-white rounded-lg px-4 py-3 w-full"
                    placeholder="First Search by email, then select user via dropdown..."
                    bind:value={searchQuery}
                    on:input={filterUsers}
                />
                {#if searchQuery}
                <button
                        class="absolute ml-2 text-black font-bold text-xl focus:outline-none top-1/2 transform -translate-y-1/2"
                        on:click={clearSearch}
                >
                    ⨉
                </button>
                {/if}
            </div>

            <select bind:value={selectedUserEmail} class="bg-white rounded-lg px-4 py-2 w-full">
                <option value="">Mail to user</option>
                {#each filteredUsers as user}
                    <option value={user.email}>{user.email}</option>
                {/each}
            </select>

            <input
                    type="text"
                    class="bg-white rounded-lg px-4 py-2 w-full"
                    placeholder="Subject"
                    bind:value={subject}
            />

            <textarea
                    class="bg-white rounded-lg px-4 py-2 w-full"
                    placeholder="Message"
                    bind:value={message}
            ></textarea>

            <button
                    class="bg-green font-bold py-2 px-4 rounded-lg hover:bg-green-hover"
                    on:click={handleSendEmail}
            >
                Send Email
            </button>
        </div>
        {/if}
    </div>
</div>
