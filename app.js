
const cfg = window.SEASAT_CONFIG;

document.getElementById('title').textContent = cfg.title;
document.getElementById('subtitle').textContent = cfg.subtitle;
document.getElementById('meta').innerHTML = `<strong>Date:</strong> ${cfg.dateLabel}`;

const map = L.map('map');
map.fitBounds(cfg.aoiBounds);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

let rgbLayer = null;
if (cfg.rgbOverlay.enabled) {
  rgbLayer = L.imageOverlay(cfg.rgbOverlay.imageUrl, cfg.rgbOverlay.bounds, { opacity: cfg.rgbOverlay.opacity });
  rgbLayer.addTo(map);
}

function getColour(v, minv, maxv) {
  if (v == null || Number.isNaN(v)) return '#777777';
  const t = (v - minv) / (maxv - minv || 1);
  if (t < 0.33) return '#2c7bb6';
  if (t < 0.66) return '#fdae61';
  return '#d7191c';
}

async function loadGeoJson(url, valueField, radius=5) {
  const r = await fetch(url);
  const gj = await r.json();
  const vals = gj.features
    .map(f => f.properties[valueField])
    .filter(v => typeof v === 'number' && Number.isFinite(v));
  const minv = Math.min(...vals);
  const maxv = Math.max(...vals);

  return L.geoJSON(gj, {
    pointToLayer: function(feature, latlng) {
      const v = feature.properties[valueField];
      return L.circleMarker(latlng, {
        radius: radius,
        fillColor: getColour(v, minv, maxv),
        color: '#111',
        weight: 0.3,
        opacity: 0.6,
        fillOpacity: 0.85
      });
    },
    onEachFeature: function(feature, layer) {
      const p = feature.properties;
      layer.bindPopup(
        `<strong>${valueField}</strong>: ${p[valueField]}<br>` +
        (p.date ? `<strong>Date</strong>: ${p.date}<br>` : '') +
        (p.model ? `<strong>Model</strong>: ${p.model}` : '')
      );
    }
  });
}

let sstLayer, sssLayer, chlaLayer;

Promise.all([
  loadGeoJson(cfg.geojsonFiles.sst, 'sst'),
  loadGeoJson(cfg.geojsonFiles.sss, 'sss'),
  loadGeoJson(cfg.geojsonFiles.chla, 'chla')
]).then(([sst, sss, chla]) => {
  sstLayer = sst.addTo(map);
  sssLayer = sss.addTo(map);
  chlaLayer = chla.addTo(map);

  document.getElementById('toggle-rgb').addEventListener('change', e => {
    if (!rgbLayer) return;
    if (e.target.checked) map.addLayer(rgbLayer); else map.removeLayer(rgbLayer);
  });
  document.getElementById('toggle-sst').addEventListener('change', e => {
    if (e.target.checked) map.addLayer(sstLayer); else map.removeLayer(sstLayer);
  });
  document.getElementById('toggle-sss').addEventListener('change', e => {
    if (e.target.checked) map.addLayer(sssLayer); else map.removeLayer(sssLayer);
  });
  document.getElementById('toggle-chla').addEventListener('change', e => {
    if (e.target.checked) map.addLayer(chlaLayer); else map.removeLayer(chlaLayer);
  });
}).catch(err => {
  console.error(err);
  document.getElementById('meta').innerHTML += '<br><span style="color:#b00">Layer load failed. Check your GeoJSON file names and paths.</span>';
});
