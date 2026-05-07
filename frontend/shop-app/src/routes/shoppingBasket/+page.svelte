<script>
    import "../../input.css";
    import { onMount } from "svelte";
    import { getProducts } from "../../api/products/products.js";
    import {addMessage} from "../../stores/global_stores.js";
    import Notification from "$lib/components/messages/Notification.svelte";
    import Header from "$lib/components/Header.svelte";
    import Footer from "$lib/components/Footer.svelte";

    let products = [];
    let cart = [];
    let totalPrice = 0;
    let errorMessageStock = "";

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

    onMount(async () => {
        try {
            let tmp = await getProducts();
            if (tmp) {
                products = tmp;
            }
            addMessage({ type: 'success', text: 'Shopping basket succesfully loaded'});
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
    <title>Shopping basket</title>
</head>

<Notification />
<Header title="Shopping basket"/>
<div id="content" class="overflow-hidden min-h-screen mt-3 md:mt-0">
    <div class="m-5 pb-2 md:m-10">
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
                {#if cart.length === 0}
                    <!-- svelte-ignore a11y-missing-attribute -->
                    <a class="opacity-50 cursor-not-allowed bg-black hover:bg-gray-500 text-white font-bold py-2 px-4 rounded-3xl text-xl">
                        Checkout
                    </a>
                {:else}
                    <a href="/checkout" class="bg-black hover:bg-gray-500 text-white font-bold py-2 px-4 rounded-3xl text-xl">
                        Checkout
                    </a>
                {/if}
            </div>
        </div>
    </div>
</div>

<Footer/>