const map = L.map('map').setView([55.2, -5.25], 9);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '&copy; OpenStreetMap'
}).addTo(map);

const statusEl = document.getElementById('status');
const dateEl = document.getElementById('dateInput');
const runBtn = document.getElementById('runBtn');

const demoBox = [[55.0, -5.5], [55.4, -5.0]];
L.rectangle(demoBox, {weight: 2}).addTo(map);
map.fitBounds(demoBox);

const layers = {
  s2_rgb: L.layerGroup().addTo(map),
  sst: L.layerGroup(),
  sss: L.layerGroup(),
  chla: L.layerGroup(),
};

L.control.layers(null, {
  'Sentinel-2 RGB': layers.s2_rgb,
  'Predicted SST': layers.sst,
  'Predicted SSS': layers.sss,
  'Predicted Chl-a': layers.chla,
}).addTo(map);

async function loadConfig() {
  const res = await fetch('/api/demo-config');
  const cfg = await res.json();
  dateEl.value = cfg.default_date;
}

async function runDemo() {
  statusEl.textContent = 'Loading…';
  const payload = {
    date: dateEl.value,
    bbox: [-5.5, 55.0, -5.0, 55.4],
    mode: 'demo',
  };
  const res = await fetch('/api/predict', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload),
  });
  const data = await res.json();
  statusEl.textContent = data.message;
}

runBtn.addEventListener('click', runDemo);
loadConfig();
