"use strict";
console.log("Hello, World!");

const map = L.map("map").setView([51.505, -0.09], 13);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution:
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

L.marker([51.5, -0.09]).addTo(map).bindPopup("Somewhere on Earth").openPopup();

L.marker([19.2, 72.5]).addTo(map).bindPopup("Mumbai").openPopup();
