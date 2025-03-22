if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function (position) {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;
        console.log('Latitude: ' + lat + ', Longitude: ' + lon);
        getCityName(lat, lon);
    }, function (error) {
        console.log("Error getting location: " + error.message);
    });
} else {
    console.log("Geolocation is not supported by this browser.");
}




function getCityName(lat, lon) {
    const apiKey = '141710af2113bab9f55ef73e1bcd33d5'; 
    const url = `https://maps.googleapis.com/maps/api/geocode/json?latlng=${lat},${lon}&key=${apiKey}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.status === "OK") {
                const address = data.results[0].formatted_address;
                console.log('Current Location: ' + address); 
            } else {
                console.log('Geocoding failed: ' + data.status);
            }
        })
        .catch(error => console.log('Error:', error));
}
