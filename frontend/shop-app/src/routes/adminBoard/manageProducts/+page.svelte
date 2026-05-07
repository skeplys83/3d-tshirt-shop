<script>
    import "../../../input.css";
    import {getProducts, putProduct, uploadProductFiles} from "../../../api/products/products.js";
    import {onMount} from "svelte";
    import {setCsrfToken} from "$lib";
    import {addMessage} from "../../../stores/global_stores";
    import Notification from "$lib/components/messages/Notification.svelte";
    import arrow from '$lib/images/arrow.png';
    import {slide} from 'svelte/transition';
    import DeleteProductPopup from "../../../lib/components/popUps/deleteProduct.svelte";
    import {deleteProduct} from "../../../api/products/products";
    import Header from "$lib/components/Header.svelte";

    let products = [];
    let expandedProducts = {};
    let editingProductId = null;
    let isLoading = true;
    let isError = false;

    let showPopup = false;
    let currentProductId = null;

    // Felder zum Bearbeiten eines Produkts
    let id = '';
    let name = '';
    let description = '';
    let price = 0;
    let stripePriceId = '';
    let stockEntries = [{ size: '', quantity: '' }];
    let productBlenderModel;
    let productPicture;
    let colors = [''];
    let categories = [''];
    let discount = false;
    let discountInPercent = 0;

    // Produkte laden
    onMount(async () => {
        setCsrfToken();
        try {
            products = await getProducts();
            isLoading = false;
            addMessage({ type: 'success', text: 'Products loaded successfully' });
        } catch (error) {
            addMessage({ type: 'error', text: 'Failed to load products: ' + (error.message || 'Unknown error') });
            isLoading = false;
            isError = true;
        }
    });

    function toggleProductDetails(productId) {
        if (!editingProductId || editingProductId === productId) {
            expandedProducts[productId] = !expandedProducts[productId];
        }
    }

    function startEditingProduct(product) {
        if (editingProductId === product.id) {
            editingProductId = null;
        } else {
            editingProductId = product.id;
            expandedProducts[product.id] = true;

            id = product.id;
            name = product.name;
            description = product.description;
            price = product.price;
            stripePriceId = product.stripePriceId;
            productBlenderModel = product.productBlenderModel;
            productPicture = product.productPicture;
            discount = product.discount;
            discountInPercent = product.discountInPercent;

            stockEntries = Object.entries(product.stock).map(([size, quantity]) => {
                return { size, quantity };
            });
            stockEntries.push({ size: "", quantity: null });
            
            colors = [...product.colors];
            colors.push("");

            categories = [...product.category];
            categories.push("");
        }
    }


    async function updateAProduct() {
        if (!validateStockEntries()) {
            addMessage({ type: 'error', text: 'Add at least one size and the corresponding stock and make sure that both are filled in.' });
            return;
        }

        if (!validateColors()) {
            addMessage({ type: 'error', text: 'Please add at least one color.' });
            return;
        }

        if (!validateCategories()) {
            addMessage({ type: 'error', text: 'Please add at least one category.' });
            return;
        }

        const stock = stockEntries.reduce((acc, entry) => {
            if (entry.size && entry.quantity) {
                acc[entry.size] = parseInt(entry.quantity, 10);
            }
            return acc;
        }, {});

        if (Object.keys(stock).length === 0) {
            addMessage({ type: 'error', text: 'Add at least one size and the corresponding stock and make sure that both are filled in.' });
            return;
        }

        const filteredColors = colors.filter(color => color.trim() !== '');
        const filteredCategories = categories.filter(category => category.trim() !== '');

        try {


            await putProduct(id, name, description, price, stripePriceId, stock, filteredColors, filteredCategories, discount, discountInPercent);

            if (productPicture || productBlenderModel) {
                try {
                    await uploadProductFiles(id, productPicture, productBlenderModel);
                }catch (error){
                    addMessage({ text: 'Picture/Model update failed or not provided' });
                }
            }

            addMessage({ type: 'success', text: 'Product updated successfully' });
            editingProductId = null;
        } catch (error) {
            addMessage({ type: 'error', text: 'Failed to update product: ' + (error.message || 'Unknown error') });
        }

        products = await getProducts();
    }

    const validateStockEntries = () => {
        return stockEntries.every(entry => (entry.size && entry.quantity) || (!entry.size && !entry.quantity));
    };

    const validateColors = () => {
        return colors.some(color => color.trim() !== '');
    };

    const validateCategories = () => {
        return categories.some(category => category.trim() !== '');
    };

    const handleStockInputChange = (index) => {
        const currentEntry = stockEntries[index];
        if (currentEntry.size && currentEntry.quantity && index === stockEntries.length - 1) {
            stockEntries = [...stockEntries, { size: '', quantity: '' }];
        }
    };

    const handleColorInputChange = (index) => {
        if (colors[index].trim() && index === colors.length - 1) {
            colors = [...colors, ''];
        }
    };

    const handleCategoryInputChange = (index) => {
        if (categories[index].trim() && index === categories.length - 1) {
            categories = [...categories, ''];
        }
    };

    function handleFileChange(event, type) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                let base64Data = reader.result;
                if (type === 'productPicture') {
                    // Präfix für Bilder entfernen
                    base64Data = base64Data.replace(/^data:image\/[a-z]+;base64,/, '');
                    productPicture = base64Data;
                } else if (type === 'productBlenderModel') {
                    // Präfix für .glb-Dateien entfernen
                    base64Data = base64Data.replace(/^data:application\/octet-stream;base64,/, '');
                    productBlenderModel = base64Data;
                }
            };
            reader.readAsDataURL(file);
        }
    }

    function createImageUrl(base64String) {
        return `data:image/png;base64,${base64String}`;
    }

    function togglePopup(id) {
        currentProductId = id;
        showPopup = !showPopup;
    }

    function closePopup() {
        showPopup = false;
    }


    async function deleteProductThroughPopUp() {
        if (currentProductId) {
            handleDeleteProduct(currentProductId);
        }
        showPopup = false;
    }

    async function handleDeleteProduct(productId) {
        try {
            await deleteProduct(productId);
            addMessage({ type: 'success', text: 'Product deleted successfully' });
            products = await getProducts();
        } catch (error) {
            addMessage({ type: 'error', text: 'Failed to delete product: ' + (error.message || 'Unknown error') });
        }
    }
