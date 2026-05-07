<script>
    import { onMount } from "svelte";
    import "../../input.css";
    import Header from "$lib/components/Header.svelte";
    import Footer from "$lib/components/Footer.svelte";

    onMount(() => {
        const url = new URL(window.location.href);

        if (url.searchParams.get("success") === "true") {
            localStorage.removeItem("cart");
            localStorage.removeItem("order");
        }
    });
</script>

<head>
    <title>Thanks for ordering</title>
</head>

<Header/>
<div id="content" class="min-h-screen flex items-center justify-center -translate-y-24">
    <div class="md:p-28 p-4">
        <p class="text-3xl text-center">
            Thank you for your order, payment has been successfully received.<br>
            We will now process your order as quickly as possible.
        </p>
        <div class="flex justify-center mt-8">
            <a href="/" class="bg-black hover:bg-gray-500 text-white font-bold py-2 px-6 rounded-3xl text-xl">Back to the Shop</a>
        </div>
    </div>
</div>

<Footer/>
