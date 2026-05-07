<script lang="ts">
    import { showPreloader } from '../../stores/global_stores.js';
    import Spinner from '$lib/images/Spinner.gif';
  </script>
  
  <style>
    .preloader {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(0, 0, 0, 1);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      z-index: 99999;
      color: white;
      font-family: Arial, sans-serif;
      font-size: 1.2rem;
    }
  
    .preloader img {
      margin-bottom: 1rem;
    }
  </style>
  
  {#if $showPreloader}
    <div class="preloader">
      <img src="{Spinner}" alt="Loading..." />
      <p>Loading the best shop in the world. Please wait...</p>
    </div>
  {/if}
  