<script>
    import { register } from '../../api/auth/auth.js';
    import "../../input.css";
    import { goto } from "$app/navigation";
    import {addMessage} from "../../stores/global_stores.js";
    import Notification from "$lib/components/messages/Notification.svelte";
    import Footer from '$lib/components/Footer.svelte';
    import Logo from '$lib/images/Logo.png';

    let email = '';
    let salutation = '';
    let firstName = '';
    let lastName = '';
    let dateOfBirth = '';
    let phoneNumber = '';
    let streetAndNumber = '';
    let postalCode = '';
    let city = '';
    let country = '';
    let password = '';

    const handleRegister = async () => {
        try {
            await register(email, salutation, firstName, lastName, password, dateOfBirth, phoneNumber, streetAndNumber, postalCode, city, country);

            addMessage({ type: 'success', text: 'Registration succeeded'});
            await goto('/login');
        } catch (error) {
            addMessage({ type: 'error', text: error.message || 'Registration failed'});
        }
    };
</script>

<head>
    <title>Register</title>
</head>

<Notification/>
<div class="">
    <a href="/">
        <img src={Logo} alt="Logo" class="w-14 md:w-16 lg:w-20 mt-8 ml-8 md:mb-6 lg:mb-0" />
    </a>
</div>
<div class="flex md:justify-center md:items-center min-h-screen md:-translate-y-16 -translate-y-5">
    <div class="max-w-xl w-full mx-auto p-4 md:p-12 md:border md:border-gray-100 md:rounded-2xl md:shadow-2xl md:mb-7">
        <h1 class="text-3xl font-bold mb-4 text-center">Register</h1>
        <form on:submit|preventDefault={handleRegister} class="space-y-4">
            <div>
                <label class="block text-gray-700 text-sm font-bold mb-1" for="email">Email:</label>
                <input
                        id="email"
                        type="email"
                        bind:value={email}
                        class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500"
                        required
                />
            </div>
            <div>
                <label class="block text-gray-700 text-sm font-bold mb-1" for="salutation">Salutation:</label>
                <select id="Salutation"
                    bind:value={salutation}
                    class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500"
                    required
                >
                    <option value="Mr.">Mr.</option>
                    <option value="Mrs.">Mrs.</option>
                    <option value="Mx.">Mx.</option>
                </select>
            </div>
            <div>
                <label class="block text-gray-700 text-sm font-bold mb-1" for="firstName">First Name:</label>
                <input
                        id="firstName"
                        type="text"
                        bind:value={firstName}
                        class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500"
                        required
                />
            </div>
            <div>
                <label class="block text-gray-700 text-sm font-bold mb-1" for="lastName">Last Name:</label>
                <input
                        id="lastName"
                        type="text"
                        bind:value={lastName}
                        class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500"
                        required
                />
            </div>
            <div>
                <label class="block text-gray-700 text-sm font-bold mb-1" for="dateOfBirth">Date of Birth:</label>
                <input
                        id="dateOfBirth"
                        type="date"
                        bind:value={dateOfBirth}
                        class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500"
                        required
                />
            </div>
            <div>
                <label class="block text-gray-700 text-sm font-bold mb-1" for="phoneNumber">Phone number:</label>
                <input
                        id="phoneNumber"
                        type="tel"
                        bind:value={phoneNumber}
                        class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500"
                        required
                />
            </div>
            <div>
                <label class="block text-gray-700 text-sm font-bold mb-1" for="streetAndNumber">Street and Number:</label>
                <input
                        id="streetAndNumber"
                        type="text"
                        bind:value={streetAndNumber}
                        class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500"
                        required
                />
            </div>
            <div>
                <label class="block text-gray-700 text-sm font-bold mb-1" for="postalCode">Postal Code:</label>
                <input
                        id="postalCode"
                        type="text"
                        bind:value={postalCode}
                        class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500"
                        required
                />
            </div>
            <div>
                <label class="block text-gray-700 text-sm font-bold mb-1" for="city">City:</label>
                <input
                        id="city"
                        type="text"
                        bind:value={city}
                        class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500"
                        required
                />
            </div>
            <div>
                <label class="block text-gray-700 text-sm font-bold mb-1" for="country">Country:</label>
                <input
                        id="country"
                        type="text"
                        bind:value={country}
                        class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500"
                        required
                />
            </div>
            <div>
                <label class="block text-gray-700 text-sm font-bold mb-1" for="password">Password:</label>
                <input
                        id="password"
                        type="password"
                        bind:value={password}
                        class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500"
                        required
                        minlength="8"
                />
            </div>
            <button
                    type="submit"
                    class="w-full bg-black text-xl my-4 text-white font-bold py-2 rounded hover:bg-gray-500 focus:outline-none focus:bg-gray-500"
            >
                Register
            </button>
        </form>
        <p class="pt-5 text-center">Already have an account? <a href="/login" class="text-blue-400">Log in here</a></p>
    </div>
</div>

<Footer/>