<script>
    import { Billboard, HTML } from "@threlte/extras";
    import { selectedProductID, selectedProductPosition } from "../../../stores/product_selection";
    import Notification from "$lib/components/messages/Notification.svelte";
    import {addMessage} from "../../../stores/global_stores.js";
    import { updateCartItemCount } from '../../../stores/product_selection';
    import { triggerDeselect } from "../../../stores/product_selection";
    import TryonOverlay from './tryonOverlay.svelte';
    
    let cart = [];
    let totalPrice = 0;
    let errorMessageStock = "";

    let isVisible = false;

    export let productData;
    let selectedProductinOL = [];

    let selectedSize = "";
    let selectedColor = "";
    let quantity = 1;

    if (typeof window !== 'undefined') {
        cart = JSON.parse(localStorage.getItem("cart")) || [];
    }

    const calculateTotalPrice = () => {
        totalPrice = cart.reduce((total, item) => total + item.quantity * parseFloat(item.price), 0).toFixed(2);
    };

    $: if (selectedSize && selectedProductinOL) {
        const availableStock = selectedProductinOL.stock[selectedSize];
        if (quantity > availableStock) {
            quantity = availableStock;
        }
        errorMessageStock = ""; 
    }

    $: if (selectedColor) {
        errorMessageStock = "";
    }


    const addToCart = () => {
        const product = selectedProductinOL;

        if (!selectedSize || !selectedColor) {
            errorMessageStock = "Please select size and color.";
            return;
        }

        const existingProduct = cart.find(item => item.id === product.id && item.size === selectedSize && item.color === selectedColor);

        if (existingProduct) {
            const availableStock = product.stock[selectedSize];

            if (existingProduct.quantity + quantity <= availableStock) {
                existingProduct.quantity += quantity;
            } else {
                errorMessageStock = `There are just ${availableStock - existingProduct.quantity} piece in size ${selectedSize} available.`;
                return;
            }
        } else {
            if (product.stock[selectedSize] >= quantity) {
                cart.push({ 
                    ...product, 
                    size: selectedSize, 
                    color: selectedColor, 
                    quantity 
                });
            } else {
                errorMessageStock = `There is none ${selectedSize} in stock currently.`;
                return;
            }
        }

        updateCart();
        addMessage({ type: 'success', text: 'Product successfully added to cart.' });
        updateCartItemCount();

        triggerDeselect.set(true); 

        selectedSize = "";
        selectedColor = "";
        quantity = 1;

    };

    const increaseQuantity = () => {
        if (selectedSize === "" || selectedColor === "") {
            errorMessageStock = "Please select size and color.";
            return;
        }

        if (quantity < selectedProductinOL.stock[selectedSize]) {
            quantity++;
        } else {
            errorMessageStock = `Just ${selectedProductinOL.stock[selectedSize]} Piece/s available.`;
        }
    };

    const decreaseQuantity = () => {
        if (quantity > 1) {
            quantity--;
        }
    };

    const updateCart = () => {
        if (typeof window !== 'undefined') {
            localStorage.setItem("cart", JSON.stringify(cart));
        }
        cart = [...cart];
        calculateTotalPrice();
    };

    $: if (productData) {
        selectedProductinOL = productData.find(product => product.id === $selectedProductID);     
    }
</script>

<Notification />
<Billboard>
    {#if $selectedProductID !== -1}
    <HTML
        position.x={$selectedProductPosition[0] - 0.5}
        position.y={$selectedProductPosition[1] - 2}
        position.z={$selectedProductPosition[2]}
        center
    >
        <div class='w-80 h-36'></div>
        <div class='w-80 bg-white flex flex-col p-4 pt-0 rounded-2xl'>
            <div class='py-3'>
                <p class='text-4xl font-semibold'>{selectedProductinOL.name}</p>
                <p class='text-2xl'>{selectedProductinOL.price}€ <span class='text-xs text-gray-400'>tax included</span></p>
            </div>
            <button
            class="item-center ml-2 border-2 border-black bg-black text-white rounded-full h-12 text-xl px-6 my-4 hover:bg-gray-600"
            on:click={() => (isVisible = true)}
        >
            Try-On
        </button>
            <div class='bg-gray-200 shadow-lg rounded-xl pl-3'>
                <h3 class='text-xl font-semibold'>Select size</h3>
                <div>
                    {#each Object.keys(selectedProductinOL.stock) as size}
                        <button
                            class='border-2 border-black rounded-full h-10 w-10 pl-2 pr-2 mr-1 hover:bg-gray-400'
                            class:bg-black={selectedSize === size}
                            class:text-white={selectedSize === size}
                            on:click={() => (selectedSize = size)}
                        >
                            {size}
                        </button>
                    {/each}
                </div>
                <h3 class='text-xl font-semibold'>Select color</h3>
                <div class="">
                    {#each selectedProductinOL.colors as color}
                        <button
                            class='border-2 border-black rounded-full h-10 pl-2 pr-2 mr-1 hover:bg-gray-400'
                            class:bg-black={selectedColor === color}
                            class:text-white={selectedColor === color}
                            on:click={() => (selectedColor = color)}
                        >
                            {color}
                        </button>
                    {/each}
                </div>
                <div class='inline-flex w-full py-3 pr-3'>
                    <div class="flex items-center gap-2 border-2 border-black rounded-full mr-3 px-2">
                        <button
                            class="text-xl font-semibold hover:bg-gray-400 rounded-full h-8 w-8 flex items-center justify-center"
                            on:click={decreaseQuantity}
                        >
                            -
                        </button>
                        <span class="text-lg">{quantity}</span>
                        <button
                            class="text-xl font-semibold hover:bg-gray-400 rounded-full h-8 w-8 flex items-center justify-center"
                            on:click={increaseQuantity}
                        >
                            +
                        </button>
                    </div>
                    <button
                        class='grow border-2 border-black bg-black text-white rounded-full h-14 text-xl hover:bg-gray-600'
                        on:click={addToCart}
                    >
                        Add to cart
                    </button>
                </div>
                {#if errorMessageStock}
                    <p class='text-red-500 mt-2'>{errorMessageStock}</p>
                {/if}
            </div>
        </div>
    </HTML>
    {/if}
</Billboard>


{#if isVisible}
<TryonOverlay
position={[
    $selectedProductPosition[0] - 0.5,
    $selectedProductPosition[1] + 0.1,      
    $selectedProductPosition[2]      
  ]}
productId={$selectedProductID}
on:close={() => (isVisible = false)}
/>
{/if}
