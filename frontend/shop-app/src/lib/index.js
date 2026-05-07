import {addMessage, csrfToken, user} from "../stores/global_stores.js";
import {getUserInfo} from "../api/auth/auth.js";
import {get} from "svelte/store";
import {page} from "$app/stores";

export function getCsrfToken() {
    let cookieValue = null;

    if (document.cookie) {
        const cookie = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='));

        if (cookie) {
            cookieValue = cookie.split('=')[1];
        }
    }

    if (!cookieValue) {
        console.error('CSRF-Token not found');
        return null;
    }

    return cookieValue;
}

export function setCsrfToken(){
    const token = getCsrfToken();
    if (token) {
        csrfToken.set(token);
    } else {
        console.error('No CSRF token found.');
    }
}

export async function setUserInfo() {
    try {
        const userInfo = await getUserInfo();
        user.set({
            is_staff: userInfo.is_staff,
            is_active: userInfo.is_active,
            is_superuser: userInfo.is_superuser,
        });

        if (get(page).url.pathname.includes('adminBoard')) {
            if (!userInfo.is_active || !userInfo.is_staff) {
                addMessage({text: 'Not enough permission to access admin tools'});
                location.replace('/login');
            }
        }
    } catch (error) {
    }
}