// Read-only MAIN-world lightweight reader for Fab model settings (Zero-Lag & Low-RAM).
(() => {
  'use strict';
  if (!location.pathname.startsWith('/dope/')) return;
  if (document.documentElement.dataset.wt3dReaderVersion === '3.9.54') return;
  document.documentElement.dataset.wt3dReaderVersion = '3.9.54';
  const OUTPUT = 'wt3d-render-reference-data';
  const REQUEST = 'wt3d-read-render-reference';
  let currentCameraView;
  let readingCamera = false;

  function dataCopy(value, seen = new WeakSet(), depth = 0) {
    if (value === null || ['string', 'number', 'boolean'].includes(typeof value)) return value;
    if (!value || typeof value !== 'object' || depth > 6 || seen.has(value)) return undefined;
    seen.add(value);
    if (Array.isArray(value)) return value.slice(0, 200).map(v => dataCopy(v, seen, depth + 1));
    const copy = {};
    for (const key of Object.keys(value)) {
      if (/token|cookie|password|authorization|secret/i.test(key)) continue;
      const v = dataCopy(value[key], seen, depth + 1);
      if (v !== undefined) copy[key] = v;
    }
    return copy;
  }

  function capture() {
    const report = {
      schemaVersion: 1,
      capturedAt: new Date().toISOString(),
      source: 'Fab engine loaded reference; read-only',
      status: 'waiting'
    };
    const engine = window.__dope;
    if (engine) {
      report.sceneUid = engine.args?.sceneUid || null;
      report.currentCameraView = currentCameraView;
      if (!readingCamera && currentCameraView === undefined && typeof engine.getCameraView === 'function') {
        readingCamera = true;
        Promise.resolve(engine.getCameraView()).then(view => {
          currentCameraView = dataCopy(view);
          readingCamera = false;
        }, error => {
          currentCameraView = { error: String(error?.message || error) };
          readingCamera = false;
        });
      }
      const source = engine.preloadedFetches?.doptions;
      if (source && typeof source === 'object') {
        report.doptions = {
          materials: dataCopy(source.materials || {}),
          materialgroups: dataCopy(source.materialgroups || {}),
          environment: dataCopy(source.environment || {}),
          background: dataCopy(source.background || {}),
          ground: dataCopy(source.ground || {}),
          camera: dataCopy(source.camera || {}),
          postprocess: dataCopy(source.postprocess || {}),
          lights: dataCopy(source.lights || {})
        };
        report.status = 'ready';
      } else {
        report.status = 'engine-present-no-doptions';
      }
    } else {
      report.status = 'engine-unavailable';
    }
    let output = document.getElementById(OUTPUT);
    if (!output) {
      output = document.createElement('script');
      output.id = OUTPUT;
      output.type = 'application/json';
      document.documentElement.appendChild(output);
    }
    output.textContent = JSON.stringify(report);
    document.dispatchEvent(new Event('wt3d-render-reference-ready'));
    return report.status === 'ready';
  }

  document.addEventListener(REQUEST, capture);
  let attempts = 0;
  const poll = setInterval(() => {
    if (capture() || ++attempts >= 8) clearInterval(poll);
  }, 1500);
  capture();
})();
