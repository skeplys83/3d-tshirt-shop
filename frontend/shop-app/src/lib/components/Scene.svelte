<script lang="ts">
  import { extend, T } from '@threlte/core';
  import { Stars } from '@threlte/extras';
  import ShopModel from './3D/shopModel.svelte';
  import Tshirt from './3D/tshirt.svelte';
  import { getProducts } from '../../api/products/products';
  import { onMount } from 'svelte';
  import { initialCameraPosition, productSlotPositions, selectedProductID, selectedProductPosition } from '../../stores/product_selection';
  import { cameraControls } from './cameraControls/stores';
  import CameraControls from './cameraControls/CameraControls.svelte';
  import PurchaseOverlay from './3D/purchaseOverlay.svelte';
  import PictureBillboard from './3D/pictureBillboard.svelte';
  import InteractiveBillboard from './3D/interactiveBillboard.svelte';
  import { Object3D } from 'three';
  import { showPreloader } from '../../stores/global_stores.js';
  import Preloader from './Preloader.svelte';
  import { AudioListener, Audio } from '@threlte/extras';

  extend({ Object3D });

  let products = [];
  let camera;
  let roofSpotlightFocus: Object3D;
  let productFillLightFocus: Object3D;
  let billboardSpotlight: Object3D;
  let keyboardControlsEnabled = true;
  let ambientSound;

  $: if ($cameraControls) {
    camera = $cameraControls._camera;
  }

  onMount(async () => {
    try {
      let tmp = await getProducts();

      if (tmp) {
        products = tmp;
      } else {
        console.log('No products found');
      }
      console.dir(products);
    } catch (error) {
      console.log('error: ' + error.message);
    } 

    //Add event listener for toggling controls and movement
    document.addEventListener('keydown', handleKeyPress);
    if (keyboardControlsEnabled) {
      document.addEventListener('keydown', handleKeyDown);
    }

    return () => {
      document.removeEventListener('keydown', handleKeyPress);
      document.removeEventListener('keydown', handleKeyDown);
    };
  });

  function handleKeyPress(event: KeyboardEvent) {
    if (event.key.toLowerCase() === 'p') {
      keyboardControlsEnabled = !keyboardControlsEnabled;
      console.log(`Keyboard controls ${keyboardControlsEnabled ? 'enabled' : 'disabled'}`);
      if (keyboardControlsEnabled) {
        document.addEventListener('keydown', handleKeyDown);
      } else {
        document.removeEventListener('keydown', handleKeyDown);
      }
    }
  }

  function handleKeyDown(event: KeyboardEvent) {
    if (!$cameraControls) return;

    const moveSpeed = 2; // Speed of movement
    const zoomSpeed = 5; // Speed of zooming

    switch (event.key) {
      case 'ArrowUp': // Move forward
        $cameraControls.forward(moveSpeed, true);
        break;
      case 'ArrowDown': // Move backward
        $cameraControls.forward(-moveSpeed, true);
        break;
      case 'ArrowLeft': // Move left
        $cameraControls.truck(-moveSpeed, 0, true);
        break;
      case 'ArrowRight': // Move right
        $cameraControls.truck(moveSpeed, 0, true);
        break;
      case '+': // Zoom in
      case '=': // Zoom in (alternative key)
        $cameraControls.dolly(-zoomSpeed, true);
        break;
      case '-': // Zoom out
        $cameraControls.dolly(zoomSpeed, true);
        break;
    }
  }

</script>

<T.PerspectiveCamera
  makeDefault
  position={[30, 5, -15]}
  fov={50}
