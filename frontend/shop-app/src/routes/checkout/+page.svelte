<script>
    import "../../input.css";
    import UpAndDownArrow from '$lib/images/down-arrow.png';
    import { createCheckoutSession } from "../../api/checkout/checkout.js";
    import { onMount } from "svelte";
    import { getProducts } from "../../api/products/products.js";
    import { addMessage } from "../../stores/global_stores.js";
    import Notification from "$lib/components/messages/Notification.svelte";
    import { setCsrfToken } from "$lib";
    import { getUserInfo } from '../../api/auth/auth';
    import { login } from '../../api/auth/auth.js';
    import { scale } from "svelte/transition";
    import { slide } from "svelte/transition";
    import Header from "$lib/components/Header.svelte";
    import Footer from "$lib/components/Footer.svelte";

    let products = [];
    let cart = [];
    let user = {};
    let totalPrice = 0;
    let readyforPayment = false;
    let termsAccepted = false;
    let differentShippingAddress = false;
    let showLegalSection = false;
    let editMode = true;
    let emailError = '';
    let errorMessageStock = '';
    let userAuthenticated = false;
    let selectLoginOrPrefill = true;

    let loginEmail = '';
    let password = '';

    let salutation = '';
    let firstName = '';
    let lastName = '';
    let email = '';
    let confirmEmail = '';
    let phoneNumber = '';
    let streetAndNumber = '';
    let city = '';
    let postalCode = '';
    let country = '';
    let alternativeStreetAndNumber = '';
    let alternativeCity = '';
    let alternativePostalCode = '';
    let alternativeCountry = '';

    let rotation = 0;
    let customerInformation;
    let moveUpCustomerInformation;
    let LoginArea;
    let legalRequirements;

    if (typeof window !== 'undefined') {
        cart = JSON.parse(localStorage.getItem("cart")) || [];
    }

    const calculateTotalPrice = () => {
        totalPrice = cart.reduce((total, item) => total + item.quantity * parseFloat(item.price), 0).toFixed(2);
    };

    const increaseQuantity = (item) => {
        errorMessageStock = "";
        const existingProduct = cart.find(cartItem => cartItem.id === item.id && cartItem.size === item.size);

        if (existingProduct) {
            // Get the available stock for the item from the products list
            const product = products.find(p => p.id === item.id);
            const availableStock = product.stock[item.size];

            // Check if adding one more would exceed the stock
            if (existingProduct.quantity + 1 <= availableStock) {
                existingProduct.quantity += 1;
                updateCart();
            } else {
                errorMessageStock = `There are just ${availableStock} pieces in size ${item.size} available.`;
            }
        }
    };

    const decreaseQuantity = (item) => {
        errorMessageStock = "";
        const existingProduct = cart.find(cartItem => cartItem.id === item.id && cartItem.size === item.size);
        if (existingProduct) {
            if (existingProduct.quantity > 1) {
                existingProduct.quantity -= 1;
                item.stock[item.size] += 1; // Increase stock on decrease
            } else {
                cart = cart.filter(cartItem => cartItem.id !== existingProduct.id || cartItem.size !== existingProduct.size);
            }
            updateCart();
        }
    };

    const updateCart = () => {
        if (typeof window !== 'undefined') {
            localStorage.setItem("cart", JSON.stringify(cart));
        }
        cart = [...cart];
        calculateTotalPrice();
    };

    async function collectCheckoutItems() {
        let products = JSON.parse(localStorage.getItem("cart"));

        if (!products || products.length === 0) {
            addMessage({ type: 'error', text: 'There are no products in cart'});
            return [];
        }

        let lineItems = products.map(product => {
            return {
                price: product.stripePriceId,
                quantity: product.quantity
            };
        });

        return lineItems;
    }

    async function handleSubmit() {
        let collectedProducts = await collectCheckoutItems();
        
        try {
            const order = {
                salutation,
                firstName,
                lastName,
                email,
                phoneNumber,
                streetAndNumber,
                city,
                postalCode,
                country,
                differentShippingAddress,
                alternativeAddress: {
                    streetAndNumber: alternativeStreetAndNumber,
                    city: alternativeCity,
                    postalCode: alternativePostalCode,
                    country: alternativeCountry
                },
                termsAccepted,
                totalPrice,
                selectedProducts: cart,
                line_items: collectedProducts
            };

            console.log("Order vor dem Abschicken: ", order);

            await createCheckoutSession(order);
        } catch (error) {
            addMessage({ type: 'error', text: 'Error while processing payment: ' + (error.message || 'Unknown error')});
        }
    }

    const handleTermsAndConditionsCheckboxChange = (event) => {
        termsAccepted = event.target.checked;
        readyforPayment = termsAccepted && cart.length > 0;
    };

    const handleNext = () => {
        const form = document.querySelector('#customerInformation');

        if (form.checkValidity()) {
            if (email !== confirmEmail) {
                emailError = 'The email addresses do not match. Please make sure they are the same.';
                return;
            }

            emailError = '';
            rotation += 180;
            
            if (editMode) {
                showLegalSection = true;
                editMode = false;
                legalRequirements.scrollIntoView({ behavior: 'smooth' });
            } else {
                editMode = true;
                showLegalSection = false;
                moveUpCustomerInformation.scrollIntoView({ behavior: 'smooth' });
            }
        } else {
            form.reportValidity();
        }
    };

    async function handleLogin() {
        try {
            const response = await login(loginEmail, password);
            selectLoginOrPrefill = true;
            location.reload();
            addMessage({ type: 'success', text: 'Successfully logged in'});
        } catch (error) {
            addMessage({ type: 'error', text: error.message || 'Login failed'});
        }
    }

    const handleContinueAsGuest = () => {
        selectLoginOrPrefill = false;
        editMode = true;
        customerInformation.scrollIntoView({ behavior: 'smooth' });
    };

    const handlePrefillFields = () => {
        try {
            salutation = user.salutation;
            firstName = user.first_name;
            lastName = user.last_name;
            email = user.email;
            confirmEmail = user.email;
            phoneNumber = user.phone_number;
            streetAndNumber = user.street_and_number;
            city = user.city;
            country = user.country;
            postalCode = user.postal_code;
        } catch (error) {
            addMessage({ type: 'error', text: 'Error while prefilling fields: ' + (error.message || 'Unknown error')});
        }
        selectLoginOrPrefill = false;
        customerInformation.scrollIntoView({ behavior: 'smooth' });
    };

    const handleFillOutManual = () => {
        selectLoginOrPrefill = false;
        customerInformation.scrollIntoView({ behavior: 'smooth' });
    };

    const handleBackToLogin = () => {
        selectLoginOrPrefill = true;
        LoginArea.scrollIntoView({ behavior: 'smooth' });
    };

    onMount(async () => {
        setCsrfToken();

        try {
            let userResponse = await getUserInfo();

            let skipUserAuthentication = false;
            
            if (!userResponse || userResponse.error || userResponse == null || userResponse === undefined) {
                skipUserAuthentication = true;
                userAuthenticated = false;
            }

            if(!skipUserAuthentication){
                userAuthenticated = true;
                user = userResponse;
            }
        } catch (error) {
            userAuthenticated = false;
        }

        try {
            let tmp = await getProducts();
            if (tmp) {
                products = tmp;
            }
        } catch (error) {
            addMessage({ type: 'error', text: 'No products available: ' + (error.message || 'Unknown error')});
        }
        calculateTotalPrice();
    });

    function createImageUrl(base64String) {
        return `data:image/png;base64,${base64String}`;
    }

