
window.SEASAT_CONFIG = {
  title: "SeaSat Ocean Demo",
  subtitle: "Fixed demo area • fixed date • toggleable layers",
  dateLabel: "Set this to your chosen date",
  aoiBounds: [[56.00, -6.00], [56.15, -5.75]],
  rgbOverlay: {
    enabled: false,
    imageUrl: "./layers/s2_rgb.png",
    bounds: [[56.00, -6.00], [56.15, -5.75]],
    opacity: 0.65
  },
  geojsonFiles: {
    sst: "./data/sst.geojson",
    sss: "./data/sss.geojson",
    chla: "./data/chla.geojson"
  }
};
