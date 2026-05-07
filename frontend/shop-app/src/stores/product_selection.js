import { readable, writable } from "svelte/store"

export const cartItemCount = writable(0);

export function updateCartItemCount() {
    const cart = JSON.parse(localStorage.getItem("cart")) || [];
    cartItemCount.set(cart.length);
}

export const selectedProductID = writable(-1)

const xPosition = -4.8 //distance from wall
export const productSlotPositions = readable([
    [xPosition, 10.5, 2.7],
    [xPosition, 10.5, -0.45],
    [xPosition, 10.5, -3.7],
    [xPosition, 6.3, 2.7],
    [xPosition, 6.3, -0.45],
    [xPosition, 6.3, -3.7]
]);
export const selectedProductPosition = readable([0.5,5.0,-0.45])
export const selectedProductRotation = readable([0,Math.PI*0.75,0])

export const selectedProductRotationSpeed = readable(0.05)

export const triggerDeselect = writable(false);

//camera
export const cameraControls = writable(undefined)
export const initialCameraPosition = readable([-30,5,-2])

export const defaultTransitionTime = readable(0.2)