</script>

<head>
    <title>Checkout</title>
</head>

<Notification />
<Header title="Checkout"/>
<div id="content" class="overflow-hidden">
        <div class="m-5 pb-2 md:m-10">
            <h1 class="text-2xl font-bold pb-2">Shopping basket:</h1>
            <div class="bg-gray-200 rounded-xl shadow-lg flex flex-col space-y-4 md:space-y-0 relative">
                <div class="pt-8 pb-8">
                    {#if cart.length === 0}
                        <p class="text-lg text-center font-bold">Your shopping basket is empty.</p>
                    {:else}
                        <div class="flex flex-col space-y-2 mr-4 ml-4">
                            {#each cart as item}
                                <div class="flex flex-col md:flex-row md:justify-between md:items-center border-b-2 border-gray-400 pb-2">
                                    <div class="flex flex-row md:space-x-6 md:space-y-0 space-y-4 pt-3">
                                        <img src={createImageUrl(item.productPicture)} alt={item.name} class="w-24 h-24 pb-2"/>
                                        <div class="pl-2 md:pl-0">
                                            <p class="font-bold">{item.name}</p>
                                            <p>Size: {item.size}</p>
                                            <p>Quantity: {item.quantity}</p>
                                        </div>
                                    </div>
                                    <div class="flex items-center mt-4 md:mt-0">
                                        <button 
                                            on:click={() => decreaseQuantity(item)} 
                                            class="text-gray-500 font-bold hover:bg-gray-400 w-9 h-9 rounded-full border-1 border-gray-500">
                                            -
                                        </button>
                                        <span class="px-2">{item.quantity}</span>
                                        <button 
                                            on:click={() => increaseQuantity(item)} 
                                            class="text-gray-500 font-bold hover:bg-gray-400 w-9 h-9 rounded-full border-1 border-gray-500">
                                            +
                                        </button>
                                    </div>
                                    <div class="text-right ml-4 mt-4 md:mt-0">
                                        <p>${item.price} each</p>
                                        <p class="font-bold">Total: ${(item.quantity * item.price).toFixed(2)}</p>
                                    </div>
                                </div>
                            {/each}
                        </div>
                    {/if}
                    {#if errorMessageStock}
                        <p class="text-center text-red-600 pt-3">{errorMessageStock}</p>
                    {/if}
                </div>
                <div class="flex justify-between items-center p-4 pt-0 relative">
                    <p class="font-bold text-lg">Total Price: {totalPrice}€</p>
                </div>
            </div>
        </div>

        <div class={`m-5 pb-2 md:m-10 ${(!selectLoginOrPrefill || totalPrice == 0.00) ? 'opacity-50 pointer-events-none' : ''}`} bind:this={LoginArea}>
            {#if userAuthenticated}
                <p class="text-2xl font-bold pb-2">You are already logged in!</p>
                <div class="bg-gray-200 rounded-xl shadow-lg flex flex-col space-y-4 md:space-y-0 relative p-5">
                    <p class="">Would you like to use your customer information from the profile and pre-fill it directly?</p>
                    <div class="pt-4 flex flex-col items-center">
                        <button on:click={handlePrefillFields} class="bg-black hover:bg-gray-500 text-white px-8 py-3 rounded text-l font-bold mb-2 w-60">Yes</button>
                        <button on:click={handleFillOutManual} class="bg-black hover:bg-gray-500 text-white px-5 py-3 rounded text-l font-bold w-60">No, I will enter it manually</button>
                    </div>
                </div>
            {:else}
                <p class="text-2xl font-bold pb-2">How would you like to proceed?</p>
                <div class="flex flex-col md:flex-row md:space-x-5 bg-gray-200 rounded-xl shadow-lg p-5">
                    <div id="Login" class="md:w-1/2">
                        <p class="text-xl font-bold">Already have a profile? </p>
                        <form on:submit|preventDefault={handleLogin}>
                            <div class="mb-4 mt-3">
                                <label for="loginEmail" class="block mb-2 font-bold">Email:</label>
                                <input type="email" id="loginEmail" bind:value={loginEmail} required class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500" />
                            </div>
                            <div class="mb-4">
                                <label for="password" class="block mb-2 font-bold">Password:</label>
                                <input type="password" id="password" bind:value={password} required class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500" />
                            </div>
                            <button type="submit" class="w-full bg-black text-xl my-2 text-white font-bold py-2 rounded hover:bg-gray-500 focus:outline-none focus:bg-gray-500">Login</button>
                            <p class="pt-3 text-center">You don't have an account yet? <a href="/register" class="text-blue-400">Register here</a></p>
                        </form>
                    </div>
                    <!-- Horizontale Trennungslinie für mobile View -->
                    <hr class="block md:hidden my-5 border-gray-300">
                    <!-- Vertikale Trennungslinie für Web View -->
                    <div class="hidden md:block w-px bg-gray-300"></div>
                    <div class="md:w-1/2 flex items-center justify-center mt-5 md:mt-0">
                        <button on:click={handleContinueAsGuest} class="py-2 px-5 bg-black text-white rounded hover:bg-gray-500 text-xl font-bold">Continue as a guest</button>
                    </div>
                </div>    
            {/if}
        </div>

        {#if !selectLoginOrPrefill}
            <div class="flex justify-center mt-5" bind:this={moveUpCustomerInformation}>
                <div class="flex-col">
                    <!-- svelte-ignore a11y-click-events-have-key-events -->
                    <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
                    <img 
                        src={UpAndDownArrow}
                        alt="Arrow" 
                        class={`w-16 h-16 bg-black p-3 rounded-full object-cover rotate-180 hover:bg-gray-500 ${(!editMode || cart.length === 0 || selectLoginOrPrefill) ? 'opacity-50 pointer-events-none' : ''}`} 
                        on:click={handleBackToLogin} 
                        in:scale={{ duration: 300, start: 0.5 }} 
                        out:scale={{ duration: 300, end: 0.5 }}
                    />
                    <p class="text-center pt-2 opacity-80 font-bold">Step back</p>
                </div>
            </div>
        {/if}
               

        <div class={`m-5 pb-2 md:m-10 ${(!editMode || cart.length === 0 || selectLoginOrPrefill) ? 'opacity-50 pointer-events-none' : ''}`} bind:this={customerInformation}>
            <p class="text-2xl font-bold pb-2">Customer information:</p>
            <div class="bg-gray-200 rounded-xl shadow-lg flex flex-col space-y-4 md:space-y-0 relative p-5">
            <div class="flex flex-col space-y-2">
                <form id="customerInformation" class="flex flex-col px-2 pt-2" on:submit|preventDefault={handleNext}>
                    <div class="md:my-2">
                        <label class="block text-gray-700 text-sm font-bold mb-1 text-l" for="salutation">Salutation:</label>
                        <select id="Salutation" 
                            disabled={!editMode}
                            bind:value={salutation}
                            class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500"
                            required
                        >
                            <option value="Mr.">Mr.</option>
                            <option value="Mrs.">Mrs.</option>
                            <option value="Mx.">Mx.</option>
                        </select>
                    </div>
                    <div class="my-2">
                        <label class="block text-gray-700 text-sm font-bold mb-1 text-l" for="firstName">First Name:</label>
                        <input
                                id="firstName"
                                type="text"
                                disabled={!editMode}
                                bind:value={firstName}
                                class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500"
                                required
                        />
                    </div>
                    <div class="my-2">
                        <label class="block text-gray-700 text-sm font-bold mb-1 text-l" for="lastName">Last Name:</label>
                        <input
                                id="lastName"
                                type="text"
                                disabled={!editMode}
                                bind:value={lastName}
                                class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500"
                                required
                        />
                    </div>
                    <div class="my-2">
                        <label class="block text-gray-700 text-sm font-bold mb-1 text-l" for="email">E-Mail:</label>
                        <input
                                id="email"
                                type="email"
                                disabled={!editMode}
                                bind:value={email}
                                class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500"
                                required
                        />
                    </div>
                    <div class="my-2">
                        <label class="block text-gray-700 text-sm font-bold mb-1 text-l" for="confirmEmail">Confirm E-Mail:</label>
                        <input
                                id="confirmEmail"
                                type="email"
                                disabled={!editMode}
                                bind:value={confirmEmail}
                                class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500"
                                required
                        />
                        {#if emailError}
                            <p class="text-red-500 text-sm">{emailError}</p>
                        {/if}
                    </div>
                    <div class="my-2">
                        <label class="block text-gray-700 text-sm font-bold mb-1 text-l" for="phoneNumber">Phone:</label>
                        <input
                                id="phoneNumber"
                                type="tel"
                                disabled={!editMode}
                                bind:value={phoneNumber}
                                class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500"
                                required
                        />
                    </div>
                    <div class="my-2">
                        <label class="block text-gray-700 text-sm font-bold mb-1 text-l" for="streetAndNumber">Street and Number:</label>
                        <input
                                id="streetAndNumber"
                                type="text"
                                disabled={!editMode}
                                bind:value={streetAndNumber}
                                class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500"
                                required
                        />
                    </div>
                    <div class="my-2">
                        <label class="block text-gray-700 text-sm font-bold mb-1 text-l" for="city">City:</label>
                        <input
                                id="city"
                                type="text"
                                disabled={!editMode}
                                bind:value={city}
                                class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500"
                                required
                        />
                    </div>
                    <div class="my-2">
                        <label class="block text-gray-700 text-sm font-bold mb-1 text-l" for="postalCode">Postal Code:</label>
                        <input
                                id="postalCode"
                                type="text"
                                disabled={!editMode}
                                bind:value={postalCode}
                                class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500"
                                required
                        />
                    </div>
                    <div class="my-2">
                        <label class="block text-gray-700 text-sm font-bold mb-1 text-l" for="country">Country:</label>
                        <input
                                id="country"
                                type="text"
                                disabled={!editMode}
                                bind:value={country}
                                class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500"
                                required
                        />
                    </div>
                    <label class="flex items-center space-x-2 pl-3 my-2 text-l">
                        <input type="checkbox" bind:checked={differentShippingAddress} class="form-checkbox" disabled={!editMode}>
                        <span class="font-bold">Different delivery address</span>
                    </label>
                    {#if differentShippingAddress}
                    <div transition:slide={{ duration: 300 }}>
                        <p class="text-xl font-bold mt-3 ml-3">New Delivery Address:</p>
                        <div class="ml-5 mt-2">
                            <div class="my-2">
                                <label class="block text-gray-700 text-sm font-bold mb-1 text-l" for="alternativeStreetAndNumber">Street and Number:</label>
                                <input
                                        id="alternativeStreetAndNumber"
                                        type="text"
                                        disabled={!editMode}
                                        bind:value={alternativeStreetAndNumber}
                                        class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500"
                                        required={differentShippingAddress}
                                />
                            </div>
                            <div class="my-2">
                                <label class="block text-gray-700 text-sm font-bold mb-1 text-l" for="alternativeCity">City:</label>
                                <input
                                        id="alternativeCity"
                                        type="text"
                                        disabled={!editMode}
                                        bind:value={alternativeCity}
                                        class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500"
                                        required={differentShippingAddress}
                                />
                            </div>
                            <div class="my-2">
                                <label class="block text-gray-700 text-sm font-bold mb-1 text-l" for="alternativePostalCode">Postal Code:</label>
                                <input
                                        id="alternativePostalCode"
                                        type="text"
                                        disabled={!editMode}
                                        bind:value={alternativePostalCode}
                                        class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500"
                                        required={differentShippingAddress}
                                />
                            </div>
                            <div class="my-2">
                                <label class="block text-gray-700 text-sm font-bold mb-1 text-l" for="alternativeCountry">Country:</label>
                                <input
                                        id="alternativeCountry"
                                        type="text"
                                        disabled={!editMode}
                                        bind:value={alternativeCountry}
                                        class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500"
                                        required={differentShippingAddress}
                                />
                            </div>
                        </div>
                    </div>
                    {/if}
                </form>
            </div>
            </div>
        </div>

        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <div class={`flex justify-center mt-5 ${(selectLoginOrPrefill) ? 'opacity-50 pointer-events-none' : ''}`}>
            <div class="flex-col">
                <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
                <img 
                    src={UpAndDownArrow} 
                    alt="Arrow" 
                    on:click={handleNext}
                    class="w-16 h-16 bg-black p-3 rounded-full object-cover hover:bg-gray-500 transition-transform duration-500"
                    style="transform: rotate({rotation}deg);"
                />
                {#if editMode}
                    <p class="text-center pt-2 opacity-80 font-bold">Next step</p>
                {:else}
                    <p class="text-center pt-2 opacity-80 font-bold">Step Back</p>
                {/if}
            </div>
        </div>

        <div class={`m-5 pb-2 md:m-10 ${(editMode) ? 'opacity-50 pointer-events-none' : ''}`} bind:this={legalRequirements}>
            <p class="text-2xl font-bold pb-2">Legal requirements:</p>
            <div class="bg-gray-200 rounded-xl shadow-lg flex flex-col space-y-4 md:space-y-0 relative p-5">
                <div class="flex flex-col space-y-2">
                    <p class="p-3 pb-0 font-bold">Shipping information:</p>
                    <p class="pl-3">We ship your order with DHL. The delivery time is usually 2-4 working days within Germany. You will receive a tracking number as soon as your order has been dispatched. Further information can be found in our shipping conditions.</p>
                    <p class="p-3 pb-0 font-bold">Consent to the General Terms and Conditions and Privacy Policy:</p>
                    <p class="pl-3">
                        By completing your order, you agree to our 
                        <a href="/legalInformation#terms" class="text-blue-600 hover:underline">General Terms and Conditions (GTC)</a>, 
                        the <a href="/legalInformation#privacy" class="text-blue-600 hover:underline">Privacy Policy</a>, and the 
                        <a href="/legalInformation#cancellation" class="text-blue-600 hover:underline">Cancellation Policy</a>. 
                        You confirm that you have read and understood the conditions and agree to them. Your data will be processed exclusively in the context of order processing.
                    </p>
                    <label class="flex items-center space-x-2 pl-3">
                        <input type="checkbox" bind:checked={termsAccepted} on:change={handleTermsAndConditionsCheckboxChange} class="form-checkbox">
                        <span>I agree to the Terms and Conditions and Privacy Policy <span class="text-red-700">*</span></span>
                    </label>
                </div>
            </div>
            <div class="flex justify-center items-center mt-5">
                <div class="flex flex-col">
                    <div class="flex flex-col items-center my-8">
                        <p class="text-gray-500 text-l">Order price</p>
                        <p class="text-2xl font-bold">{totalPrice} €</p>
                    </div>
                    <div>
                        {#if readyforPayment}
                            <button on:click={handleSubmit} class="bg-black hover:bg-gray-500 text-white px-8 py-3 rounded-3xl text-xl font-bold">
                                Continue to payment ⇨
                            </button>
                        {:else}
                            <button class="bg-black text-white px-8 py-3 rounded-3xl opacity-50 cursor-not-allowed text-xl font-bold">
                                Continue to payment ⇨
                            </button>
                        {/if}
                    </div>
                </div>
            </div>
            <div id="spacer" class="h-5"></div>
        </div>
</div>

<Footer />