<script>
    import "../../input.css";
    import Header from "$lib/components/Header.svelte";
    import Footer from "$lib/components/Footer.svelte";

</script>

<head>
    <title>Impressum</title>
</head>

<Header title="Impressum Shop-App"/>
<div id="content" class="overflow-hidden min-h-screen">
    <div id="terms" class="m-5 pb-2 md:m-10">
        <h1 class="text-2xl font-bold pb-2">Information</h1>
        <div class="bg-gray-200 rounded-xl shadow-lg flex flex-col space-y-4 md:space-y-0 relative p-4">
            <p class="font-bold">MKI-Projekt Gruppe</p>
            <p class="pt-1">Alteburgstraße 150</p>
            <p class="pt-1">72762 Reutlingen</p>
            <p class="pt-1">Baden-Württemberg</p>
            <p class="pt-1">Deutschland</p>

            <p class="font-bold pt-4">Contact</p>
            <p class="pt-1">Phone: 12345678</p>
            <p class="pt-1">E-Mail: shopcore.info@gmail.com</p>

            <p class="pt-4">$ 27a Umsatzsteuergesetz: DE XXXXXXXXXX</p>
        </div>
    </div>
</div>

<Footer/>