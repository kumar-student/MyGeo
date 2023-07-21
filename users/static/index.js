const osm = "http://www.openstreetmap.org/copyright";
const maxZoom = 19;
const copy = `&copy; <a href='${osm}'>OpenStreetMap</a>`;
const url = "https://tile.openstreetmap.org/{z}/{x}/{y}.png";
const layer = L.tileLayer(url, {attribution: copy});
const map = L.map("map", {layers: [layer]});
map.fitWorld();
const data = document.getElementById("locations-data");
let feature = L.geoJSON(JSON.parse(data.textContent))
    .bindPopup(function (layer){    // Add user details to the popup
        const first_name = layer.feature.properties.first_name
        const last_name = layer.feature.properties.last_name
        const address = layer.feature.properties.address
        const phone = layer.feature.properties.phone
        const popupContent = `
            <b>${first_name} ${last_name}</b><br>
            <span>${address}</span><br>
            <span>${phone}</span><br>
        `;
        return popupContent;
    })
    .addTo(map);
map.fitBounds(feature.getBounds());
