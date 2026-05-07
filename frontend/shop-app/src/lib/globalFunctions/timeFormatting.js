export function formatDate(dateString) {
    const dateObj = new Date(dateString);
    const day = dateObj.getDate();
    const month = dateObj.toLocaleString('de-DE', { month: 'long' });
    const year = dateObj.getFullYear();
    return `${day}. ${month} ${year}`;
}

export function formatDateTime(dateTimeString) {
    const dateObj = new Date(dateTimeString);

    const day = dateObj.getDate();
    const month = dateObj.toLocaleString('de-DE', { month: 'long' });
    const year = dateObj.getFullYear();

    const hours = dateObj.getHours().toString().padStart(2, '0');
    const minutes = dateObj.getMinutes().toString().padStart(2, '0'); 

    return `${day}. ${month} ${year}, ${hours}:${minutes}`;
}