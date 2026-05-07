<script>
    import "../../input.css";
    import Header from "$lib/components/Header.svelte";
    import Footer from "$lib/components/Footer.svelte";

</script>

<head>
    <title>About us</title>
</head>

<Header title="About us"/>
<div id="content" class="overflow-hidden min-h-screen">
    <div id="terms" class="m-5 pb-2 md:m-10">
        <h1 class="text-2xl font-bold pb-2">Information</h1>
        <div class="bg-gray-200 rounded-xl shadow-lg flex flex-col space-y-4 md:space-y-0 relative p-4">
            <p>This is a group project for the MKI Project.</p>
        </div>
    </div>
</div>

<Footer/>