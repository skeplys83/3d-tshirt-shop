<script>
    import "../../../../input.css";
    import {addMessage} from "../../../../stores/global_stores";
    import Notification from "$lib/components/messages/Notification.svelte";
    import { postProduct } from "../../../../api/products/products";
    import { goto } from "$app/navigation";
    import Header from "$lib/components/Header.svelte";

    let name = '';
    let description = '';
    let price = '';
    let stripePriceId = '';
    let stockEntries = [{ size: '', quantity: '' }];
    let colors = [''];
    let categories = ['']; 
    let discount = false;
    let discountInPercent = 0;
    let productBlenderModel;
    let productPicture;

    const createProduct = async () => {
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
            await postProduct(name, description, price, stripePriceId, stock, filteredColors, filteredCategories, discount, discountInPercent, productPicture, productBlenderModel);
            addMessage({ type: 'success', text: 'Product creation succeeded'});
            await goto('/adminBoard/manageProducts');
        } catch (error) {
            addMessage({ type: 'error', text: 'Product creation failed: ' + (error.message || 'Unknown error')});
        }
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
                // Präfix `data:image/png;base64,` entfernen
                base64Data = base64Data.replace(/^data:image\/[a-z]+;base64,/, '');
                if (type === 'productPicture') {
                    productPicture = base64Data;
                } else if (type === 'productBlenderModel') {
                    productBlenderModel = base64Data;
                }
            };
            reader.readAsDataURL(file);
        }
    }
</script>

<head>
    <title>Manage products - Create New Product</title>
</head>

<Notification />
<Header title="Create New Product" />
<div id="content" class="">
    <div class="m-5 pb-2 md:m-10">
        <h1 class="text-2xl font-bold pb-2">New Product</h1>
        <div class="bg-gray-200 rounded-xl shadow-lg flex flex-col space-y-4 md:space-y-0 relative p-4">
            <form on:submit|preventDefault={createProduct} class="space-y-4">
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
                        type="file" accept=".blend" 
                        on:change={(event) => handleFileChange(event, 'blenderModel')} 
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
                <button
                    type="submit"
                    class="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded-3xl mt-4"
                >
                    Create Product
                </button>
            </form>    
        </div>
    </div>
</div>