</script>

<head>
    <title>Admin Board - Manage products</title>
</head>

<Notification />
<Header title="Manage products"/>
<div id="content" class="">
    <div>
        <div class="flex justify-end mr-4 md:mr-10">
            <a href="/adminBoard/manageProducts/createNewProduct" class="bg-green-500 hover:bg-green-600 text-white font-bold text-xl py-2 px-4 rounded-3xl mt-4">
                Create New Product
            </a>
        </div>
    </div>
    <div class="m-5 pb-2 md:m-10">
        {#if isLoading}
            <div class="flex space-x-2 justify-center items-center mt-10">
                <div class='h-5 w-5 bg-black rounded-full animate-bounce [animation-delay:-0.3s]'></div>
                <div class='h-5 w-5 bg-black rounded-full animate-bounce [animation-delay:-0.15s]'></div>
                <div class='h-5 w-5 bg-black rounded-full animate-bounce'></div>
            </div>
        {:else if isError}
            <p class="text-center mt-10 font-bold text-xl text-red-600">Oops, something went wrong..</p>
        {:else if products.length === 0}
            <p class="text-center mt-5 font-bold text-xl">No products found</p>
        {:else}
            {#each products as product}
                <div class="bg-gray-200 rounded-xl shadow-lg flex flex-col space-y-4 md:space-y-0 p-4 relative mb-6">
                    <!-- svelte-ignore a11y-click-events-have-key-events -->
                    <!-- svelte-ignore a11y-no-static-element-interactions -->
                    <div class="flex justify-between items-center cursor-pointer hover:opacity-60" on:click={() => toggleProductDetails(product.id)}>
                        <p class="font-bold text-xl">{product.name} (ID: {product.id})</p>
                        <img
                                src={arrow}
                                alt="arrow"
                                class="transition-transform duration-300 w-12 h-7"
                                style="transform: rotate({expandedProducts[product.id] ? '180deg' : '0deg'});"
                        />
                    </div>

                    {#if expandedProducts[product.id]}
                        <div class="mt-2" transition:slide>
                            <div class="flex flex-col sm:flex-row sm:space-x-6 md:space-y-0 pt-3">
                                <img src={createImageUrl(product.productPicture)} alt={product.name} class="w-24 h-24 pb-2"/>
                                <div class="pl-2 sm:pl-0">
                                    <p class="mt-1"><span class="font-semibold">Description:</span> {product.description}</p>
                                    <p class="mt-1"><span class="font-semibold">Price:</span> {product.price} €</p>
                                    <p class="mt-1"><span class="font-semibold">Stripe Price ID:</span> {product.stripePriceId}</p>
                                </div>
                            </div>
                            <div class="flex flex-col sm:flex-row sm:space-y-0 sm:space-x-6">
                                <div class="flex-1 rounded-lg p-2 ">
                                    <p class="font-semibold mt-3">Stock:</p>
                                    <ul class="ml-4">
                                        {#each Object.entries(product.stock) as [size, quantity]}
                                            <li>Size {size}: <span class="font-semibold">{quantity}</span></li>
                                        {/each}
                                    </ul>
                                </div>
                                <div class="flex-1 rounded-lg p-2">
                                    <p class="font-semibold mt-3"> Available Colors:</p>
                                    <ul class="ml-4">
                                        {#each product.colors as color}
                                            <li>- {color}</li>
                                        {/each}
                                    </ul>
                                </div>
                                <div class="flex-1 rounded-lg p-2">
                                    <p class="font-semibold mt-3"> Categories:</p>
                                    <ul class="ml-4">
                                        {#each product.category as category}
                                            <li>- {category}</li>
                                        {/each}
                                    </ul>
                                </div>
                            </div>                   

                            <div class="flex justify-end mt-auto">
                                <button class="bg-black hover:bg-gray-500 text-white font-bold py-2 px-4 rounded-3xl mb-3" on:click={() => startEditingProduct(product)}>
                                    {editingProductId === product.id ? 'Cancel' : 'Edit Product'}
                                </button>
                                <button class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-3xl mb-3 ml-4" on:click={() => togglePopup(product.id)}>
                                    Delete Product
                                </button>
                            </div>
                        </div>

                        {#if editingProductId === product.id}
                            <div class="bg-gray-100 rounded-lg shadow-lg p-4 mt-4 mb-8" transition:slide>
                                <h2 class="text-xl font-bold mb-4">Edit Product with ID {id}</h2>
                                <form on:submit|preventDefault={updateAProduct} class="space-y-4">
                                    <div>
                                        <label class="block text-gray-700 text-sm font-bold mb-1" for="email">Name:</label>
                                        <input
                                                id="name"
                                                type="text"
                                                bind:value={name}
                                                class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500"
                                                required
                                        />
                                    </div>
                                    <div>
                                        <label class="block text-gray-700 text-sm font-bold mb-1" for="description">Description:</label>
                                        <input
                                                id="description"
                                                type="text"
                                                bind:value={description}
                                                class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500"
                                                required
                                        />
                                    </div>
                                    <div>
                                        <label class="block text-gray-700 text-sm font-bold mb-1" for="price">Price:</label>
                                        <input
                                                id="price"
                                                type="number"
                                                min="0"
                                                step="0.01"
                                                bind:value={price}
                                                class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500"
                                                required
                                        />
                                    </div>
                                    <div>
                                        <label class="block text-gray-700 text-sm font-bold mb-1" for="stripePriceId">Stripe Price ID:</label>
                                        <input
                                                id="stripePriceId"
                                                type="text"
                                                bind:value={stripePriceId}
                                                class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500"
                                                required
                                        />
                                    </div>
                                    <div>
                                        <!-- svelte-ignore a11y-label-has-associated-control -->
                                        <label class="block text-gray-700 text-sm font-bold mb-1">Size and Stock:</label>
                                        {#each stockEntries as entry, index}
                                            <div class="flex space-x-2 mb-2">
                                                <input
                                                    type="text"
                                                    placeholder="Size (e.g., S, M, L)"
                                                    bind:value={entry.size}
                                                    on:input={() => handleStockInputChange(index)}
                                                    class="w-1/2 px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500"
                                                />
                                                <input
                                                    type="number"
                                                    min="0"
                                                    placeholder="Quantity"
                                                    bind:value={entry.quantity}
                                                    on:input={() => handleStockInputChange(index)}
                                                    class="w-1/2 px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500"
                                                />
                                            </div>
                                        {/each}
                                    </div>
                                    <div>
                                        <!-- svelte-ignore a11y-label-has-associated-control -->
                                        <label class="block text-gray-700 text-sm font-bold mb-1">Colors:</label>
                                        {#each colors as color, index}
                                            <div class="mb-2">
                                                <input
                                                    type="text"
                                                    placeholder="Color (e.g., White, Black)"
                                                    bind:value={colors[index]}
                                                    on:input={() => handleColorInputChange(index)}
                                                    class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500"
                                                />
                                            </div>
                                        {/each}
                                    </div>
                                    <div>
                                        <!-- svelte-ignore a11y-label-has-associated-control -->
                                        <label class="block text-gray-700 text-sm font-bold mb-1">Categories:</label>
                                        {#each categories as category, index}
                                            <div class="mb-2">
                                                <input
                                                    type="text"
                                                    placeholder="Category (e.g., T-Shirts, Hoodies)"
                                                    bind:value={categories[index]}
                                                    on:input={() => handleCategoryInputChange(index)}
                                                    class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500"
                                                />
                                            </div>
                                        {/each}
                                    </div>
                                    <div>
                                        <!-- svelte-ignore a11y-label-has-associated-control -->
                                        <label class="block text-gray-700 text-sm font-bold mb-1">Product Picture:</label>
                                        <input 
                                            class="w-full p-2 border" 
                                            type="file" accept="image/*" 
                                            required
                                            on:change={(event) => handleFileChange(event, 'productPicture')} 
                                        />
                                    </div>
                                    <div>
                                        <!-- svelte-ignore a11y-label-has-associated-control -->
                                        <label class="block text-gray-700 text-sm font-bold mb-1">Product Blender Model:</label>
                                        <input 
                                            class="w-full p-2 border" 
                                            type="file" accept=".glb"
                                            on:change={(event) => handleFileChange(event, 'productBlenderModel')}
                                        />
                                    </div>
                                    <div>
                                        <label class="block text-gray-700 text-sm font-bold mb-1" for="discount">Discount:</label>
                                        <div class="flex items-center space-x-2 pl-2">
                                            <input
                                                id="discount"
                                                type="checkbox"
                                                bind:checked={discount}
                                                class="w-4 h-4 text-gray-500 border-gray-300 rounded focus:ring focus:ring-gray-500 focus:border-gray-500"
                                            />
                                            <span>Should the product have a discount?</span>
                                        </div>
                                    </div>
                                    {#if discount}
                                        <div>
                                            <label class="block text-gray-700 text-sm font-bold mb-1" for="discountInPercent">Discount in percent:</label>
                                            <input
                                                    id="discountInPercent"
                                                    type="number"
                                                    min="0"
                                                    max="100"
                                                    step="1"
                                                    bind:value={discountInPercent}
                                                    class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring ring-gray-500 focus:border-gray-500"
                                            />
                                        </div>
                                    {/if}
                                    <button class="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded-3xl mt-4" on:click={updateAProduct}>
                                        Update Product
                                    </button>
                                </form>
                            </div>
                        {/if}
                    {/if}
                </div>
            {/each}
        {/if}
    </div>
</div>

{#if showPopup}
    <div class="fixed inset-0 z-50">
        <DeleteProductPopup on:deleteProductThroughPopUp={deleteProductThroughPopUp} on:closePopup={closePopup} />
    </div>
{/if}