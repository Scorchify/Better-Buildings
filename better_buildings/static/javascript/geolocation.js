document.addEventListener("DOMContentLoaded", function() {
    function sendGeolocation(latitude, longitude) {
        const originalFetch = window.fetch;
        window.fetch = function(url, options) {
            const urlObj = new URL(url, window.location.origin);
            urlObj.searchParams.append('latitude', latitude);
            urlObj.searchParams.append('longitude', longitude);
            return originalFetch(urlObj.toString(), options);
        };
    }

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            sendGeolocation(latitude, longitude);
        }, function(error) {
            // If geolocation fails use IP geolocation
            fetch('https://ipinfo.io/json?token=YOUR_TOKEN_HERE')
                .then(response => response.json())
                .then(data => {
                    const [latitude, longitude] = data.loc.split(',');
                    sendGeolocation(latitude, longitude);
                })
                .catch(() => console.log("IP Geolocation failed."));
        });
    } else {
        // If geolocation is not supported, use IP geolocation
        fetch('https://ipinfo.io/json?token=YOUR_TOKEN_HERE')
            .then(response => response.json())
            .then(data => {
                const [latitude, longitude] = data.loc.split(',');
                sendGeolocation(latitude, longitude);
            })
            .catch(() => console.log("IP Geolocation failed."));
    }
});