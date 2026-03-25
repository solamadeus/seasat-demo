
# Sentinel-2 RGB overlay note

For tonight, the quickest approach is:
1. export a fixed RGB image for your AOI and chosen date
2. save it as `layers/s2_rgb.png`
3. set its bounds in `config.js`
4. turn `rgbOverlay.enabled` to `true`

You can do this from Earth Engine by exporting a thumbnail or a clipped image.
If that takes too long, skip the RGB overlay for tonight and just use the base map + prediction layers.
