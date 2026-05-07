<script>
	import { goto } from '$app/navigation';
    import { login } from '../../api/auth/auth.js'
    import "../../input.css";
    import {userId, addMessage} from "../../stores/global_stores.js";
    import Notification from "$lib/components/messages/Notification.svelte";
    import Footer from '$lib/components/Footer.svelte';
    import Logo from '$lib/images/Logo.png';

    let email = '';
    let password = '';

    async function handleSubmit() {
        try {
            const response = await login(email, password);
            $userId = response.user_id;
            await goto('/');
            addMessage({ type: 'success', text: 'Successfully logged in' });
        } catch (error) {
            addMessage({ type: 'error', text: error.message || 'Login failed' });
        }
    }
</script>

<head>
    <title>Login</title>
</head>

<Notification />
<div class="flex flex-col md:justify-center md:items-center min-h-screen md:-translate-y-20">
    <div class="mt-4 self-center z-0">
        <a href="/">
            <img src={Logo} alt="Logo" class="w-16 md:w-20 lg:w-24 m-8 z-0" />
        </a>
    </div>
    <div class="max-w-lg w-full mx-auto p-4 md:p-12 md:border md:border-gray-100 bg-white md:rounded-2xl md:shadow-2xl z-20">
        <h1 class="text-3xl font-bold mb-4 text-center">Login</h1>
        <form on:submit|preventDefault={handleSubmit}>
            <div class="mb-4">
                <label for="email" class="block mb-2 font-bold">Email:</label>
                <input type="email" id="email" bind:value={email} required class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500"/>
            </div>
            <div class="mb-4">
                <label for="password" class="block mb-2 font-bold">Password:</label>
                <input type="password" id="password" bind:value={password} required class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500" />
            </div>
            <button type="submit" class="w-full p-2 mt-3 bg-black hover:bg-gray-500 text-white rounded font-bold text-xl">Login</button>
            <p class="mt-5 text-center">You don't have an account yet? <a href="/register" class="text-blue-400">Register here</a></p>
        </form>
    </div>
</div>

<Footer/>