async function pingServer() {

    if (api_key) {
        try {
            const response = await fetch('./api/ping', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    api_key: api_key,
                    action: 'keepalive'
                })
            });

            if (response.status === 401) {
                console.log('Session timeout.');
                location.reload(); // Reload page if session invalid
            } else if (!response.status === 200) {
                console.error('Unexpected status:', response.status);
            }
        } catch (error) {
            console.error('Error pinging server:', error);
        }
    }
}

setInterval(pingServer, 120000); // Ping server every 120 seconds

document.addEventListener('DOMContentLoaded', pingServer);
