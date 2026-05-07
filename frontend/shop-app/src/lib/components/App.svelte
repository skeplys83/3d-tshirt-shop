<script lang="ts">
  import { Canvas } from '@threlte/core'
  import Scene from './Scene.svelte'
  import Notification from '$lib/components/messages/Notification.svelte';
  import Preloader from './Preloader.svelte';
  import arrow from '$lib/images/arrow.png';
  import shoppingCart from '$lib/images/shoppingCart.png';
  import { onMount } from 'svelte';
  import { getUserInfo } from '../../api/auth/auth';
  import { setCsrfToken } from "$lib";
  import {addMessage} from "../../stores/global_stores.js";
  import { logout } from '../../api/auth/auth.js'
  import { PerfMonitor, Sky } from '@threlte/extras';
  import { selectedProductID, initialCameraPosition, selectedProductPosition } from '../../stores/product_selection';
  import { cameraControls } from './cameraControls/stores';
  import { cartItemCount, updateCartItemCount } from '../../stores/product_selection';
  import { Audio } from '@threlte/extras'

  let isDropdownOpen = false;
  let userAuthenticated = false;
  let user = {};

  let camera;
  $: if ($cameraControls) {
    camera = $cameraControls._camera;
  }

  const toggleDropdown = () => {
    isDropdownOpen = !isDropdownOpen;
  };

  async function handleLogout() {
    try {
      const response = await logout();
      addMessage({ type: 'success', text: 'Successfully logged out'});
      userAuthenticated = false;
    } catch (error) {
      addMessage({ type: 'error', text: 'Logout failed: ' + (error.message || 'Unknown error')});
    }
  }

  const handleCameraControl = () => {
    $cameraControls.setLookAt(
      -9.5, 7.5, -10, 
      -9.5, 7.5,  -8,   
      true 
    );
  };

  onMount(async () => {
    setCsrfToken();

    try {
      const userResponse = await getUserInfo();

      let skipUserAuthentication = false;

      if (!userResponse || userResponse.error || userResponse == null || userResponse === undefined) {
        skipUserAuthentication = true;
        userAuthenticated = false;
      }

      if (!skipUserAuthentication) {
        userAuthenticated = true;
        user = userResponse;
      }
    } catch (error) {
      userAuthenticated = false;
    }

    updateCartItemCount();

    window.addEventListener("storage", updateCartItemCount);
  });
</script>

<div style="position: relative; width: 100%; height: 100vh;">
  <Notification />
  <Preloader />

  {#if $selectedProductID === -1}
  <div class="absolute top-0 right-0 m-4 pointer-events-none">
    <div class="pointer-events-auto flex items-center space-x-4 p-3">
        <button 
        class="bg-white rounded-full p-3 hover:bg-lightGrey" 
        on:click={(event) => {
            handleCameraControl()
        }}
        >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        </button>
        <a href="/shoppingBasket" class="mr-3 bg-white rounded-full p-3 hover:bg-lightGrey">
            <img src="{shoppingCart}" class="h-8 w-8" alt="Shopping Cart">
            {#if $cartItemCount > 0}
                <span class="absolute transform translate-x-7 -translate-y-12 bg-black text-white text-xs font-bold rounded-full h-5 w-5 flex items-center justify-center">
                    {$cartItemCount}
                </span>
            {/if}
        </a>
        {#if !userAuthenticated}        
          <a href="/login" class="bg-white hover:bg-lightGrey px-6 py-3 rounded-2xl text-xl font-bold">Login</a>
        {:else}
          <div class="relative">
            <button 
                class="bg-white hover:bg-lightGrey px-6 py-3 rounded-2xl text-xl font-bold flex items-center" 
                on:click={toggleDropdown}
            >
                {user.first_name} {user.last_name}
                <img 
                    src="{arrow}" 
                    alt="Arrow" 
                    class="ml-4 h-3 w-6 transition-transform duration-300" 
                    style="transform: rotate({isDropdownOpen ? '180deg' : '0deg'});"
                />
            </button>
            {#if isDropdownOpen}
                <div class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg">
                    <a href="/profile" class="block px-4 py-2 hover:bg-lightGrey">View profile</a>
                    {#if user.is_staff === true}
                      <a href="/adminBoard" class="block px-4 py-2 hover:bg-lightGrey">Admin Board</a>
                    {/if}
                    <button on:click={handleLogout} class="block px-4 py-2 hover:bg-lightGrey w-full text-left">Logout</button>
                </div>
            {/if}
        </div>
        {/if}
    </div>
  </div>
  {/if}
  
  <Canvas class="w-full h-full">
    <!-- <PerfMonitor anchorX={'left'} anchorY={'bottom'} logsPerSecond={30} visible={$selectedProductID === -1}/>  -->

    <Sky
      setEnvironment={true}
      turbidity={10.0}
      rayleigh={3.0}
      azimuth={-110}
      elevation={-2}
      mieCoefficient={0.005}
      mieDirectionalG={0.7}
    />

    <Scene />
  </Canvas>
</div>