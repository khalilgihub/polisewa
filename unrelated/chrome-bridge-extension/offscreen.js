// Antigravity Pro Offscreen Document
// Maintains persistent worker heartbeat and executes image stitching/cropping

// 1. Keep-Alive Heartbeat (fires every 20 seconds)
setInterval(() => {
  chrome.runtime.sendMessage({ type: "offscreen_heartbeat", timestamp: Date.now() }).catch(() => {});
}, 20000);

// 2. Canvas Image Processing Pipeline
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.target !== "offscreen") return;

  if (request.action === "cropImage") {
    handleCropImage(request.dataUrl, request.rect, request.dpr || 1)
      .then(resultUrl => sendResponse({ success: true, dataUrl: resultUrl }))
      .catch(err => sendResponse({ success: false, error: err.toString() }));
    return true; // async response
  }

  if (request.action === "stitchImages") {
    handleStitchImages(request.slices, request.totalWidth, request.totalHeight, request.dpr || 1)
      .then(resultUrl => sendResponse({ success: true, dataUrl: resultUrl }))
      .catch(err => sendResponse({ success: false, error: err.toString() }));
    return true; // async response
  }
});

function loadImage(src) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.crossOrigin = "anonymous";
    img.onload = () => resolve(img);
    img.onerror = (e) => reject(new Error("Failed to load image for canvas operation"));
    img.src = src;
  });
}

async function handleCropImage(dataUrl, rect, dpr) {
  const img = await loadImage(dataUrl);
  const canvas = document.getElementById("offscreenCanvas");
  const ctx = canvas.getContext("2d");

  const cropX = Math.max(0, Math.round(rect.x * dpr));
  const cropY = Math.max(0, Math.round(rect.y * dpr));
  const cropW = Math.round(rect.width * dpr);
  const cropH = Math.round(rect.height * dpr);

  canvas.width = cropW;
  canvas.height = cropH;

  ctx.drawImage(img, cropX, cropY, cropW, cropH, 0, 0, cropW, cropH);
  return canvas.toDataURL("image/png");
}

async function handleStitchImages(slices, totalWidth, totalHeight, dpr) {
  const canvas = document.getElementById("offscreenCanvas");
  const ctx = canvas.getContext("2d");

  const canvasWidth = Math.round(totalWidth * dpr);
  const canvasHeight = Math.round(totalHeight * dpr);

  canvas.width = canvasWidth;
  canvas.height = canvasHeight;

  for (const slice of slices) {
    const img = await loadImage(slice.dataUrl);
    const destY = Math.round(slice.offsetY * dpr);
    ctx.drawImage(img, 0, destY);
  }

  return canvas.toDataURL("image/png");
}
