<script>
    import {onMount} from "svelte";
    import { setCsrfToken, setUserInfo } from '$lib/index.js';
    import favicon from '$lib/images/favicon.ico';

    onMount(async () => {
        setCsrfToken();
        await setUserInfo();
    })
</script>

<svelte:head>
  <link rel="icon" type="image/x-icon" href={favicon} />
</svelte:head>

<slot />
