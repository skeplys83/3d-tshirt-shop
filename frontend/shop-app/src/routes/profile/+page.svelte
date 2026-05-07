<script>
    import "../../input.css";
    import { onMount } from "svelte";
    import { getUserInfo, updateUser } from "../../api/auth/auth";
    import {addMessage} from "../../stores/global_stores";
    import { getOrdersFromUser } from "../../api/orders/orders";
    import Notification from "$lib/components/messages/Notification.svelte";
    import { setCsrfToken } from "$lib";
    import { slide } from "svelte/transition";
    import { formatDate, formatDateTime } from "$lib/globalFunctions/timeFormatting";
    import Footer from "$lib/components/Footer.svelte";
    import Logo from "$lib/images/Logo.png";

    let user = [];
    let orders = [];
    let userID = "";
    let showEditForm = false;

    let isLoadingUser = true;
    let isLoadingOrders = true;
    let isErrorUser = false;
    let isErrorOrders = false;

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

    async function updateUserProfile() {
        try {
            const response = await updateUser(userID, email, salutation, firstName, lastName, dateOfBirth, phoneNumber, streetAndNumber, postalCode, city, country);
            addMessage({ type: 'success', text: 'Profile updated successfully' });
            showEditForm = false;
        } catch (error) {
            addMessage({ type: 'error', text: 'Failed to update profile: ' + (error.message || 'Unknown error') });
        }
        let userResponse = await getUserInfo();
        user = userResponse;
    }

    function toggleEditForm() {
        showEditForm = !showEditForm;
    }

    onMount( async () => {
        setCsrfToken();

        try {
            let userResponse = await getUserInfo();
            if (!userResponse || userResponse.error || userResponse == null || userResponse === undefined) {
                addMessage({ type: 'error', text: 'Error while loading profile'});
                isLoadingUser = false;
                isLoadingOrders = false;
                isErrorUser = true;
                isErrorOrders = true;
                return;
            }
            user = userResponse;
            userID = user.id;

            email = user.email;
            salutation = user.salutation;
            firstName = user.first_name;
            lastName = user.last_name;
            dateOfBirth = user.date_of_birth;
            phoneNumber = user.phone_number;
            streetAndNumber = user.street_and_number;
            postalCode = user.postal_code;
            city = user.city;
            country = user.country;

            isLoadingUser = false;

            try {
                let ordersResponse = await getOrdersFromUser(userID);
                orders = ordersResponse;
                isLoadingOrders = false;
                addMessage({ type: 'success', text: 'All orders are loaded'});
            } catch (error) {
                isLoadingOrders = false;
                isErrorOrders = true;
                addMessage({ text: 'You have no orders yet'});
            }
        } catch (error) {
            isLoadingUser = false;
            isErrorUser = true;
            addMessage({ type: 'error', text: error.message || 'No userinfo available'});
        }
    });

    function createImageUrl(base64String) {
        return `data:image/png;base64,${base64String}`;
    }

</script>

