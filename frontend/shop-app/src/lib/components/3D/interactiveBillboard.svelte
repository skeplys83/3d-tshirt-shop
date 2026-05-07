<script lang="ts">
  import { T } from "@threlte/core";
  import { Audio, HTML } from "@threlte/extras";
  import { writable } from 'svelte/store';
  import { onMount, onDestroy } from 'svelte';
  import { cameraControls } from '../cameraControls/stores';
  
  const showCover = writable(true);
  const currentPage = writable(0);
  let timer;

  let boardVisible = true;

  setInterval(() => {
    boardVisible = $cameraControls.azimuthAngle > 2.87 && $cameraControls.azimuthAngle < Math.PI * 1.45;
  }, 30)

 // Camera position coordinates
  let x = 0;
  let y = 0;
  let z = 0;

  function updateCoordinates() {
    if ($cameraControls) {
      const position = $cameraControls.getPosition();
      x = position.x;
      y = position.y;
      z = position.z;
    }
  }

  function resetTimer() {
    clearTimeout(timer);
    timer = setTimeout(() => {
      showCover.set(true); // Show cover again after 20 seconds
    }, 20000);
  }

  let updateInterval: number;

  onMount(() => {
    wosh2.play();

    // Update coordinates every 100ms
    updateInterval = setInterval(updateCoordinates, 100);
    if ($cameraControls) {
      $cameraControls.addEventListener('update', updateCoordinates);
    }

    showCover.subscribe((value) => {
      if (!value) {
        resetTimer(); // Reset the timer
        initfocusCamera(); // Focus camera on the initial position
      }
    });

    return () => {
      clearTimeout(timer);
      clearInterval(updateInterval);
      if ($cameraControls) {
        $cameraControls.removeEventListener('update', updateCoordinates);
      }
    };
  });

  // Focus the camera to the initial view
  function initfocusCamera() {
    if ($cameraControls) {
      $cameraControls.setLookAt(
        -9.5, 7.5, -10, 
        -9.5, 7.5,  -8,   
        true 
      );

      clickSound.play();
    }
  }

  function focusCamera({ position, lookAt }: { position: number[]; lookAt: number[] }) {
    if ($cameraControls) {
      $cameraControls.setLookAt(...position, ...lookAt, true);
    }
  }

  const pages = [
    {
      title: "Tea Shirt Shop",
      content: "Welcome to our 3D T-shirt shop! This project show cases innovation in digital retail.",
      icon: "https://img.icons8.com/?size=100&id=86527&format=png&color=000000",
      coordinates: { position: [22, 6, -5], lookAt: [0.5,5.0,-0.45] }
    },
    {
      title: "Our Tea-Shirts",
      content: "Our T-shirts are crafted from 100% fairly produced cotton, ensuring comfort and sustainability.",
      icon: "https://img.icons8.com/?size=100&id=87780&format=png&color=000000",
      coordinates: { position: [9.6, 9.5, -1], lookAt: [-5, 8, -1] }
    },
    {
      title: "Artwork Gallery",
      content: "Explore our unique collection of artwork featured as designs on our T-shirts.",
      icon: "https://img.icons8.com/?size=100&id=86317&format=png&color=000000",
      coordinates: { position: [16, 23, 13.2], lookAt: [13, 23, 13.2] }
    },
    {
      title: "Virutal Try-On",
      content: "You can try on our T-shirts virtually by clicking on the 'Try-On' button.",
      icon: "https://img.icons8.com/?size=100&id=105719&format=png&color=000000",
      coordinates: { position: [9.6, 9.5, -1], lookAt: [-5, 8, -1]}
    },
    {
      title: "Credits",
      content: "This project was developed by a passionate team of MKI students from Reutlingen University. More details can be found on the credits page.",
      icon: "https://img.icons8.com/?size=100&id=89709&format=png&color=000000",
      coordinates: { position: [-42.5, 7.5, 3], lookAt: [-39.5, 7.2, 3] }
    },
    {
      title: "Anleitung",
      content: "To navigate the shop, simply click and drag to pivot the camera, and use the mouse wheel to zoom in and out. ",
      icon: "https://img.icons8.com/?size=100&id=84161&format=png&color=000000",
      coordinates: { position: [13, 4, -2], lookAt: [12, 3.5, -1]}
    }
  ];

  let clickSound: Audio;
  let wosh2: Audio;
  </script>

  <Audio src={'./static/sounds/click.wav'} bind:this={clickSound} />
  <Audio src={'./static/sounds/wosh2.flac'} volume={0.5} bind:this={wosh2} />
  
  {#if boardVisible}
    <HTML position={[-9.3, 7.5, -4]} rotation={[0, Math.PI, 0]} transform>
      <div class="w-[146px] h-[160px] relative">
        <!-- Main Content -->
        <div class="w-full h-full bg-black text-white text-[0.7rem] rounded-lg overflow-hidden p-0 flex">
          <!-- Sidebar Navigation -->
          <div class="w-[30px] flex flex-col gap-1 items-center p-1">
            {#each pages as page, i}
              <button
                on:click={() => { {
                  clickSound.stop();
                  clickSound.play();
                  resetTimer(); $currentPage = i;
                }}}
                class="w-5 h-5 border-none rounded-full flex items-center justify-center cursor-pointer"
                style="background: {$currentPage === i ? '#ffffff' : '#333333'};"
              >
                <img src={page.icon} alt="icon" class="w-2.5 h-2.5" style="opacity: {$currentPage === i ? 1 : 0.6};" />
              </button>
            {/each}
          </div>
    
          <!-- Content Area -->
          <div class="flex-1 p-1 flex flex-col justify-between">
            <div>
              <h3 class="m-0 text-[0.7rem] p-1">{pages[$currentPage].title}</h3>
              <p class="m-0 text-[0.5rem] leading-snug text-left whitespace-pre-wrap overflow-wrap break-word hyphens-auto p-2">
                {pages[$currentPage].content}
              </p>
            </div>
    
            <!-- Button Container -->
            <div class="flex justify-between mt-auto">
              <button
                on:click={() => {
                  focusCamera(pages[$currentPage].coordinates)
                  wosh2.play();
                }}
                class="w-10 h-4 bg-white text-black border-none rounded-full cursor-pointer text-[0.35rem] font-bold"
              >
                Check out
              </button>
              <button
                on:click={() => {
                  clickSound.stop();
                  clickSound.play();
                  $currentPage = ($currentPage + 1) % pages.length
                }}
                class="w-10 h-4 bg-black text-white border-0 border-white rounded-full cursor-pointer text-[0.35rem] font-bold"
              >
                Next →
              </button>
            </div>
          </div>
        </div>
    
        <!-- Cover Layer -->
        {#if $showCover}
          <button
            on:click={() => {showCover.set(false); initfocusCamera();}}
            class="z-[9999999] absolute top-0 left-0 w-full h-full bg-cover bg-no-repeat bg-center rounded-lg flex justify-center items-center"
            style="background-image: url('Billboards/BillboardBackground.gif');"
          >
            <p class="text-white text-[0.8rem] text-center p-4 text-shadow">
              Click here for <br> Information
            </p>
          </button>
        {/if}
      </div>
    </HTML>
  {/if}
  
<!-- Billboard for Camera Coordinates 
<HTML position= {[0, 8, -2]} >
  <div style="
    position: fixed;
    top: 20px;
    right: 20px;
    width: 200px;
    background: rgba(0, 0, 0, 0.85);
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    padding: 1rem;
    border-radius: 8px;
    text-align: center;
    font-family: 'Courier New', monospace;
    color: #ffffff;
    font-size: 0.9rem;
    z-index: 1000;
    pointer-events: none;">
    <div style="margin-bottom: 0.5rem; font-weight: bold; font-size: 1.1rem;">
      Camera Position
    </div>
    <div style="margin-bottom: 0.3rem;">X: {x.toFixed(2)}</div>
    <div style="margin-bottom: 0.3rem;">Y: {y.toFixed(2)}</div>
    <div>Z: {z.toFixed(2)}</div>
  </div>
</HTML>

-->