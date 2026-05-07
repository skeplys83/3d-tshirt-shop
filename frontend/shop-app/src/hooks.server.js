// src/hooks.server.js
import { redirect } from '@sveltejs/kit';

export async function handle({ event, resolve }) {
    const token = event.cookies.get('sessionid');

    if (token) {
        event.locals.userLoggedIn = true;
    } else {
        event.locals.userLoggedIn = false;
    }

    if (
        event.url.pathname.includes('/adminBoard') &&
        !event.locals.userLoggedIn
    ) {
        throw redirect(302, '/login');
    }

    return await resolve(event);
}
