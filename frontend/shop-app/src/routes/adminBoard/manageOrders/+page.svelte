<script>
    import "../../../input.css";
    import { getAllOrders } from "../../../api/orders/orders";
    import { onMount } from "svelte";
    import { setCsrfToken } from "$lib";
    import { addMessage } from "../../../stores/global_stores";
    import Notification from "$lib/components/messages/Notification.svelte";
    import { formatDateTime } from "$lib/globalFunctions/timeFormatting";
    import arrow from '$lib/images/arrow.png';
    import { slide } from 'svelte/transition';
    import { updateOrder, deleteOrder } from "../../../api/orders/orders";
	import DeleteOrderPopup from "../../../lib/components/popUps/deleteOrder.svelte";
    import Header from "$lib/components/Header.svelte";

    let activeOrders = [];
    let cancelledOrders = [];
    let deliveredOrders = [];
    let isLoading = true;
    let isError = false;

    let showPopup = false;
    let currentOrderId = null;

    let expandedOrders = {};

    let editingOrderId = null;

    let id = '';
    let status = '';
    let alternative_address = [];
    let city = '';
    let country = '';
    let differentShippingAddress = false;
    let email = '';
    let salutation = '';
    let first_name = '';
    let last_name = '';
    let phone_number = '';
    let postal_code = '';
    let payedStatus = false;
    let paymentMethod = '';
    let selectedProducts = [];
    let street_and_number = '';
    let termsAccepted = false;
    let totalPrice = '';
    let orderPlacedByUserWithId = '';
    let stripe_session_id = '';


    function toggleOrderDetails(orderId) {
        if (!editingOrderId || editingOrderId === orderId) {
            expandedOrders[orderId] = !expandedOrders[orderId];
        }
    }

    function startEditingOrder(order) {
        if (editingOrderId === order.id) {
            editingOrderId = null;
            return;
        } else {
            editingOrderId = order.id;

            expandedOrders[order.id] = true;

            id = order.id;
            status = order.status;
            alternative_address = order.alternative_address || {};
            city = order.city;
            country = order.country;
            differentShippingAddress = order.differentShippingAddress;
            email = order.email;
            first_name = order.first_name;
            last_name = order.last_name;
            phone_number = order.phone_number;
            postal_code = order.postal_code;
            payedStatus = order.payedStatus;
            selectedProducts = order.selectedProducts;
            salutation = order.salutation;
            selectedProducts = order.selectedProducts;
            street_and_number = order.street_and_number;
            termsAccepted = order.termsAccepted;
            totalPrice = order.totalPrice;
            orderPlacedByUserWithId = order.orderPlacedByUserWithId;
            stripe_session_id = order.stripe_session_id;
        }
    }

    async function updateAOrder() {
        try {
            const response = await updateOrder(id, alternative_address, city, country, differentShippingAddress, email, first_name, last_name, phone_number, postal_code, payedStatus, paymentMethod, salutation, selectedProducts, street_and_number, termsAccepted, totalPrice, orderPlacedByUserWithId, stripe_session_id, status);
            addMessage({ type: 'success', text: 'Order ' + editingOrderId + ' updated successfully' });
            editingOrderId = null;

            // Reload orders
            setCsrfToken();
            try {
                let ordersResponse = await getAllOrders();
                activeOrders = ordersResponse.filter(order => order.status !== 'cancelled' && order.status !== 'delivered');
                cancelledOrders = ordersResponse.filter(order => order.status === 'cancelled');
                deliveredOrders = ordersResponse.filter(order => order.status === 'delivered');


                addMessage({ type: 'success', text: 'Orders refreshed successfully' });
            } catch (error) {
                addMessage({ type: 'error', text: 'Failed to refresh orders: ' + (error.message || 'Unknown error') });
            }

        } catch (error) {
            addMessage({ type: 'error', text: 'Failed to update order: ' + (error.message || 'Unknown error') });
        }
        let ordersResponse = await getAllOrders();
        activeOrders = ordersResponse.filter(order => order.status !== 'cancelled' && order.status !== 'delivered');
        cancelledOrders = ordersResponse.filter(order => order.status === 'cancelled');
        deliveredOrders = ordersResponse.filter(order => order.status === 'delivered');
    }

    async function handleDeleteOrder(id) {
        try {
            await deleteOrder(id);
            addMessage({ type: 'success', text: 'Order ' + id + ' deleted successfully' });

            // Reload orders
            setCsrfToken();
                try {
                    let ordersResponse = await getAllOrders();
                    activeOrders = ordersResponse.filter(order => order.status !== 'cancelled' && order.status !== 'delivered');
                    cancelledOrders = ordersResponse.filter(order => order.status === 'cancelled');
                    deliveredOrders = ordersResponse.filter(order => order.status === 'delivered');


                    addMessage({ type: 'success', text: 'Orders refreshed successfully' });
                } catch (error) {
                    addMessage({ type: 'error', text: 'Failed to refresh orders: ' + (error.message || 'Unknown error') });
                }
        } catch (err) {
            addMessage({ type: 'error', text: 'Failed to delete order: ' + (err.message || 'Unknown error') });
        }
    }

    function togglePopup(id) {
        currentOrderId = id;
        showPopup = !showPopup;
    }

    function closePopup() {
        showPopup = false;
    }


    async function deleteOrderThroughPopUp() {
        if (currentOrderId) {
            handleDeleteOrder(currentOrderId);
        }
        showPopup = false;
    }

    onMount(async () => {
        setCsrfToken();
        try {
            let ordersResponse = await getAllOrders();
            activeOrders = ordersResponse.filter(order => order.status !== 'cancelled' && order.status !== 'delivered');
            cancelledOrders = ordersResponse.filter(order => order.status === 'cancelled');
            deliveredOrders = ordersResponse.filter(order => order.status === 'delivered');

            isLoading = false;
            addMessage({ type: 'success', text: 'Orders loaded successfully' });
        } catch (error) {
            isLoading = false;
            isError = true;
            addMessage({ type: 'error', text: 'Failed to load orders: ' + (error.message || 'Unknown error') });
        }
    });

    function createImageUrl(base64String) {
        return `data:image/png;base64,${base64String}`;
    }

