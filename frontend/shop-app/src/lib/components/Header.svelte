<script>
    import Logo from "$lib/images/Logo.png";

    export let title = '';
</script>

<div class="flex flex-row items-center w-full">   
    <a href="/">
        <img src={Logo} alt="Logo" class="w-12 md:w-16 md:mt-8 md:ml-8 mt-3 ml-3" />
    </a>
    <h1 class="md:text-3xl text-2xl font-bold pb-2 text-center flex-grow px-2 mt-3">{title}</h1>
    <div class="w-12 md:w-16 md:mt-8 md:ml-8 mt-3 ml-3"></div>
</div>