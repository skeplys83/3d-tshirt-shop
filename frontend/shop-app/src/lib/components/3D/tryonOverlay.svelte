<script lang="ts">
  import { onMount } from "svelte";
  import { HTML, Billboard } from '@threlte/extras';
  import * as posenet from "@tensorflow-models/posenet";
  import "@tensorflow/tfjs-backend-webgl";
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();

  const closeOverlay = () => {
    dispatch('close');
  };

  let isVisible = true;
  export let productId: number;

  // Component props
  export let position = [0, 0, 0];
  export let rotation = [0, 0, 0];

  // Shirt configuration to adjust the size and position
  export let shirtConfig = {
    scale: 1.5,
    offsetX: 0,
    offsetY: 32,
    width: 290,
    height: 300
  };

  // References
  let videoRef: HTMLVideoElement | null = null;
  let canvasRef: HTMLCanvasElement | null = null;
  let net: posenet.PoseNet | null = null;
  let intervalId: number | null = null;

  // // Map product IDs to shirt paths hardcoded
  // const SHIRT_PATHS = {
  //   1: "/shirts/1.png",
  //   2: "/shirts/2.png",
  //   3: "/shirts/3.png",
  //   4: "/shirts/4.png"
  // };

  function getShirtPath(productId: number): string {
  return `/shirts/${productId}.png`; // Dynamically create path
}

  let shirtImage: HTMLImageElement | null = null;

  const VIDEO_CONFIG = {
    width: 640,
    height: 480,
  };

  async function loadShirtImage(path: string) {
    return new Promise<HTMLImageElement>((resolve, reject) => {
      const img = new Image();
      img.onload = () => resolve(img);
      img.onerror = reject;
      img.src = path;
    });
  }

  async function initialize(productId: number) {
    if (!videoRef) return;

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: VIDEO_CONFIG });
      videoRef.srcObject = stream;
      await videoRef.play();

      // Load shirt based on product ID
      const shirtPath = getShirtPath(productId);
      shirtImage = await loadShirtImage(shirtPath);

      // Initialize PoseNet
      net = await posenet.load({
        architecture: "MobileNetV1",
        outputStride: 16,
        inputResolution: { width: VIDEO_CONFIG.width, height: VIDEO_CONFIG.height },
        multiplier: 0.75,
      });

      intervalId = window.setInterval(() => {
        if (net) detect(net);
      }, 100);
    } catch (err) {
      console.error("Error initializing:", err);
    }
  }

  async function detect(net: posenet.PoseNet) {
    if (videoRef && canvasRef && videoRef.readyState === 4) {
      const video = videoRef;
      const videoWidth = video.videoWidth;
      const videoHeight = video.videoHeight;

      video.width = videoWidth;
      video.height = videoHeight;

      const pose = await net.estimateSinglePose(video, { flipHorizontal: false });
      drawCanvas(pose, video, videoWidth, videoHeight, canvasRef);
    }
  }

  function drawCanvas(pose: posenet.Pose, video: HTMLVideoElement, videoWidth: number, videoHeight: number, canvas: HTMLCanvasElement) {
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    canvas.width = videoWidth;
    canvas.height = videoHeight;

    ctx.clearRect(0, 0, videoWidth, videoHeight);
    ctx.drawImage(video, 0, 0, videoWidth, videoHeight);

    drawShirt(pose, ctx);
  }

  function drawShirt(pose: posenet.Pose, ctx: CanvasRenderingContext2D) {
    if (!shirtImage) return;

    const leftShoulder = pose.keypoints.find(kp => kp.part === "leftShoulder");
    const rightShoulder = pose.keypoints.find(kp => kp.part === "rightShoulder");

    if (leftShoulder && rightShoulder && leftShoulder.score > 0.5 && rightShoulder.score > 0.5) {
      const midX = (leftShoulder.position.x + rightShoulder.position.x) / 2;
      const midY = (leftShoulder.position.y + rightShoulder.position.y) / 2;

      const shoulderWidth = Math.sqrt(
        Math.pow(rightShoulder.position.x - leftShoulder.position.x, 2) +
        Math.pow(rightShoulder.position.y - leftShoulder.position.y, 2)
      );

      const finalWidth = shoulderWidth * shirtConfig.scale * 1.5;
      const finalHeight = (finalWidth * shirtConfig.height) / shirtConfig.width;

      ctx.save();
      ctx.translate(midX + shirtConfig.offsetX, midY + shirtConfig.offsetY);

      const angle = Math.atan2(
        rightShoulder.position.y - leftShoulder.position.y,
        rightShoulder.position.x - leftShoulder.position.x
      );
      ctx.rotate(angle);

      ctx.scale(1, -1);
      ctx.drawImage(
        shirtImage,
        -finalWidth / 2,
        -finalHeight / 4,
        finalWidth,
        finalHeight
      );

      ctx.restore();
    }
  }

  onMount(() => {
    initialize(productId);
    return cleanup;
  });

  function cleanup() {
    if (intervalId) clearInterval(intervalId);
    if (videoRef?.srcObject) {
      const tracks = (videoRef.srcObject as MediaStream).getTracks();
      tracks.forEach((track) => track.stop());
    }
    isVisible = false;
  }
</script>

<Billboard>
  <HTML position={position} rotation={rotation} center>
    <div class="w-80 h-96 border-8 border-white relative overflow-hidden">
      <video
        autoplay
        playsinline
        bind:this={videoRef}
        class="hidden"
      >
        <track kind="captions" />
      </video>
      <canvas
        bind:this={canvasRef}
        class="absolute top-0 left-0 w-full h-full object-cover"
      ></canvas>
    </div>

    <div class="w-80 bg-white flex flex-col p-4 pt-0">
      <div class="pb-2">
        <p class="text-4xl font-semibold">Virtual Try-On</p>
        <p>Explore how your product fits you in the virtual world. Please move back if you can't see the virtual product.</p>
      </div>
      <div class="mt-4 flex flex-col items-center">
        <button
          class=" border-2 border-black bg-red-600 text-white rounded-full h-14 text-xl w-1/2 hover:bg-red-800"
          on:click={closeOverlay}
        >
          Close
        </button>
      </div>
    </div>
  </HTML>
</Billboard>


