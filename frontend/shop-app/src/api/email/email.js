import axios from 'axios';
import { csrfToken, apiUrl } from "../../stores/global_stores.js";
import { get } from 'svelte/store';

export async function sendEmail(email, subject, message) {
    const token = get(csrfToken);

    if (!token) {
        console.error('CSRF-Token not found');
        return;
    }

    try {
        const response = await axios.post(`${apiUrl}/api/v1/email/send-email/`,
            {
                email: email,
                subject: subject,
                message: message
            },
            {
                withCredentials: true,
                headers: {
                    'X-CSRFToken': token,
                    'Content-Type': 'application/json'
                }
            });
        return response.data;
    } catch (error) {
        throw error.response ? error.response.data : new Error('Sending email failed');
    }
}