</script>

<head>
    <title>Admin Board - Manage orders</title>
</head>

<Notification />
<Header title="Manage orders"/>
<div id="content" class="">
    <div class="m-5 pb-2 md:m-10">
        <h1 class="text-2xl font-bold pb-2">Active Orders:</h1>
        {#if isLoading}
            <div class="flex space-x-2 justify-center items-center">
                <div class='h-5 w-5 bg-black rounded-full animate-bounce [animation-delay:-0.3s]'></div>
                <div class='h-5 w-5 bg-black rounded-full animate-bounce [animation-delay:-0.15s]'></div>
                <div class='h-5 w-5 bg-black rounded-full animate-bounce'></div>
            </div>
        {:else if isError}
            <p class="text-center mt-5 font-bold text-l text-red-600">Oops, something went wrong..</p>
        {:else if activeOrders.length === 0}
            <p class="text-center mt-5 font-bold text-l">No active orders yet</p>
        {:else}
            {#each activeOrders as order}
                <!-- svelte-ignore missing-declaration -->
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <!-- svelte-ignore a11y-no-static-element-interactions -->
                <div class="bg-gray-200 rounded-xl shadow-lg flex flex-col space-y-4 md:space-y-0 p-4 relative mb-6">
                    <div class="flex justify-between items-center cursor-pointer hover:opacity-60" on:click={() => toggleOrderDetails(order.id)}>
                        <p class="font-bold text-xl">Order with ID {order.id} from {formatDateTime(order.created_at)}</p>
                        <img 
                            src={arrow} 
                            alt="arrow" 
                            class="transition-transform duration-300 w-12 h-7" 
                            style="transform: rotate({expandedOrders[order.id] ? '180deg' : '0deg'});" 
                        />
                    </div>

                    {#if expandedOrders[order.id]}
                        <div class="mt-2" transition:slide>
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
                                            <p class="m-2 ml-4 text-l">{order.alternative_address.street_and_number}</p>
                                            <p class="m-2 ml-4 text-l">{order.alternative_address.postal_code}, {order.alternative_address.city}</p>
                                            <p class="m-2 ml-4 text-l pb-2">{order.alternative_address.country}</p>
                                        {:else}
                                            <p class="m-2 ml-4 text-l">{order.street_and_number}</p>
                                            <p class="m-2 ml-4 text-l">{order.postal_code}, {order.city}</p>
                                            <p class="m-2 ml-4 text-l pb-2">{order.country}</p>
                                        {/if}
                                    </div>
                                </div>
                                <div class="flex-1 rounded-lg p-2">
                                    <p class="font-semibold">Payment information:</p>
                                    <div>
                                        {#if order.payedStatus}
                                            <p class="m-2 ml-4 text-l">Payment Status: Payed</p>
                                        {:else}    
                                            <p class="m-2 ml-4 text-l">Payment Status: Not Payed</p>
                                        {/if} 
                                        <p class="m-2 ml-4 text-l">Payment Method: {order.paymentMethod}</p>
                                        <p class="m-2 ml-4 text-l">Payed at: {formatDateTime(order.payed_at)}</p>
                                    </div>
                                </div>
                            </div>
                            <div>
                                <p class="font-bold text-xl">Total Price: {order.totalPrice}</p>              
                            </div>
                            <div>
                                <p class="pt-3 font-bold ">Purchased products:</p>
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
                                {#if order.status === "new"}
                                    <p class="font-bold text-xl pt-5">Current Order Status: New order</p>
                                {:else if order.status === "cancelled"}
                                    <p class="font-bold text-xl pt-5">Current Order Status: Cancelled</p>
                                {:else if order.status === "delivered"}
                                    <p class="font-bold text-xl pt-5">Current Order Status: Delivered</p>
                                {:else if order.status === "in_progress"}
                                    <p class="font-bold text-xl pt-5">Current Order Status: In progress</p>
                                {:else if order.status === "in_shipment"}
                                    <p class="font-bold text-xl pt-5">Current Order Status: In Shipment</p>
                                {/if}
                            </div>
                            <div>
                                <p class="font-bold text-l pt-3">Metadata:</p>
                                <p class="m-2 ml-4 text-l">Order Placed by User with ID: {order.orderPlacedByUserWithId}</p>
                                <p class="m-2 ml-4 text-l">Terms of Service accepted: {order.termsAccepted}</p>
                                <p class="m-2 ml-4 text-l">Created at: {formatDateTime(order.created_at)}</p>
                                <p class="m-2 ml-4 text-l">Last Updated: {formatDateTime(order.updated_at)}</p>
                                <p class="m-2 ml-4 text-m">Stripe Session ID: {order.stripe_session_id}</p>
                            </div>
                        </div>
                        <div class="flex justify-end mt-auto">
                            <button class="bg-black hover:bg-gray-500 text-white font-bold py-2 px-4 rounded-3xl" on:click={() => startEditingOrder(order)}>
                                {editingOrderId === order.id ? 'Cancel' : 'Edit Order'}
                            </button>
                            <button class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-3xl ml-4" on:click={() => togglePopup(order.id)}>
                                Delete Order
                            </button>
                        </div>
                    {/if}
                </div>
                {#if editingOrderId === order.id}
                    <div class="bg-gray-100 rounded-lg shadow-lg p-4 mt-4 mb-8" transition:slide>
                        <h2 class="text-xl font-bold mb-4">Edit Order with ID {id}</h2>
                        <div class="space-y-4">
                            <p>Order Status:</p>
                            <select class="w-full p-2 border" bind:value={status}>
                                <option value="new">New order</option>
                                <option value="cancelled">Cancelled</option>
                                <option value="delivered">Delivered</option>
                                <option value="in_progress">In progress</option>
                                <option value="in_shipment">In Shipment</option>
                            </select>
                            
                            <p>Payment Status:</p>
                            <select class="w-full p-2 border" bind:value={payedStatus}>
                                <option value={true}>Payed</option>
                                <option value={false}>Not Payed</option>
                            </select>

                            <p>Total Price:</p>
                            <input class="w-full p-2 border" type="text" bind:value={totalPrice} placeholder="Total Price" />

                            <p>Payment Method:</p>
                            <select class="w-full p-2 border" bind:value={paymentMethod}>
                                <option value="Credit Card">Credit Card</option>
                                <option value="PayPal">Paypal</option>
                                <option value="Bank Transfer">Bank Transfer</option>
                            </select>

                            <p>Salutation:</p>
                            <select class="w-full p-2 border" bind:value={salutation}>
                                <option value="Mr.">Mr.</option>
                                <option value="Mrs.">Mrs.</option>
                                <option value="Mx.">Mx.</option>
                            </select>

                            <p>First Name:</p>
                            <input class="w-full p-2 border" type="text" bind:value={first_name} placeholder="First Name" />
                            
                            <p>Last Name:</p>
                            <input class="w-full p-2 border" type="text" bind:value={last_name} placeholder="Last Name" />

                            <p>Email:</p>
                            <input class="w-full p-2 border" type="text" bind:value={email} placeholder="Email" />
                            
                            <p>Phone Number:</p>
                            <input class="w-full p-2 border" type="text" bind:value={phone_number} placeholder="Phone Number" />

                            <p>Street and Number:</p>
                            <input class="w-full p-2 border" type="text" bind:value={street_and_number} placeholder="Street and Number" />

                            <p>Postal Code:</p>
                            <input class="w-full p-2 border" type="text" bind:value={postal_code} placeholder="Postal Code" />

                            <p>City:</p>
                            <input class="w-full p-2 border" type="text" bind:value={city} placeholder="City" />

                            <p>Country:</p>
                            <input class="w-full p-2 border" type="text" bind:value={country} placeholder="Country" />

                            <p>Different Shipping Address:</p>
                            <select class="w-full p-2 border" bind:value={differentShippingAddress}>
                                <option value={true}>Yes</option>
                                <option value={false}>No</option>
                            </select>

                            {#if differentShippingAddress}
                                <p>Alternative Address:</p>
                                <input class="w-full p-2 border" type="text" bind:value={alternative_address.street_and_number} placeholder="Street and Number"/>
                                <input class="w-full p-2 border" type="text" bind:value={alternative_address.postal_code} placeholder="Postal Code"/>
                                <input class="w-full p-2 border" type="text" bind:value={alternative_address.city} placeholder="City"/>
                                <input class="w-full p-2 border" type="text" bind:value={alternative_address.country} placeholder="Country"/>
                            {/if}

                            <p>Terms Accepted:</p>
                            <select class="w-full p-2 border" bind:value={termsAccepted}>
                                <option value={true}>Yes</option>
                                <option value={false}>No</option>
                            </select>
                        </div>
                        <button class="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded-3xl mt-4" on:click={updateAOrder}>
                            Update Order
                        </button>
                    </div>
                {/if}
            {/each}
        {/if}
    </div>

    <div class="m-5 pb-2 md:m-10">
        <h1 class="text-2xl font-bold pb-2">Delivered Orders:</h1>
        {#if isLoading}
            <div class="flex space-x-2 justify-center items-center">
                <div class='h-5 w-5 bg-black rounded-full animate-bounce [animation-delay:-0.3s]'></div>
                <div class='h-5 w-5 bg-black rounded-full animate-bounce [animation-delay:-0.15s]'></div>
                <div class='h-5 w-5 bg-black rounded-full animate-bounce'></div>
            </div>
        {:else if isError}
            <p class="text-center mt-5 font-bold text-l text-red-600">Oops, something went wrong..</p>
        {:else if deliveredOrders.length === 0}
            <p class="text-center mt-5 font-bold text-l">No delivered orders yet</p>
        {:else}
            {#each deliveredOrders as order}
            <!-- svelte-ignore missing-declaration -->
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <!-- svelte-ignore a11y-no-static-element-interactions -->
            <div class="bg-gray-200 rounded-xl shadow-lg flex flex-col space-y-4 md:space-y-0 p-4 relative mb-6">
                <div class="flex justify-between items-center cursor-pointer hover:opacity-60" on:click={() => toggleOrderDetails(order.id)}>
                    <p class="font-bold text-xl">Order with ID {order.id} from {formatDateTime(order.created_at)}</p>
                    <img 
                        src={arrow} 
                        alt="arrow" 
                        class="transition-transform duration-300 w-12 h-7" 
                        style="transform: rotate({expandedOrders[order.id] ? '180deg' : '0deg'});" 
                    />
                </div>

                {#if expandedOrders[order.id]}
                    <div class="mt-2" transition:slide>
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
                                        <p class="m-2 ml-4 text-l">{order.alternative_address.street_and_number}</p>
                                        <p class="m-2 ml-4 text-l">{order.alternative_address.postal_code}, {order.alternative_address.city}</p>
                                        <p class="m-2 ml-4 text-l pb-2">{order.alternative_address.country}</p>
                                    {:else}
                                        <p class="m-2 ml-4 text-l">{order.street_and_number}</p>
                                        <p class="m-2 ml-4 text-l">{order.postal_code}, {order.city}</p>
                                        <p class="m-2 ml-4 text-l pb-2">{order.country}</p>
                                    {/if}
                                </div>
                            </div>
                            <div class="flex-1 rounded-lg p-2">
                                <p class="font-semibold">Payment information:</p>
                                <div>
                                    {#if order.payedStatus}
                                        <p class="m-2 ml-4 text-l">Payment Status: Payed</p>
                                    {:else}    
                                        <p class="m-2 ml-4 text-l">Payment Status: Not Payed</p>
                                    {/if} 
                                    <p class="m-2 ml-4 text-l">Payment Method: {order.paymentMethod}</p>
                                    <p class="m-2 ml-4 text-l">Payed at: {formatDateTime(order.payed_at)}</p>
                                </div>
                            </div>
                        </div>
                        <div>
                            <p class="font-bold text-xl">Total Price: {order.totalPrice}</p>              
                        </div>
                        <div>
                            <p class="pt-3 font-bold ">Purchased products:</p>
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
                            {#if order.status === "new"}
                                <p class="font-bold text-xl pt-5">Current Order Status: New order</p>
                            {:else if order.status === "cancelled"}
                                <p class="font-bold text-xl pt-5">Current Order Status: Cancelled</p>
                            {:else if order.status === "delivered"}
                                <p class="font-bold text-xl pt-5">Current Order Status: Delivered</p>
                            {:else if order.status === "in_progress"}
                                <p class="font-bold text-xl pt-5">Current Order Status: In progress</p>
                            {:else if order.status === "in_shipment"}
                                <p class="font-bold text-xl pt-5">Current Order Status: In Shipment</p>
                            {/if}
                        </div>
                        <div>
                            <p class="font-bold text-l pt-3">Metadata:</p>
                            <p class="m-2 ml-4 text-l">Order Placed by User with ID: {order.orderPlacedByUserWithId}</p>
                            <p class="m-2 ml-4 text-l">Terms of Service accepted: {order.termsAccepted}</p>
                            <p class="m-2 ml-4 text-l">Created at: {formatDateTime(order.created_at)}</p>
                            <p class="m-2 ml-4 text-l">Last Updated: {formatDateTime(order.updated_at)}</p>
                            <p class="m-2 ml-4 text-m">Stripe Session ID: {order.stripe_session_id}</p>
                        </div>
                    </div>
                    <div class="flex justify-end mt-auto">
                        <button class="bg-black hover:bg-gray-500 text-white font-bold py-2 px-4 rounded-3xl" on:click={() => startEditingOrder(order)}>
                            {editingOrderId === order.id ? 'Cancel' : 'Edit Order'}
                        </button>
                        <button class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-3xl ml-4" on:click={() => togglePopup(order.id)}>
                            Delete Order
                        </button>
                    </div>
                {/if}
            </div>
            {#if editingOrderId === order.id}
                <div class="bg-gray-100 rounded-lg shadow-lg p-4 mt-4 mb-8" transition:slide>
                    <h2 class="text-xl font-bold mb-4">Edit Order with ID {id}</h2>
                    <div class="space-y-4">
                        <p>Order Status:</p>
                        <select class="w-full p-2 border" bind:value={status}>
                            <option value="new">New order</option>
                            <option value="cancelled">Cancelled</option>
                            <option value="delivered">Delivered</option>
                            <option value="in_progress">In progress</option>
                            <option value="in_shipment">In Shipment</option>
                        </select>
                        
                        <p>Payment Status:</p>
                        <select class="w-full p-2 border" bind:value={payedStatus}>
                            <option value={true}>Payed</option>
                            <option value={false}>Not Payed</option>
                        </select>

                        <p>Total Price:</p>
                        <input class="w-full p-2 border" type="text" bind:value={totalPrice} placeholder="Total Price" />

                        <p>Payment Method:</p>
                        <select class="w-full p-2 border" bind:value={paymentMethod}>
                            <option value="Credit Card">Credit Card</option>
                            <option value="PayPal">Paypal</option>
                            <option value="Bank Transfer">Bank Transfer</option>
                        </select>

                        <p>Salutation:</p>
                        <select class="w-full p-2 border" bind:value={salutation}>
                            <option value="Mr.">Mr.</option>
                            <option value="Mrs.">Mrs.</option>
                            <option value="Mx.">Mx.</option>
                        </select>

                        <p>First Name:</p>
                        <input class="w-full p-2 border" type="text" bind:value={first_name} placeholder="First Name" />
                        
                        <p>Last Name:</p>
                        <input class="w-full p-2 border" type="text" bind:value={last_name} placeholder="Last Name" />

                        <p>Email:</p>
                        <input class="w-full p-2 border" type="text" bind:value={email} placeholder="Email" />
                        
                        <p>Phone Number:</p>
                        <input class="w-full p-2 border" type="text" bind:value={phone_number} placeholder="Phone Number" />

                        <p>Street and Number:</p>
                        <input class="w-full p-2 border" type="text" bind:value={street_and_number} placeholder="Street and Number" />

                        <p>Postal Code:</p>
                        <input class="w-full p-2 border" type="text" bind:value={postal_code} placeholder="Postal Code" />

                        <p>City:</p>
                        <input class="w-full p-2 border" type="text" bind:value={city} placeholder="City" />

                        <p>Country:</p>
                        <input class="w-full p-2 border" type="text" bind:value={country} placeholder="Country" />

                        <p>Different Shipping Address:</p>
                        <select class="w-full p-2 border" bind:value={differentShippingAddress}>
                            <option value={true}>Yes</option>
                            <option value={false}>No</option>
                        </select>

                        {#if differentShippingAddress}
                            <p>Alternative Address:</p>
                            <input class="w-full p-2 border" type="text" bind:value={alternative_address.street_and_number} placeholder="Street and Number"/>
                            <input class="w-full p-2 border" type="text" bind:value={alternative_address.postal_code} placeholder="Postal Code"/>
                            <input class="w-full p-2 border" type="text" bind:value={alternative_address.city} placeholder="City"/>
                            <input class="w-full p-2 border" type="text" bind:value={alternative_address.country} placeholder="Country"/>
                        {/if}

                        <p>Terms Accepted:</p>
                        <select class="w-full p-2 border" bind:value={termsAccepted}>
                            <option value={true}>Yes</option>
                            <option value={false}>No</option>
                        </select>
                    </div>
                    <button class="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded-3xl mt-4" on:click={updateAOrder}>
                        Update Order
                    </button>
                </div>
            {/if}
        {/each}
        {/if}
    </div>

    <div class="m-5 pb-2 md:m-10">
        <h1 class="text-2xl font-bold pb-2">Cancelled Orders:</h1>
        {#if isLoading}
            <div class="flex space-x-2 justify-center items-center">
                <div class='h-5 w-5 bg-black rounded-full animate-bounce [animation-delay:-0.3s]'></div>
                <div class='h-5 w-5 bg-black rounded-full animate-bounce [animation-delay:-0.15s]'></div>
                <div class='h-5 w-5 bg-black rounded-full animate-bounce'></div>
            </div>
        {:else if isError}
            <p class="text-center mt-5 font-bold text-l text-red-600">Oops, something went wrong..</p>
        {:else if cancelledOrders.length === 0}
            <p class="text-center mt-5 font-bold text-l">No cancelled orders yet</p>
        {:else}
            {#each cancelledOrders as order}
            <!-- svelte-ignore missing-declaration -->
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <!-- svelte-ignore a11y-no-static-element-interactions -->
            <div class="bg-gray-200 rounded-xl shadow-lg flex flex-col space-y-4 md:space-y-0 p-4 relative mb-6">
                <div class="flex justify-between items-center cursor-pointer hover:opacity-60" on:click={() => toggleOrderDetails(order.id)}>
                    <p class="font-bold text-xl">Order with ID {order.id} from {formatDateTime(order.created_at)}</p>
                    <img 
                        src={arrow} 
                        alt="arrow" 
                        class="transition-transform duration-300 w-12 h-7" 
                        style="transform: rotate({expandedOrders[order.id] ? '180deg' : '0deg'});" 
                    />
                </div>

                {#if expandedOrders[order.id]}
                    <div class="mt-2" transition:slide>
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
                                        <p class="m-2 ml-4 text-l">{order.alternative_address.street_and_number}</p>
                                        <p class="m-2 ml-4 text-l">{order.alternative_address.postal_code}, {order.alternative_address.city}</p>
                                        <p class="m-2 ml-4 text-l pb-2">{order.alternative_address.country}</p>
                                    {:else}
                                        <p class="m-2 ml-4 text-l">{order.street_and_number}</p>
                                        <p class="m-2 ml-4 text-l">{order.postal_code}, {order.city}</p>
                                        <p class="m-2 ml-4 text-l pb-2">{order.country}</p>
                                    {/if}
                                </div>
                            </div>
                            <div class="flex-1 rounded-lg p-2">
                                <p class="font-semibold">Payment information:</p>
                                <div>
                                    {#if order.payedStatus}
                                        <p class="m-2 ml-4 text-l">Payment Status: Payed</p>
                                    {:else}    
                                        <p class="m-2 ml-4 text-l">Payment Status: Not Payed</p>
                                    {/if} 
                                    <p class="m-2 ml-4 text-l">Payment Method: {order.paymentMethod}</p>
                                    <p class="m-2 ml-4 text-l">Payed at: {formatDateTime(order.payed_at)}</p>
                                </div>
                            </div>
                        </div>
                        <div>
                            <p class="font-bold text-xl">Total Price: {order.totalPrice}</p>              
                        </div>
                        <div>
                            <p class="pt-3 font-bold ">Purchased products:</p>
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
                            {#if order.status === "new"}
                                <p class="font-bold text-xl pt-5">Current Order Status: New order</p>
                            {:else if order.status === "cancelled"}
                                <p class="font-bold text-xl pt-5">Current Order Status: Cancelled</p>
                            {:else if order.status === "delivered"}
                                <p class="font-bold text-xl pt-5">Current Order Status: Delivered</p>
                            {:else if order.status === "in_progress"}
                                <p class="font-bold text-xl pt-5">Current Order Status: In progress</p>
                            {:else if order.status === "in_shipment"}
                                <p class="font-bold text-xl pt-5">Current Order Status: In Shipment</p>
                            {/if}
                        </div>
                        <div>
                            <p class="font-bold text-l pt-3">Metadata:</p>
                            <p class="m-2 ml-4 text-l">Order Placed by User with ID: {order.orderPlacedByUserWithId}</p>
                            <p class="m-2 ml-4 text-l">Terms of Service accepted: {order.termsAccepted}</p>
                            <p class="m-2 ml-4 text-l">Created at: {formatDateTime(order.created_at)}</p>
                            <p class="m-2 ml-4 text-l">Last Updated: {formatDateTime(order.updated_at)}</p>
                            <p class="m-2 ml-4 text-m">Stripe Session ID: {order.stripe_session_id}</p>
                        </div>
                    </div>
                    <div class="flex justify-end mt-auto">
                        <button class="bg-black hover:bg-gray-500 text-white font-bold py-2 px-4 rounded-3xl" on:click={() => startEditingOrder(order)}>
                            {editingOrderId === order.id ? 'Cancel' : 'Edit Order'}
                        </button>
                        <button class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-3xl ml-4" on:click={() => togglePopup(order.id)}>
                            Delete Order
                        </button>
                    </div>
                {/if}
            </div>
            {#if editingOrderId === order.id}
                <div class="bg-gray-100 rounded-lg shadow-lg p-4 mt-4 mb-8" transition:slide>
                    <h2 class="text-xl font-bold mb-4">Edit Order with ID {id}</h2>
                    <div class="space-y-4">
                        <p>Order Status:</p>
                        <select class="w-full p-2 border" bind:value={status}>
                            <option value="new">New order</option>
                            <option value="cancelled">Cancelled</option>
                            <option value="delivered">Delivered</option>
                            <option value="in_progress">In progress</option>
                            <option value="in_shipment">In Shipment</option>
                        </select>
                        
                        <p>Payment Status:</p>
                        <select class="w-full p-2 border" bind:value={payedStatus}>
                            <option value={true}>Payed</option>
                            <option value={false}>Not Payed</option>
                        </select>

                        <p>Total Price:</p>
                        <input class="w-full p-2 border" type="text" bind:value={totalPrice} placeholder="Total Price" />

                        <p>Payment Method:</p>
                        <select class="w-full p-2 border" bind:value={paymentMethod}>
                            <option value="Credit Card">Credit Card</option>
                            <option value="PayPal">Paypal</option>
                            <option value="Bank Transfer">Bank Transfer</option>
                        </select>

                        <p>Salutation:</p>
                        <select class="w-full p-2 border" bind:value={salutation}>
                            <option value="Mr.">Mr.</option>
                            <option value="Mrs.">Mrs.</option>
                            <option value="Mx.">Mx.</option>
                        </select>

                        <p>First Name:</p>
                        <input class="w-full p-2 border" type="text" bind:value={first_name} placeholder="First Name" />
                        
                        <p>Last Name:</p>
                        <input class="w-full p-2 border" type="text" bind:value={last_name} placeholder="Last Name" />

                        <p>Email:</p>
                        <input class="w-full p-2 border" type="text" bind:value={email} placeholder="Email" />
                        
                        <p>Phone Number:</p>
                        <input class="w-full p-2 border" type="text" bind:value={phone_number} placeholder="Phone Number" />

                        <p>Street and Number:</p>
                        <input class="w-full p-2 border" type="text" bind:value={street_and_number} placeholder="Street and Number" />

                        <p>Postal Code:</p>
                        <input class="w-full p-2 border" type="text" bind:value={postal_code} placeholder="Postal Code" />

                        <p>City:</p>
                        <input class="w-full p-2 border" type="text" bind:value={city} placeholder="City" />

                        <p>Country:</p>
                        <input class="w-full p-2 border" type="text" bind:value={country} placeholder="Country" />

                        <p>Different Shipping Address:</p>
                        <select class="w-full p-2 border" bind:value={differentShippingAddress}>
                            <option value={true}>Yes</option>
                            <option value={false}>No</option>
                        </select>

                        {#if differentShippingAddress}
                            <p>Alternative Address:</p>
                            <input class="w-full p-2 border" type="text" bind:value={alternative_address.street_and_number} placeholder="Street and Number"/>
                            <input class="w-full p-2 border" type="text" bind:value={alternative_address.postal_code} placeholder="Postal Code"/>
                            <input class="w-full p-2 border" type="text" bind:value={alternative_address.city} placeholder="City"/>
                            <input class="w-full p-2 border" type="text" bind:value={alternative_address.country} placeholder="Country"/>
                        {/if}

                        <p>Terms Accepted:</p>
                        <select class="w-full p-2 border" bind:value={termsAccepted}>
                            <option value={true}>Yes</option>
                            <option value={false}>No</option>
                        </select>
                    </div>
                    <button class="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded-3xl mt-4" on:click={updateAOrder}>
                        Update Order
                    </button>
                </div>
            {/if}
        {/each}
        {/if}
    </div>
</div>

{#if showPopup}
    <div class="fixed inset-0 z-50">
        <DeleteOrderPopup on:deleteOrderThroughPopUp={deleteOrderThroughPopUp} on:closePopup={closePopup} />
    </div>
{/if}