>
  <CameraControls
    on:create={({ ref }) => {
      $cameraControls = ref
      $cameraControls.smoothTime = 0.3;
      $cameraControls.maxDistance = 120;
      $cameraControls.minDistance = 20;
      $cameraControls.maxPolarAngle = Math.PI * 0.515;
      $cameraControls.minAzimuthAngle = Math.PI * 0.2;
      $cameraControls.maxAzimuthAngle = Math.PI * 1.55;
      $cameraControls.mouseButtons.right = 0;
      $cameraControls.draggingSmoothTime = 0.08;

      $cameraControls.setLookAt(
        //camera Position
        $initialCameraPosition[0], 
        $initialCameraPosition[1], 
        $initialCameraPosition[2],
        //lookAt position
        $selectedProductPosition[0], 
        $selectedProductPosition[1] + 2, 
        $selectedProductPosition[2], 
        false
      )

      $: if($showPreloader){
        setTimeout(() => {
          showPreloader.set(false)

          $cameraControls.rotateTo(Math.PI * 0.6, Math.PI * 0.5, true)
          $cameraControls.dollyTo(35,true)
        }, 1500)
      }

      setTimeout(() => {
        ambientSound.play()
      }, 90000) //90s
    }}
  />
</T.PerspectiveCamera>

<AudioListener
  masterVolume = {0.5}
/>

<Audio src={'./static/sounds/Ambient.mp3'} bind:this={ambientSound} />

<Stars 
  count={10000}
  depth={0}
  radius={800}
  factor={30}
/>

<!-- <T.AmbientLight intensity={0.5} /> -->

<!-- Ball -->
<!-- <T.Mesh position={[1, 23, 7]}>
  <T.SphereGeometry radius={5.0}/>
</T.Mesh> -->

<!--Top Down light that Covers the entire scene-->
<T.SpotLight
  color="#ffffff"
  intensity={500}
  position={[0, 100, 0]}
  angle={0.5}
  penumbra={1.0}
  decay={1.5}
/>

<!--Inside Light-->
<T.SpotLight
  color="#ffffff"
  intensity={300}
  position={[0, 13.5, 0]}
  angle={1.4}
  penumbra={0.2}
  decay={2.0}
/>

<!--Left Roof Spotights Target-->
<T.Object3D
  bind:ref={productFillLightFocus}
  position={[0,6,0]}
/>
<!--Product Front Fill Light #FFa0a0 -->
{#if $selectedProductID !== -1}
  <T.SpotLight
    color="#ffffff" 
    intensity={500}
    position={[10, 8, -10]}
    target={productFillLightFocus}
    angle={0.4}
    penumbra={0.3}
    decay={2.0}
  />
{/if}

<!--Left Building Billboard Target -->
<T.Object3D
  bind:ref={billboardSpotlight}
  position={[0.5, 23, 7]}
/>

<!--Left Building Billboard Light-->
<T.SpotLight
  color="#ffffff"
  intensity={150}
  position={[0, 23, 0]}
  target={billboardSpotlight}
  angle={0.9}
  penumbra={0.2}
  decay={2.0}
/>

<!--Latern-->
<T.PointLight 
  color="#7b00ff"
  intensity={160}
  distance={0}
  decay={2.0}
  position={[11, 12, 6.3]}
/>

<!--Left Roof Spotights Target-->
<T.Object3D
  bind:ref={roofSpotlightFocus}
  position={[-16, 19, 3]}
/>

<!--Roof Light Left-->
<T.SpotLight
  color="#0000ff"
  intensity={200}
  position={[-11, 12, -3]}
  target={roofSpotlightFocus}
  angle={0.7}
  penumbra={0.2}
  decay={2.0}
/>

<!--Roof Light Right-->
<T.SpotLight
  color="#ff0000"
  intensity={200}
  position={[-20, 12, -3]}
  target={roofSpotlightFocus}
  angle={0.7}
  penumbra={0.2}
  decay={2.0}
/>

<ShopModel
  position={[0, 0, 0]}
  rotation={[-Math.PI / 2, 0, 0]}   
  renderOrder={1} 
  depthWrite={true} 
/>

{#each products as product, index}
  <Tshirt
    productData={product}
    startPosition={$productSlotPositions[index]} 
    startRotation={[0, Math.PI/2, 0]}
  />
{/each}

{#if $selectedProductID !== -1} 
  <PurchaseOverlay productData = {products}/>
{/if}

<!-- Overlays & Billboards -->
{#if !$showPreloader}
  <PictureBillboard />
  <InteractiveBillboard />
{/if}
  
<Preloader />
