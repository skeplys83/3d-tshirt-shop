<script lang="ts">
  import { HTML } from '@threlte/extras';
  import { onMount } from 'svelte';
  import { cameraControls } from '../cameraControls/stores';
  import { Audio } from '@threlte/extras';

  //Billboard 1
  const imagePosition = [7.6, 22.8, 13.1]; // x, y, z coordinates
  const rotation = [0, Math.PI / 2, 0];

  //Billboard 2
  const imagePosition2 = [1.0, 22.8, 6.45]; // x, y, z coordinates
  const rotation2 = [0, Math.PI, 0];

  const imagePaths = [
    "Billboards/BillboardImage2.jpg",
    "Billboards/BillboardImage3.jpg",
    "Billboards/BillboardImage1.jpg",
    "Billboards/BillboardImage4.jpg",
    "Billboards/BillboardImage5.jpg"
  ];

  let currentImageIndex = 0;
  let currentImage = imagePaths[currentImageIndex];
  let currentImage2 = imagePaths[(currentImageIndex + 2) % imagePaths.length];

   // Camera target coordinates
   const cameraTarget = {
    position: [22, 6, -5],
    lookAt: [0.5,5.0,-0.45],
  };

    // Function to focus the camera
    function focusCamera() {
    if ($cameraControls) {
      $cameraControls.setLookAt(
        ...cameraTarget.position, 
        ...cameraTarget.lookAt,   
        true                     
      );
    }
  }

  onMount(() => {
    const interval = setInterval(() => {
      currentImageIndex = (currentImageIndex + 1) % imagePaths.length;
      currentImage = imagePaths[currentImageIndex];
      currentImage2 = imagePaths[(currentImageIndex + 2) % imagePaths.length];
    }, 5000);

    return () => clearInterval(interval);
  });

  let wosh1: Audio;
</script>

<Audio src={'./static/sounds/wosh1.flac'} bind:this={wosh1} />

<HTML
  position={imagePosition}
  rotation={rotation}
  occlude={true}
  transform
>
  <div
    style="width: 33rem; height: 20rem; transform-origin: center center; cursor: pointer;"
    on:click={() => {
      focusCamera();
      wosh1.play();
    }}
  >
    <img
      src={currentImage}
      alt="Billboard"
      style="width: 100%; height: 100%; object-fit: cover;"
    />
  </div>
</HTML>


<!-- <HTML
  position={imagePosition2}
  rotation={rotation2}
  occlude={true}
  transform
>
  <div
    style="width: 33rem; height: 20rem; transform-origin: center center;"
    on:click={() => {
      focusCamera();
    }}
  >
    <img
      src={currentImage2}
      alt="Billboard"
      style="width: 100%; height: 100%; object-fit: cover;"
    />
  </div>
</HTML> -->