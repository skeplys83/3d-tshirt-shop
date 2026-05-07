import { csrfToken, apiUrl } from "../../stores/global_stores.js";
import { get } from 'svelte/store';
import axios from 'axios';

export const createCheckoutSession = async (order) => {
    try {
        const response = await axios.post(`${apiUrl}/api/v1/payments/create-checkout-session/`,
            {
                order: order
            },
            {
                withCredentials: true,
            });

        if (response.data.url) {
            console.log('Checkout session created:', response.data.url);

            window.location.href = response.data.url;
        } else {
            console.error('No checkout session URL received');
        }
    } catch (error) {
        throw error.response ? error.response.data : new Error('Checkout failed');
    }
};

