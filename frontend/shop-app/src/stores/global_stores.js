import {writable} from "svelte/store";

export const apiUrl = import.meta.env.VITE_API_URL;
export const csrfToken = writable('');
export const userId = writable(null);
export const messageStore = writable([]);

export const user = writable({
    is_staff: false,
    is_active: false,
    is_superuser: false,
});

export function addMessage(message) {
    messageStore.update(messages => {
        const newMessages = [...messages, message];

        if (newMessages.length > 3) {
            newMessages.shift();
        }

        setTimeout(() => {
            messageStore.update(currentMessages => currentMessages.filter(m => m !== message));
        }, 5000);

        return newMessages;
    });
}

export const showPreloader = writable(true); 