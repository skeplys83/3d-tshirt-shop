<script>
  import App from '$lib/components/App.svelte'
  import "../input.css";
  import Notification from "$lib/components/messages/Notification.svelte";
</script>

<head>
  <title>The best shop in the World!</title>
</head>

<div>
  <App />
</div>

<style>
  :global(body) {
    margin: 0;
  }

  div {
    width: 100svw;
    height: 100svh;
    background-color: #0f0306;
  }
</style>