<head>
    {#if isLoadingUser || isErrorUser}
        <title>Profile</title>
    {:else}
        <title>{user.first_name}'s Profile</title>
    {/if}
</head>

<Notification />
<div id="content" class="bg-white w-full min-h-screen">
    <div class="flex flex-row items-center w-full">   
        <a href="/">
            <img src={Logo} alt="Logo" class="w-12 md:w-16 md:mt-8 md:ml-8 mt-3 ml-3" />
        </a>
        <div id="Header" class="text-center flex-grow mt-2 px-2">
            {#if isLoadingUser || isErrorUser || window.innerWidth < 768}
                <p class="text-3xl pt-6 font-bold">Profile</p>
            {:else}
                <p class="text-3xl pt-6 font-bold">{user.first_name}'s Profile</p>
            {/if}
        </div>
        <div class="w-12 md:w-16 md:mt-8 md:ml-8 mt-3 ml-3"></div>
    </div>
    <div class="m-5 pb-2 md:m-10">
        <h1 class="text-2xl font-bold pb-2">My details:</h1>
        <div class="bg-gray-200 rounded-xl shadow-lg flex flex-col space-y-4 md:space-y-0 p-4 relative">
            {#if isLoadingUser}
                <div class="flex flex-col md:flex-row space-y-4 md:space-y-0 md:space-x-6 animate-pulse">
                    <div class="flex-1 rounded-lg p-2">
                        <p class="font-semibold">Personal information:</p>
                        <div>
                            <div class="m-2 ml-4 text-l flex items-center">
                                <span class="mr-2">Name:</span>
                                <p class="ml-2 h-2 w-full max-w-36 bg-slate-600 rounded"></p>
                            </div>
                            <div class="m-2 ml-4 text-l flex items-center">
                                <span class="mr-2">Birth date:</span>
                                <p class="h-2 w-full max-w-32 bg-slate-600 rounded"></p>
                            </div>
                        </div>
                    </div>
                    <div class="flex-1 rounded-lg p-2">
                        <p class="font-semibold">Contact details:</p>
                        <div>
                            <div class="m-2 ml-4 text-l flex items-center">
                                <span class="mr-2">Email:</span>
                                <p class=" ml-2 h-2 w-full max-w-36 bg-slate-600 rounded"></p>
                            </div>
                            <div class="m-2 ml-4 text-l flex items-center">
                                <span class="mr-2">Phone:</span>
                                <p class="h-2 w-full max-w-36 bg-slate-600 rounded"></p>
                            </div>
                        </div>
                    </div>
                    <div class="flex-1 rounded-lg p-2">
                        <p class="font-semibold">Address:</p>
                        <div>
                            <div class="m-2 ml-4 text-l flex items-center">
                                <span class="mr-2 text-gray-200">X</span>
                                <p class="h-2 w-full max-w-36 bg-slate-600 rounded -translate-x-4"></p>
                            </div>
                            <div class="m-2 ml-4 text-l flex items-center">
                                <span class="mr-2 text-gray-200">X</span>
                                <p class="h-2 w-full max-w-36 bg-slate-600 rounded -translate-x-4"></p>
                            </div>
                            <div class="m-2 ml-4 text-l flex items-center">
                                <span class="mr-2 text-gray-200">X</span>
                                <p class="h-2 w-full max-w-36 bg-slate-600 rounded -translate-x-4"></p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="flex justify-end mt-auto">
                    <button class="bg-black hover:bg-gray-500 text-white font-bold py-2 px-4 rounded-3xl pointer-events-none cursor-not-allowed opacity-50">
                        {showEditForm ? 'Cancel' : 'Edit Profile'}
                    </button>
                </div>
            {:else if isErrorUser}
                <p class="text-center mt-5 mb-4 font-bold text-l text-red-600">Oops, something went wrong with your profile..</p>
            {:else}
                <div class="flex flex-col md:flex-row space-y-4 md:space-y-0 md:space-x-6">
                    <div class="flex-1 rounded-lg p-2">
                        <p class="font-semibold">Personal information:</p>
                        <div>
                            <p class="m-2 ml-4 text-l">Name: {user.salutation} {user.first_name} {user.last_name}</p>
                            <p class="m-2 ml-4 text-l">Birth date: {formatDate(user.date_of_birth)}</p>
                        </div>
                    </div>
                    <div class="flex-1 rounded-lg p-2">
                        <p class="font-semibold">Contact details:</p>
                        <div>
                            <p class="m-2 ml-4 text-l">Email: {user.email}</p>
                            <p class="m-2 ml-4 text-l">Phone: {user.phone_number}</p>
                        </div>
                    </div>
                    <div class="flex-1 rounded-lg p-2">
                        <p class="font-semibold">Address:</p>
                        <div>
                            <p class="m-2 ml-4 text-l">{user.street_and_number}</p>
                            <p class="m-2 ml-4 text-l">{user.postal_code}, {user.city}</p>
                            <p class="m-2 ml-4 text-l pb-2">{user.country}</p>
                        </div>
                    </div>
                </div>
                <div class="flex justify-end mt-auto">
                    <button class="bg-black hover:bg-gray-500 text-white font-bold py-2 px-4 rounded-3xl" on:click={toggleEditForm}>
                        {showEditForm ? 'Cancel' : 'Edit Profile'}
                    </button>
                </div>
            {/if}
        </div>
        {#if showEditForm}
            <div class="bg-gray-100 rounded-lg shadow-lg p-4 mt-4" transition:slide>
                <h2 class="text-xl font-bold mb-4">Edit Profile</h2>
                <div class="space-y-4">
                    <select class="w-full p-2 border" bind:value={salutation} required>
                        <option value="Mr.">Mr.</option>
                        <option value="Mrs.">Mrs.</option>
                        <option value="Mx.">Mx.</option>
                    </select>
                    <input class="w-full p-2 border" type="text" bind:value={firstName} required placeholder="First Name" />
                    <input class="w-full p-2 border" type="text" bind:value={lastName} required placeholder="Last Name" />
                    <input class="w-full p-2 border" type="text" bind:value={email} required placeholder="Email" />
                    <input class="w-full p-2 border" type="text" bind:value={phoneNumber} required placeholder="Phone Number" />
                    <input class="w-full p-2 border" type="date" bind:value={dateOfBirth} required placeholder="Date of Birth" />
                    <input class="w-full p-2 border" type="text" bind:value={streetAndNumber} required placeholder="Street and Number" />
                    <input class="w-full p-2 border" type="text" bind:value={postalCode} required placeholder="Postal Code" />
                    <input class="w-full p-2 border" type="text" bind:value={city} required placeholder="City" />
                    <input class="w-full p-2 border" type="text" bind:value={country} required placeholder="Country" />
                </div>
                <button class="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded-3xl mt-4" on:click={updateUserProfile}>
                    Update User Profile
                </button>
            </div>
        {/if}
    </div>
    <div class="m-5 pb-2 md:m-10">
        <h1 class="text-2xl font-bold pb-2">My orders:</h1>
        {#if isLoadingOrders}
            <div class="flex space-x-2 justify-center items-center mt-5">
                <div class='h-5 w-5 bg-black rounded-full animate-bounce [animation-delay:-0.3s]'></div>
                <div class='h-5 w-5 bg-black rounded-full animate-bounce [animation-delay:-0.15s]'></div>
                <div class='h-5 w-5 bg-black rounded-full animate-bounce'></div>
            </div>
        {:else if isErrorOrders}
            <p class="text-center mt-5 font-bold text-l text-red-600">Oops, something went wrong with your Orders..</p>
        {:else if orders.length == 0}
            <p class="text-center mt-5 font-bold text-l">You have no orders yet</p>
        {:else}
            {#each orders as order}
                <div class="bg-gray-200 rounded-xl shadow-lg flex flex-col space-y-4 md:space-y-0 md:space-x-6 p-4 mb-6">
                    <div>
                        <p class="font-bold text-l">Order with ID {order.id} from {formatDateTime(order.created_at)}</p>
                    </div>
                    <div class="flex flex-col md:flex-row space-y-4 md:space-y-0 md:space-x-6">
                        <div class="flex-1 rounded-lg p-2">
                            <p class="font-semibold">Contact details:</p>
                            <div>
                                <p class="m-2 ml-4 text-l">Shipped to: {order.salutation} {order.first_name} {order.last_name}</p>
                                <p class="m-2 ml-4 text-l">Email: {order.email}</p>
                                <p class="m-2 ml-4 text-l">Phone: {order.phone_number}</p>
                            </div>
                        </div>
                        <div class="flex-1 rounded-lg p-2">
                            <p class="font-semibold">Delivery address:</p>
                            <div>
                                {#if order.differentShippingAddress == true}
                                    <p class="m-2 ml-4 text-l">{order.alternative_address.streetAndNumber}</p>
                                    <p class="m-2 ml-4 text-l">{order.alternative_address.postalCode}, {order.alternative_address.city}</p>
                                    <p class="m-2 ml-4 text-l pb-2">{order.alternative_address.country}</p>
                                {:else}
                                    <p class="m-2 ml-4 text-l">{order.street_and_number}</p>
                                    <p class="m-2 ml-4 text-l">{order.postal_code}, {order.city}</p>
                                    <p class="m-2 ml-4 text-l pb-2">{order.country}</p>
                                {/if}
                            </div>
                        </div>
                    </div>
                    <div>
                        <p class="font-bold text-xl md:-translate-x-4">Total Price: {order.totalPrice}</p>
                        {#if order.payedStatus}
                            <p class="md:-translate-x-4 pt-1">Payment Status: Payed</p>
                        {:else}    
                            <p class="md:-translate-x-4 pt-1">Payment Status: Not Payed</p>
                        {/if}               
                    </div>
                    <div>
                        <p class="pt-3 font-bold md:-translate-x-4">Purchased products:</p>
                        {#each order.selectedProducts as product, index}
                            <div class="flex flex-col md:flex-row space-y-4 md:space-y-0 md:space-x-6 pt-3">
                                <img src={createImageUrl(product.productPicture)} alt={product.name} class="w-24 h-24"/>
                                <div>
                                    <p>Name: {product.name}</p>
                                    <p>Size: {product.size}</p>
                                    <p>Quantity: {product.quantity}</p>
                                    <p>Rate: {product.price}</p>
                                </div>
                            </div>
                            {#if index < order.selectedProducts.length - 1}
                                <div id="Spacer" class="w-full bg-gray-400 h-0.5 mt-3"></div>
                            {/if}
                        {/each}
                    </div>
                    <div>
                        <p class="font-bold text-l md:-translate-x-4 pt-5">Current Order Status: {order.status}</p>
                    </div>
                </div>
            {/each}
        {/if}
    </div>
</div>

<Footer/>