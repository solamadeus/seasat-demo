window.SEASAT_CONFIG = {
  title: "SeaSat Mexico Demo",
  subtitle: "Fixed demo area • 2019-06-11 • target overpass 16:20 UTC • toggleable layers",
  dateLabel: "2019-06-11 16:20 UTC (target overpass time)",
  aoiBounds: [[29.00, -80.50], [30.00, -79.50]],
  rgbOverlay: {
    enabled: false,
    imageUrl: "./layers/s2_rgb.png",
    bounds: [[29.00, -80.50], [30.00, -79.50]],
    opacity: 0.65
  },
  geojsonFiles: {
    sst: "./data/sst.geojson",
    sss: "./data/sss.geojson",
    chla: "./data/chla.geojson"
  }
};
