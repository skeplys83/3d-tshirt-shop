<script>
    import "../../input.css";
    import Header from "$lib/components/Header.svelte";
    import Footer from "$lib/components/Footer.svelte";

</script>

<head>
    <title>Your payment Failed</title>
</head>

<Header title=""/>
<div id="content" class="min-h-screen flex items-center justify-center -translate-y-24">
    <div class="md:p-28 p-4">
        <p class="text-3xl text-center">
            Something went wrong, the payment could not be completed. <br>
            Please try again or contact us.
        </p>
        <div class="flex justify-center mt-8">
            <a href="/" class="bg-black hover:bg-gray-500 text-white font-bold py-2 px-6 rounded-3xl text-xl">Back to the Shop</a>
        </div>
    </div>
</div>

<Footer/>