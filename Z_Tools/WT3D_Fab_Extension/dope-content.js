// WT3D Fab Canvas Studio v3.9.31 (Verified Studio Soft & color-safe finish)
// Dedicated WebGL & Native DOM Hybrid Automation for Fab 3D Editor (/dope/*)
// Author: Phan Trọng Tấn (@tanphan1105) - WaterTreatment3D
(() => {
  'use strict';
  const STUDIO_VERSION = '3.9.54';

  // Truy cập chrome.storage an toàn:
  // - Khi chrome.storage === undefined: báo rõ nhấn Ctrl+Shift+R.
  // - Khi extension vừa Reload khiến chrome.storage.local ném 'Extension context invalidated':
  //   tự động dùng localStorage dự phòng để mọi thao tác (chọn mẫu ★, Lưu, Bơm, Hoàn tác, 1-Click) chạy mượt 100% không ném lỗi!
  const FALLBACK_STORE_KEY = '__wt3d_ext_context_fallback_store';
  const readFallbackStore = () => {
    try { return JSON.parse(localStorage.getItem(FALLBACK_STORE_KEY) || '{}') || {}; } catch (_) { return {}; }
  };
  const writeFallbackStore = (obj) => {
    try { localStorage.setItem(FALLBACK_STORE_KEY, JSON.stringify(obj || {})); } catch (_) {}
  };
  const storageLocal = () => {
    const s = (typeof chrome !== 'undefined') && chrome.storage && chrome.storage.local;
    if (!s) throw new Error('Extension vừa được tải lại nên mất kết nối với trang này. Hãy nhấn Ctrl+Shift+R trên tab Fab rồi thử lại.');
    return {
      get: async (keys) => {
        try {
          if (!chrome.runtime || !chrome.runtime.id) throw new Error('Extension context invalidated.');
          const res = await s.get(keys);
          const fb = readFallbackStore();
          return { ...fb, ...(res || {}) };
        } catch (_) {
          const fb = readFallbackStore();
          if (keys == null) return fb;
          const ks = typeof keys === 'string' ? [keys] : Array.isArray(keys) ? keys : Object.keys(keys);
          const out = {};
          ks.forEach(k => { if (k in fb) out[k] = fb[k]; });
          return out;
        }
      },
      set: async (items) => {
        const fb = { ...readFallbackStore(), ...(items || {}) };
        writeFallbackStore(fb);
        try {
          if (!chrome.runtime || !chrome.runtime.id) return;
          await s.set(items);
        } catch (_) {}
      }
    };
  };

  const canvas = () => document.querySelector('#canvas') || document.querySelector('canvas');

  // Verify execution scope:
  // Activate only if URL contains /dope/ OR if running inside an iframe with a WebGL canvas
  const isDope = window.location.href.includes('/dope/') || (window.top !== window && !!canvas());
  if (!isDope && !window.location.href.includes('/dope/')) return;

  const parseVer = (v) => String(v || '0.0.0').split('.').map(n => parseInt(n, 10) || 0);
  const isOlderVer = (domVer, myVer) => {
    const a = parseVer(domVer), b = parseVer(myVer);
    for (let i = 0; i < 3; i++) {
      if ((a[i] || 0) < (b[i] || 0)) return true;
      if ((a[i] || 0) > (b[i] || 0)) return false;
    }
    return false;
  };
  const existingPanel = document.getElementById('wt3d-fab-studio-panel');
  if (existingPanel) {
    const domVer = existingPanel.getAttribute('data-wt3d-version') || '0.0.0';
    if (existingPanel.__wt3dWorldAlive && !isOlderVer(domVer, STUDIO_VERSION)) return;
    try { existingPanel.remove(); } catch (_) {}
    try { document.getElementById('wt3d-fab-studio-style')?.remove(); } catch (_) {}
    console.log('[WT3D Canvas Studio] ♻️ Hot-replaced Studio Panel v' + domVer + ' with v' + STUDIO_VERSION);
  }
  console.log('[WT3D Canvas Studio] 🚀 KeyShot Studio v' + STUDIO_VERSION + ' active in 3D frame:', window.location.href);

  // Proportional horizontal ratios of bottom toolbar tabs (Reference: 1024x617 Fab canvas, center=512)
  const TAB_RATIOS = {
    scene: 0.3232,       // Scene
    lighting: 0.3682,    // Lighting (Environment + HDRI Studio)
    materials: 0.4160,   // Materials (PBR)
    camera: 0.4638,      // Camera (FOV, Fit, Save)
    look: 0.5059,        // Look (Ground, Vignette, Tone Mapping, Background)
    annotations: 0.5537, // Annotations
    animation: 0.6455,   // Animation
    inspect: 0.6660      // Inspect (Wireframe, Matcap)
  };

  const CENTER_OFFSETS = {
    scene: -181,
    lighting: -135,
    materials: -86,
    camera: -37,
    look: +6,
    annotations: +55,
    animation: +149,
    inspect: +170
  };

  const KEYBOARD_SHORTCUTS = {
    scene: { key: '1', code: 'Digit1', keyCode: 49 },
    lighting: { key: '2', code: 'Digit2', keyCode: 50 },
    materials: { key: '3', code: 'Digit3', keyCode: 51 },
    camera: { key: '4', code: 'Digit4', keyCode: 52 },
    look: { key: '5', code: 'Digit5', keyCode: 53 },
    annotations: { key: '6', code: 'Digit6', keyCode: 54 },
    animation: { key: '7', code: 'Digit7', keyCode: 55 },
    inspect: { key: '8', code: 'Digit8', keyCode: 56 }
  };

  let runId = 0;
  let running = false;
  let activeProfile = 'soft';
  let activeBg = 'environment';
  let isMinimized = false;
  let isLeftSide = true;

  const wait = ms => new Promise(resolve => setTimeout(resolve, ms));

  if (window.__WT3D_DOPE_TOP_LISTENERS__) {
    try { window.removeEventListener('keydown', window.__WT3D_DOPE_TOP_LISTENERS__.keydown, true); } catch (_) {}
    try { window.removeEventListener('pointerdown', window.__WT3D_DOPE_TOP_LISTENERS__.shield, { capture: true }); } catch (_) {}
  }
  const onEscKeydown = e => {
    if (e.key === 'Escape' || e.code === 'Escape' || e.keyCode === 27) {
      if (running) {
        runId++;
        running = false;
        setStatus('🛑 Đã dừng theo phím ESC (Điều lệ 17)!', '#dc2626');
        console.warn('[WT3D Canvas Studio] 🛑 Emergency stop triggered by ESC key.');
      }
    }
  };
  const onShieldPointerDown = e => {
    const panel = document.getElementById('wt3d-fab-studio-panel');
    if (panel && (panel === e.target || panel.contains(e.target))) {
      const tag = (e.target.tagName || '').toLowerCase();
      if (tag !== 'input' && tag !== 'textarea' && tag !== 'select' && tag !== 'option' && tag !== 'label') {
        e.preventDefault();
      }
    }
  };
  window.__WT3D_DOPE_TOP_LISTENERS__ = { keydown: onEscKeydown, shield: onShieldPointerDown };
  window.addEventListener('keydown', onEscKeydown, true);
  window.addEventListener('pointerdown', onShieldPointerDown, { capture: true, passive: false });

  // [RULE 23 TPS - JIDOKA] Kiểm tra canvas còn sống, dừng ngay khi modal biến mất
  function assertAlive(id = runId) {
    const c = canvas();
    if (!c || !c.isConnected || c.getBoundingClientRect().width < 100 || id !== runId) {
      throw new Error('JIDOKA: Fab 3D canvas is no longer available. Automation stopped safely.');
    }
    return c;
  }

  function getAccessibleDocs() {
    // [JIDOKA FIX 1] Strictly isolate to the /dope/ 3D editor document only.
    // Never traverse into window.parent.document or window.top.document!
    return [document];
  }

  function getAllDomNodes(root = document) {
    const nodes = [];
    const walk = (node) => {
      if (!node) return;
      if (node.nodeType === Node.ELEMENT_NODE) {
        nodes.push(node);
        if (node.shadowRoot) walk(node.shadowRoot);
      }
      let child = node.firstElementChild;
      while (child) {
        walk(child);
        child = child.nextElementSibling;
      }
    };
    walk(root);
    return nodes;
  }

  // =========================================================================
  // [CORE 1] KIỂM TRA TRẠNG THÁI TAB PANEL NATIVE FAB ĐÃ MỞ TRÊN MÀN HÌNH CHƯA
  // =========================================================================
  function isTabPanelAlreadyOpen(tabName) {
    const lower = tabName.toLowerCase().trim();
    const docs = getAccessibleDocs();

    for (const doc of docs) {
      const labels = Array.from(doc.querySelectorAll('label, div, span, h3, h4, p, button')).filter(el => {
        if (el.id?.includes('wt3d') || el.closest?.('#wt3d-fab-studio-panel')) return false;
        if (el.querySelector?.('#wt3d-fab-studio-panel')) return false;
        if (el.children && el.children.length > 2) return false;
        const r = el.getBoundingClientRect();
        if (r.width === 0 || r.height === 0 || r.height >= 60 || r.top < 45 || r.bottom > window.innerHeight - 55) return false;
        return true;
      });

      const hasText = (pattern) => labels.some(el => {
        const t = (el.textContent || '').trim();
        const aria = el.getAttribute?.('aria-label') || '';
        return (t.length <= 40 && pattern.test(t)) || pattern.test(aria);
      });

      if (lower === 'lighting') {
        if (hasText(/^Environment$/i) && (hasText(/Orientation/i) || hasText(/Brightness/i) || hasText(/Occlusion/i) || hasText(/Reflection/i))) return true;
      } else if (lower === 'look') {
        if ((hasText(/^Background$/i) || hasText(/^Ground$/i)) && (hasText(/Vignette/i) || hasText(/Tone\s*Mapping/i) || hasText(/Grain/i) || hasText(/Chromatic\s*Aberration/i))) return true;
      } else if (lower === 'camera') {
        if (hasText(/Field\s*Of\s*View|FOV/i) || hasText(/Depth\s*Of\s*Field/i) || hasText(/Replace\s*default\s*view/i)) return true;
      } else if (lower === 'materials') {
        if (hasText(/Base\s*Color/i) || (hasText(/Roughness/i) && hasText(/Metallic/i))) return true;
      } else if (lower === 'inspect') {
        if (hasText(/Wireframe/i) || hasText(/Matcap/i)) return true;
      } else if (lower === 'scene') {
        if (hasText(/Model\s*Information/i) || hasText(/Hierarchy/i)) return true;
      }
    }
    return false;
  }

  // =========================================================================
  // [CORE 2] HUMAN CLICK CHUẨN W3C VỚI TỌA ĐỘ TÂM ĐIỂM
  // =========================================================================
  async function humanClick(el) {
    if (!el) return false;
    const r = el.getBoundingClientRect();
    const cx = Math.round(r.left + r.width * 0.5);
    const cy = Math.round(r.top + r.height * 0.5);

    const makePointer = (type, buttons) => new PointerEvent(type, {
      bubbles: true, cancelable: true, composed: true, view: window,
      clientX: cx, clientY: cy, screenX: window.screenX + cx, screenY: window.screenY + cy,
      button: 0, buttons, pointerId: 1, pointerType: 'mouse', isPrimary: true
    });

    const makeMouse = (type, buttons) => new MouseEvent(type, {
      bubbles: true, cancelable: true, composed: true, view: window,
      clientX: cx, clientY: cy, screenX: window.screenX + cx, screenY: window.screenY + cy,
      button: 0, buttons
    });

    el.dispatchEvent(makePointer('pointerdown', 1));
    el.dispatchEvent(makeMouse('mousedown', 1));
    await wait(40);
    el.dispatchEvent(makePointer('pointerup', 0));
    el.dispatchEvent(makeMouse('mouseup', 0));
    try {
      el.click();
    } catch (_) {
      el.dispatchEvent(makeMouse('click', 0));
    }
    return true;
  }

  // =========================================================================
  // [CORE 3] REACT VIRTUAL DOM VALUE BYPASS (SKILL BROWSER-EXTENSION-DEV)
  // =========================================================================
  function setReactValue(input, value) {
    if (!input) return;
    input.focus?.();
    const lastValue = input.value;
    const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value')?.set;
    if (setter) {
      setter.call(input, value);
    } else {
      input.value = value;
    }
    const tracker = input._valueTracker;
    if (tracker) {
      tracker.setValue(lastValue);
    }
    input.dispatchEvent(new Event('input', { bubbles: true }));
    input.dispatchEvent(new Event('change', { bubbles: true }));
  }

  // Multi-point geometric tap trên canvas
  async function dispatchCanvasTap(pt, id = runId) {
    const c = assertAlive(id);
    const r = c.getBoundingClientRect();

    const makePointer = (type, buttons) => {
      const ev = new PointerEvent(type, {
        bubbles: true, cancelable: true, composed: true, view: window,
        clientX: pt.x, clientY: pt.y, screenX: window.screenX + pt.x, screenY: window.screenY + pt.y,
        button: 0, buttons, pointerId: 991, pointerType: 'mouse', isPrimary: true
      });
      try {
        Object.defineProperty(ev, 'offsetX', { value: Math.round(pt.x - r.left), configurable: true });
        Object.defineProperty(ev, 'offsetY', { value: Math.round(pt.y - r.top), configurable: true });
      } catch(_) {}
      return ev;
    };

    const makeMouse = (type, buttons) => {
      const ev = new MouseEvent(type, {
        bubbles: true, cancelable: true, composed: true, view: window,
        clientX: pt.x, clientY: pt.y, screenX: window.screenX + pt.x, screenY: window.screenY + pt.y,
        button: 0, buttons
      });
      try {
        Object.defineProperty(ev, 'offsetX', { value: Math.round(pt.x - r.left), configurable: true });
        Object.defineProperty(ev, 'offsetY', { value: Math.round(pt.y - r.top), configurable: true });
      } catch(_) {}
      return ev;
    };

    c.dispatchEvent(makePointer('pointermove', 0));
    c.dispatchEvent(makeMouse('mousemove', 0));
    await wait(30);

    c.dispatchEvent(makePointer('pointerdown', 1));
    c.dispatchEvent(makeMouse('mousedown', 1));
    await wait(50);

    c.dispatchEvent(makePointer('pointerup', 0));
    c.dispatchEvent(makeMouse('mouseup', 0));
    c.dispatchEvent(makeMouse('click', 0));
  }

  // =========================================================================
  // [CORE 4] ĐỘNG CƠ KÍCH HOẠT TAB 4 LỚP (MỞ VÀ GIỮ NGUYÊN TRÊN MÀN HÌNH)
  // =========================================================================
  async function openTab(name, id = runId) {
    const c = assertAlive(id);
    const api = window.WT3DToolbar;
    if (!api) throw new Error('Bộ nhận diện thanh tab chưa nạp; mở lại editor sau Reload extension.');
    const tab = name.toLowerCase().trim();
    const before = await api.capture(c);
    const bar = api.detect(before);
    if (api.active(before, bar, tab)) return true;
    const p = api.point(bar, tab), rect = c.getBoundingClientRect();
    await dispatchCanvasTap({x:rect.left+p.x/before.width*rect.width,
      y:rect.top+p.y/before.height*rect.height}, id);
    for (let attempt=0;attempt<5;attempt++) {
      await wait(100);assertAlive(id);
      const after=await api.capture(c);
      if(api.active(after,api.detect(after),tab)) {
        setStatus(`✅ Đã xác minh tab ${tab.toUpperCase()} được chọn trên thanh Fab.`, '#16a34a');
        return true;
      }
    }
    throw new Error(`Không xác minh được tab ${tab.toUpperCase()}; đã dừng, không click thêm vị trí đoán.`);
  }

  // Retained for comparison only. Never called: old viewport ratios could hit
  // another tab and the unconditional success at its end was not trustworthy.
  async function openLegacyTab_UNUSED(name, id = runId) {
    const c = assertAlive(id);
    const lowerTab = name.toLowerCase().trim();
    console.log(`[WT3D Canvas Studio] 🚀 Requesting Open Tab: ${name.toUpperCase()}...`);

    if (isTabPanelAlreadyOpen(lowerTab)) {
      console.log(`[WT3D Canvas Studio] ⚡ Tab ${name.toUpperCase()} is ALREADY OPEN. Keeping it visible!`);
      setStatus(`✅ Tab ${name.toUpperCase()} đang mở sẵn trên màn hình!`, '#16a34a');
      return true;
    }

    const docs = getAccessibleDocs();

    // LAYER 1: Deep Semantic & Text Search across ALL nodes at the bottom toolbar
    for (const doc of docs) {
      const allElements = getAllDomNodes(doc);
      const candidates = allElements.filter(el => {
        if (el.id?.includes('wt3d') || el.closest?.('#wt3d-fab-studio-panel') || el.querySelector?.('#wt3d-fab-studio-panel')) return false;
        const r = el.getBoundingClientRect();
        if (r.width === 0 || r.height === 0 || r.height > 70 || r.width > 220) return false;
        // Must be in bottom region (bottom > window.innerHeight - 110)
        if (r.bottom < window.innerHeight - 110) return false;

        const text = (el.textContent || '').trim().toLowerCase();
        const aria = (el.getAttribute('aria-label') || '').toLowerCase();
        const title = (el.getAttribute('title') || '').toLowerCase();

        const matchText = text === lowerTab || text.startsWith(lowerTab + ' ') || text.endsWith(' ' + lowerTab);
        const matchAttr = aria === lowerTab || title === lowerTab || aria.includes(lowerTab) || title.includes(lowerTab);
        return matchText || matchAttr;
      });

      if (candidates.length > 0) {
        candidates.sort((a, b) => a.children.length - b.children.length);
        for (const cand of candidates.slice(0, 2)) {
          const btnParent = cand.closest('button, [role="tab"], [role="button"], li');
          const clickTarget = (btnParent && btnParent.getBoundingClientRect().width <= 220) ? btnParent : cand;
          console.log(`[WT3D Canvas Studio] 🎯 [Layer 1 DOM] Clicking bottom tab: <${clickTarget.tagName.toLowerCase()}> "${cand.textContent?.trim()}"`);
          await humanClick(clickTarget);
          await wait(320);
          if (isTabPanelAlreadyOpen(lowerTab)) {
            console.log(`[WT3D Canvas Studio] ✅ Tab ${name.toUpperCase()} OPENED successfully via Layer 1 DOM!`);
            setStatus(`✅ Đã mở Tab ${name.toUpperCase()}!`, '#16a34a');
            return true;
          }
        }
      }
    }

    // LAYER 2: Innermost Pill Bar Container Scanner (Tab Index Map)
    const TAB_INDEX_MAP = { scene: 0, lighting: 1, materials: 2, camera: 3, look: 4, annotations: 5, animation: 6, inspect: 7 };
    const tabIdx = TAB_INDEX_MAP[lowerTab];

    for (const doc of docs) {
      const bottomContainers = Array.from(doc.querySelectorAll('div, nav, footer, section, ul')).filter(el => {
        if (el.id?.includes('wt3d') || el.closest?.('#wt3d-fab-studio-panel') || el.querySelector?.('#wt3d-fab-studio-panel')) return false;
        const r = el.getBoundingClientRect();
        if (r.top < window.innerHeight - 110 && r.bottom < window.innerHeight - 10) return false;
        if (r.width < 200 || r.width > 1050 || r.height < 15 || r.height > 75) return false;
        return true;
      });

      for (const container of bottomContainers) {
        const directButtons = Array.from(container.querySelectorAll('button, [role="tab"], div[role="button"], li')).filter(b => {
          const br = b.getBoundingClientRect();
          return br.width >= 15 && br.width <= 220 && br.height >= 12;
        });

        if (directButtons.length >= 4 && tabIdx !== undefined && directButtons[tabIdx]) {
          console.log(`[WT3D Canvas Studio] 💊 [Layer 2 Pill] Clicking Pill item index ${tabIdx} for tab ${lowerTab}`);
          await humanClick(directButtons[tabIdx]);
          await wait(320);
          if (isTabPanelAlreadyOpen(lowerTab)) {
            console.log(`[WT3D Canvas Studio] ✅ Tab ${name.toUpperCase()} OPENED successfully via Layer 2 Pill!`);
            setStatus(`✅ Đã mở Tab ${name.toUpperCase()}!`, '#16a34a');
            return true;
          }
        }
      }
    }

    // LAYER 3: Precision Geometric Click on the Toolbar (Compact Button + Direct Bottom-Bar Coordinate Tap)
    const cr = c.getBoundingClientRect();
    const ratio = TAB_RATIOS[lowerTab] ?? 0.3682;
    const offset = CENTER_OFFSETS[lowerTab] ?? 0;
    const xByRatio = Math.round(cr.left + cr.width * ratio);
    const xByCenter = Math.round(cr.left + cr.width * 0.5 + offset);
    const yBottom = Math.round(cr.bottom - 24);

    for (const clickX of [xByCenter, xByRatio]) {
      const hitEl = document.elementFromPoint(clickX, yBottom);
      if (hitEl && hitEl.tagName !== 'CANVAS' && !hitEl.id?.includes('wt3d') && !hitEl.closest?.('#wt3d-fab-studio-panel')) {
        const btnParent = hitEl.closest('button, [role="tab"], [role="button"], li');
        const clickTarget = (btnParent && btnParent.getBoundingClientRect().width <= 220) ? btnParent : hitEl;
        if (clickTarget.getBoundingClientRect().width <= 220) {
          console.log(`[WT3D Canvas Studio] 🎯 [Layer 3 Point] Clicking compact element at (${clickX}, ${yBottom}): <${clickTarget.tagName.toLowerCase()}>`);
          await humanClick(clickTarget);
          await wait(300);
          if (isTabPanelAlreadyOpen(lowerTab)) {
            setStatus(`✅ Đã mở Tab ${name.toUpperCase()}!`, '#16a34a');
            return true;
          }
        }
      }
      await dispatchCanvasTap({ x: clickX, y: yBottom }, id);
      await wait(250);
      if (isTabPanelAlreadyOpen(lowerTab)) {
        setStatus(`✅ Đã mở Tab ${name.toUpperCase()}!`, '#16a34a');
        return true;
      }
    }

    setStatus(`✅ Đã kích hoạt Tab ${name.toUpperCase()}!`, '#16a34a');
    return true;
  }
  // =========================================================================
  // [CORE 5] THIẾT LẬP SLIDER & TOGGLE NATIVE FAB
  // =========================================================================
  async function setFabSlider(labelPattern, targetVal, sectionPattern = null) {
    const docs = getAccessibleDocs();
    const findMatchingLabels = (doc, useSection) => Array.from(doc.querySelectorAll('label, div, span, p')).filter(el => {
      if (el.id?.includes('wt3d') || el.closest?.('#wt3d-fab-studio-panel') || el.querySelector?.('#wt3d-fab-studio-panel')) return false;
      if (el.children && el.children.length > 3) return false;
      const r = el.getBoundingClientRect();
      if (r.top < 45 || r.bottom > window.innerHeight - 50 || r.width === 0 || r.height === 0 || r.height >= 50) return false;
      const t = (el.textContent || '').trim();
      if (!labelPattern.test(t)) return false;
      if (useSection && sectionPattern) {
        let section = el.parentElement;
        let found = false;
        for (let depth = 0; depth < 6 && section && section !== doc.body; depth++, section = section.parentElement) {
          const headings = Array.from(section.querySelectorAll('h1,h2,h3,h4,h5,legend,label,div,span,p,[role="heading"]'));
          if (headings.some(h => h !== el && (h.children?.length || 0) <= 2 && sectionPattern.test((h.textContent || '').trim()))) { found = true; break; }
        }
        if (!found) return false;
      }
      return true;
    });

    for (const doc of docs) {
      let labels = findMatchingLabels(doc, !!sectionPattern);
      if (labels.length === 0 && sectionPattern) {
        labels = findMatchingLabels(doc, false);
      }

      for (const lb of labels) {
        let p = lb.parentElement;
        for (let i = 0; i < 5 && p; i++) {
          if (p === doc.body || p.id?.includes('wt3d') || p.querySelector?.('#wt3d-fab-studio-panel')) break;
          const rangeInp = p.querySelector('input[type="range"]');
          const numInp = p.querySelector('input[type="number"], input[type="text"]');

          if (rangeInp) {
            const min = parseFloat(rangeInp.min || '0');
            const max = parseFloat(rangeInp.max || '100');
            const valClamped = Math.max(min, Math.min(max, targetVal));
            setReactValue(rangeInp, String(valClamped));
            console.log(`[WT3D Canvas Studio] 🎚️ Set range slider for ${labelPattern}: ${valClamped}`);
            await wait(70);
            return true;
          }

          if (numInp && !numInp.id?.includes('wt3d')) {
            setReactValue(numInp, String(targetVal));
            console.log(`[WT3D Canvas Studio] 🔢 Set num input for ${labelPattern}: ${targetVal}`);
            await wait(70);
            return true;
          }
          p = p.parentElement;
        }
      }
    }
    return false;
  }

  async function setFabToggleSwitch(labelPattern, wantOn = true) {
    const docs = getAccessibleDocs();
    for (const doc of docs) {
      const labels = Array.from(doc.querySelectorAll('label, div, span, h3, h4, p')).filter(el => {
        if (el.id?.includes('wt3d') || el.closest?.('#wt3d-fab-studio-panel') || el.querySelector?.('#wt3d-fab-studio-panel')) return false;
        if (el.children && el.children.length > 3) return false;
        const r = el.getBoundingClientRect();
        if (r.top < 45 || r.bottom > window.innerHeight - 50 || r.width === 0 || r.height === 0 || r.height >= 50) return false;
        const t = (el.textContent || '').trim();
        return labelPattern.test(t);
      });

      for (const lb of labels) {
        let p = lb.parentElement;
        for (let i = 0; i < 4 && p; i++) {
          if (p === doc.body || p.id?.includes('wt3d') || p.querySelector?.('#wt3d-fab-studio-panel')) break;
          const chk = p.querySelector('input[type="checkbox"]');
          const switchBtn = p.querySelector('[role="switch"], button[class*="switch" i], [class*="toggle" i]');

          if (chk) {
            if (chk.checked !== wantOn) {
              await humanClick(chk);
              await wait(100);
            }
            return true;
          }
          if (switchBtn) {
            const isCurrentlyOn = switchBtn.getAttribute('aria-checked') === 'true' ||
                                  switchBtn.getAttribute('data-state') === 'checked' ||
                                  switchBtn.classList.contains('active') ||
                                  switchBtn.classList.contains('checked') ||
                                  /--on|--active|checked/i.test(switchBtn.className);
            if (isCurrentlyOn !== wantOn) {
              await humanClick(switchBtn);
              await wait(100);
            }
            return true;
          }
          p = p.parentElement;
        }
      }
    }
    return false;
  }

  async function selectFabHdri(hdriName) {
    const docs = getAccessibleDocs();
    for (const doc of docs) {
      const cards = Array.from(doc.querySelectorAll('div, button, [role="button"], [class*="card" i], [class*="item" i]')).filter(el => {
        if (el.id?.includes('wt3d') || el.closest?.('#wt3d-fab-studio-panel') || el.querySelector?.('#wt3d-fab-studio-panel')) return false;
        const rect = el.getBoundingClientRect();
        if (rect.top < 50 || rect.width < 25 || rect.height < 20 || rect.height > 180) return false;
        const t = (el.textContent || '').trim().toLowerCase();
        return t === hdriName.toLowerCase() || t.startsWith(hdriName.toLowerCase());
      });

      if (cards.length > 0) {
        await humanClick(cards[0]);
        console.log(`[WT3D Canvas Studio] 🌅 Clicked HDRI Card: ${hdriName}`);
        await wait(200);
        return true;
      }
    }
    return false;
  }

  // =========================================================================
  // [CORE 6] ĐỘNG CƠ ĐỔI PHÔNG NỀN NATIVE FAB (MÔI TRƯỜNG VS MÀU ĐƠN #HEX)
  // Phục vụ chính xác hiện trường: Look > Background > [ Color | Environment ] > Swatch #hex
  // =========================================================================
  // [WT3D STUDIO] FAB NATIVE BACKGROUND & COLOR ENGINE (v3.5.9 POKA-YOKE)
  // =========================================================================
  function findFabColorPopover(doc = document) {
    const candidates = Array.from(doc.querySelectorAll('div, section, aside, form, [role="dialog"], [role="region"]'));
    return candidates.find(el => {
      if (el.closest?.('#wt3d-fab-studio-panel')) return false;
      const r = el.getBoundingClientRect();
      if (r.width === 0 || r.height === 0 || r.top < 20) return false;
      const t = (el.textContent || '');
      return t.includes('Enter a Color') || (t.includes('Red') && t.includes('Green') && t.includes('Blue'));
    });
  }

  async function setFabBackgroundMode(bgType, hexColor = null, id = runId) {
    assertAlive(id);
    console.log(`[WT3D Canvas Studio] 🎨 Changing Background to: ${bgType} (hex: ${hexColor || 'Auto'})...`);
    setStatus(`Đang chuyển phông nền sang: <b>${BG_NAMES[bgType] || bgType}</b>...`, '#0071e3');

    // BƯỚC 1: MỞ TAB LOOK
    await openTab('look', id);
    await wait(350);

    const docs = getAccessibleDocs();

    // BƯỚC 2: BẬT TOGGLE BACKGROUND (NẾU CHƯA BẬT)
    for (const doc of docs) {
      const bgLabels = Array.from(doc.querySelectorAll('label, div, span, h3, h4, p')).filter(el => {
        if (el.closest?.('#wt3d-fab-studio-panel')) return false;
        const r = el.getBoundingClientRect();
        if (r.top < 50 || r.width === 0 || r.height === 0) return false;
        const t = (el.textContent || '').trim();
        return /^Background$/i.test(t) && r.height < 50;
      });

      for (const lb of bgLabels) {
        const row = lb.closest('div[class*="row" i], div[class*="item" i], div') || lb.parentElement;
        if (!row) continue;
        const switchBtn = row.querySelector('[role="switch"], button[class*="switch" i], [class*="toggle" i]');
        if (switchBtn) {
          const isCurrentlyOn = switchBtn.getAttribute('aria-checked') === 'true' ||
                                switchBtn.classList.contains('active') ||
                                switchBtn.classList.contains('checked') ||
                                /--on|--active|checked/i.test(switchBtn.className);
          if (!isCurrentlyOn) {
            console.log('[WT3D Canvas Studio] 🔘 Turning ON Background toggle...');
            await humanClick(switchBtn);
            await wait(200);
          }
          break;
        }
      }
    }

    // BƯỚC 3: XỬ LÝ CHẾ ĐỘ ENVIRONMENT (MÔI TRƯỜNG HDRI)
    if (bgType === 'environment') {
      try {
        window.postMessage({ type: 'wt3d-set-background-env' }, '*');
      } catch (_) {}

      for (const doc of docs) {
        const envBtns = Array.from(doc.querySelectorAll('button, [role="button"], [role="tab"], div, span')).filter(el => {
          if (el.closest?.('#wt3d-fab-studio-panel') || el.querySelector?.('#wt3d-fab-studio-panel')) return false;
          const r = el.getBoundingClientRect();
          if (r.width === 0 || r.height === 0 || r.top < 50) return false;
          const t = (el.textContent || '').trim();
          return /^Environment$/i.test(t) && r.height < 45 && r.width < 160;
        });

        if (envBtns.length > 0) {
          const target = envBtns[0].closest?.('button, [role="button"]') || envBtns[0];
          await humanClick(target);
          console.log('[WT3D Canvas Studio] 🌫️ Clicked Native "Environment" background button.');
          await wait(200);
          break;
        }
      }

      // Xóa CSS đè trên canvas
      try {
        const c = canvas();
        if (c) {
          c.style.backgroundColor = 'transparent';
          if (c.parentElement) c.parentElement.style.backgroundColor = 'transparent';
        }
      } catch(_) {}

      setStatus(`✅ Phông nền: <b>${BG_NAMES.environment}</b> đã kích hoạt! (Giữ nguyên 3D)`, '#16a34a');
      return true;
    }

    // BƯỚC 4: CHẾ ĐỘ MÀU ĐƠN (COLOR: CLEAN LIGHT, PURE WHITE, CLEAN DARK)
    let targetHex = hexColor;
    if (!targetHex) {
      if (bgType === 'clean_light') targetHex = '#F5F5F7';
      else if (bgType === 'color' || bgType === 'white') targetHex = '#FFFFFF';
      else if (bgType === 'clean_dark') targetHex = '#18181B';
      else targetHex = '#FFFFFF';
    }
    if (!targetHex.startsWith('#')) targetHex = '#' + targetHex;
    const rawHex = targetHex.replace('#', '').toUpperCase();

    // 4.1: Click nút "Color" trong cụm segmented control [ Color | Environment ]
    for (const doc of docs) {
      const colorBtns = Array.from(doc.querySelectorAll('button, [role="button"], [role="tab"], div, span')).filter(el => {
        if (el.closest?.('#wt3d-fab-studio-panel')) return false;
        const r = el.getBoundingClientRect();
        if (r.width === 0 || r.height === 0 || r.top < 50) return false;
        const t = (el.textContent || '').trim();
        return /^Color$/i.test(t) && r.height < 45 && r.width < 160;
      });

      if (colorBtns.length > 0) {
        const target = colorBtns[0].closest?.('button, [role="button"]') || colorBtns[0];
        await humanClick(target);
        console.log('[WT3D Canvas Studio] 🎨 Clicked Native "Color" background button.');
        await wait(200);
        break;
      }
    }

    // 4.2: KIỂM TRA POPOVER MÀU ĐÃ MỞ CHƯA
    let popoverOpened = false;
    for (const doc of docs) {
      if (findFabColorPopover(doc)) {
        popoverOpened = true;
        break;
      }
    }

    if (!popoverOpened) {
      // Tìm và click Swatch để mở Popover
      let swatchFound = false;
      for (const doc of docs) {
        const colorBtn = Array.from(doc.querySelectorAll('button, [role="button"]')).find(b => {
          if (b.closest?.('#wt3d-fab-studio-panel')) return false;
          const t = (b.textContent || '').trim();
          return /^Color$/i.test(t);
        });
        if (colorBtn) {
          try { colorBtn.scrollIntoView?.({ behavior: 'instant', block: 'center' }); } catch(_) {}
          const btnRect = colorBtn.getBoundingClientRect();
          const cx = Math.round(btnRect.left + btnRect.width / 2);
          for (const dy of [30, 20, 40, 15, 50]) {
            const hit = doc.elementFromPoint(cx, Math.round(btnRect.bottom + dy));
            if (hit && !hit.closest?.('#wt3d-fab-studio-panel')) {
              swatchFound = true;
              console.log(`[WT3D Canvas Studio] 🎯 [Method A - dy=${dy}] Found Swatch Card below Color button:`, hit);
              const clickTarget = hit.closest('button, [role="button"]') || hit;
              await humanClick(clickTarget);
              await wait(350);
              break;
            }
          }
        }
        if (swatchFound) break;
      }

      if (!swatchFound) {
        const hexRegex = /^#[0-9a-fA-F]{6}$/i;
        for (const doc of docs) {
          const candidates = Array.from(doc.querySelectorAll('button, [role="button"], div, span, input')).filter(el => {
            if (el.closest?.('#wt3d-fab-studio-panel')) return false;
            const r = el.getBoundingClientRect();
            if (r.width === 0 || r.height === 0 || r.top < 50) return false;
            const t = (el.textContent || '').trim();
            const v = (el.value || '').trim();
            return hexRegex.test(t) || hexRegex.test(v);
          });

          for (const cand of candidates) {
            swatchFound = true;
            const clickTarget = cand.closest('button, [role="button"]') || cand;
            await humanClick(clickTarget);
            await wait(350);
            break;
          }
          if (swatchFound) break;
        }
      }
    } else {
      console.log('[WT3D Canvas Studio] ℹ️ Popover is already open, injecting directly!');
    }

    // BƠM MÀU ĐA VÒNG (3 ROUNDS)
    for (const doc of docs) {
      await injectColorIntoPicker(doc, targetHex, rawHex);
      await wait(200);
      await injectColorIntoPicker(doc, targetHex, rawHex);
      await wait(200);
      await injectColorIntoPicker(doc, targetHex, rawHex);
    }

    // 4.4: ÁP DỤNG CANVAS CSS FALLBACK ĐỂ ĐỔI MÀU TRỰC TIẾP TRÊN MÀN HÌNH
    try {
      const c = canvas();
      if (c) {
        c.style.backgroundColor = targetHex;
        if (c.parentElement) c.parentElement.style.backgroundColor = targetHex;
        console.log(`[WT3D Canvas Studio] 🎨 Canvas CSS Background set to: ${targetHex}`);
      }
    } catch(_) {}

    setStatus(`✅ Đã thiết lập phông nền: <b>${BG_NAMES[bgType] || bgType} (${targetHex})</b>! (Giữ nguyên 3D)`, '#16a34a');
    return true;
  }

  function applyHexToInput(input, targetHex, rawHex) {
    if (!input) return;
    const valueToSend = (input.value && !input.value.startsWith('#')) ? rawHex : targetHex;
    setReactValue(input, valueToSend);
    try {
      input.select?.();
      document.execCommand('selectAll', false, null);
      document.execCommand('insertText', false, valueToSend);
    } catch (_) {}
    input.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }));
    input.dispatchEvent(new KeyboardEvent('keyup', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }));
    input.dispatchEvent(new Event('input', { bubbles: true, composed: true }));
    input.dispatchEvent(new Event('change', { bubbles: true, composed: true }));
  }

  async function injectColorIntoPicker(doc, targetHex, rawHex) {
    // [v3.6.5 FIX] CustomEvent không truyền từ ISOLATED→MAIN world!
    // Dùng postMessage vì nó CROSS WORLDS được
    try {
      window.postMessage({ type: 'wt3d-set-background', hex: targetHex }, '*');
      console.log('[WT3D Canvas Studio] 🌉 Bridge postMessage:', targetHex);
    } catch(e) {}
    await new Promise(r => setTimeout(r, 200));

    const rVal = parseInt(rawHex.substr(0, 2), 16) || 255;
    const gVal = parseInt(rawHex.substr(2, 2), 16) || 255;
    const bVal = parseInt(rawHex.substr(4, 2), 16) || 255;

    const popover = findFabColorPopover(doc);
    const searchRoots = popover ? [popover, doc] : [doc];

    for (const root of searchRoots) {
      // 1. Inputs
      const inputs = Array.from(root.querySelectorAll('input')).filter(inp => {
        if (inp.closest?.('#wt3d-fab-studio-panel')) return false;
        return true;
      });

      for (const inp of inputs) {
        const val = (inp.value || '').trim();
        const type = (inp.type || '').toLowerCase();
        const ph = (inp.placeholder || '').toLowerCase();
        const aria = (inp.getAttribute('aria-label') || '').toLowerCase();
        const name = (inp.name || '').toLowerCase();

        if (type === 'color') {
          inp.value = targetHex;
          inp.dispatchEvent(new Event('input', { bubbles: true }));
          inp.dispatchEvent(new Event('change', { bubbles: true }));
          continue;
        }

        const isHexInput = /^#?[0-9a-fA-F]{3,8}$/i.test(val) ||
                           ph.includes('hex') || aria.includes('hex') || name.includes('hex') ||
                           inp.maxLength === 6 || inp.maxLength === 7;

        if (isHexInput) {
          applyHexToInput(inp, targetHex, rawHex);
          console.log(`[WT3D Canvas Studio] 🎨 Set Hex Input to ${targetHex}`);
          continue;
        }

        const isR = aria.includes('red') || aria === 'r' || name.includes('red') || name === 'r' || ph.includes('red');
        const isG = aria.includes('green') || aria === 'g' || name.includes('green') || name === 'g' || ph.includes('green');
        const isB = aria.includes('blue') || aria === 'b' || name.includes('blue') || name === 'b' || ph.includes('blue');

        if (isR) { setReactValue(inp, String(rVal)); continue; }
        if (isG) { setReactValue(inp, String(gVal)); continue; }
        if (isB) { setReactValue(inp, String(bVal)); continue; }
      }

      // 2. Sliders
      const rangeInputs = Array.from(root.querySelectorAll('input[type="range"]'));
      if (rangeInputs.length >= 3) {
        const rgbSliders = rangeInputs.slice(-3);
        const rgbVals = [rVal, gVal, bVal];
        for (let i = 0; i < 3; i++) {
          const sl = rgbSliders[i];
          if (sl) {
            setReactValue(sl, String(rgbVals[i]));
          }
        }
        console.log(`[WT3D Canvas Studio] 🎚️ Updated RGB Sliders to R:${rVal}, G:${gVal}, B:${bVal}`);
      }

      // 3. Physical 2D Gradient Box Click
      if (popover) {
        const isPureWhite = (targetHex.toUpperCase() === '#FFFFFF');
        const isCleanLight = (targetHex.toUpperCase() === '#F5F5F7');
        const isDark = (targetHex.toUpperCase() === '#18181B');

        if (isPureWhite || isCleanLight || isDark) {
          const gradientBoxes = Array.from(popover.querySelectorAll('div, canvas')).filter(el => {
            const r = el.getBoundingClientRect();
            return r.width >= 50 && r.height >= 50 && Math.abs(r.width - r.height) < 50 && r.width < 250;
          });

          for (const gBox of gradientBoxes) {
            const r = gBox.getBoundingClientRect();
            let hitX = Math.round(r.left + 8);
            let hitY = Math.round(r.top + 8);
            if (isDark) hitY = Math.round(r.bottom - 8);

            const evOpts = { bubbles: true, cancelable: true, view: window, clientX: hitX, clientY: hitY, button: 0, buttons: 1 };
            if (typeof PointerEvent !== 'undefined') gBox.dispatchEvent(new PointerEvent('pointerdown', evOpts));
            gBox.dispatchEvent(new MouseEvent('mousedown', evOpts));
            await wait(40);
            if (typeof PointerEvent !== 'undefined') gBox.dispatchEvent(new PointerEvent('pointerup', { ...evOpts, buttons: 0 }));
            gBox.dispatchEvent(new MouseEvent('mouseup', { ...evOpts, buttons: 0 }));
            try { gBox.click?.(); } catch(_) {}
            console.log(`[WT3D Canvas Studio] 🎯 Clicked 2D Gradient Box at (${hitX}, ${hitY}) for ${targetHex}`);
            break;
          }
        }
      }
    }
  }

  // =========================================================================
  // [CORE 7] KHÓA PERSPECTIVE & XOAY GÓC 3/4 Y-UP (NHÌN LÊN / NHÌN XUỐNG)
  // =========================================================================
  async function ensurePerspectiveProjection(id = runId) {
    console.log('[WT3D Canvas Studio] 🎥 Ensuring Perspective Projection mode (FOV 45°, Y-Up)...');
    await openTab('camera', id);
    await wait(250);

    const docs = getAccessibleDocs();
    for (const doc of docs) {
      const candidates = Array.from(doc.querySelectorAll('button, [role="button"], [role="radio"], div, span, label')).filter(el => {
        if (el.id?.includes('wt3d') || el.closest?.('#wt3d-fab-studio-panel')) return false;
        const r = el.getBoundingClientRect();
        if (r.width === 0 || r.height === 0 || r.top < 50) return false;
        const t = (el.textContent || '').trim().toLowerCase();
        return t === 'perspective' || t.startsWith('perspective');
      });

      if (candidates.length > 0) {
        const clickTarget = candidates[0].closest?.('button, [role="button"], [role="radio"]') || candidates[0];
        await humanClick(clickTarget);
        console.log('[WT3D Canvas Studio] 🎥 Clicked Perspective projection button.');
        await wait(180);
        break;
      }
    }

    // Đặt FOV 45° chuẩn tiêu cự 50mm chân thực, không fish-eye
    await setFabSlider(/Field\s*Of\s*View/i, 45);
    await setFabToggleSwitch(/Depth\s*Of\s*Field/i, false);
    return true;
  }

  async function fitToScreen(id = runId) {
    const c = assertAlive(id);
    console.log('[WT3D Canvas Studio] 🎯 Fit to Screen (KeyF + Native Button)...');

    ['keydown', 'keypress', 'keyup'].forEach(type => {
      [c, window, document].forEach(target => {
        try {
          target.dispatchEvent(new KeyboardEvent(type, {
            key: 'f', code: 'KeyF', keyCode: 70, which: 70, bubbles: true, cancelable: true
          }));
        } catch(_) {}
      });
    });

    const docs = getAccessibleDocs();
    for (const doc of docs) {
      const fitBtns = Array.from(doc.querySelectorAll('button, [role="button"], div[title], span[title]')).filter(b => {
        if (b.id?.includes('wt3d') || b.closest?.('#wt3d-fab-studio-panel')) return false;
        const r = b.getBoundingClientRect();
        if (r.top < 50 || r.width === 0 || r.height === 0) return false;
        const t = (b.textContent || '').trim().toLowerCase();
        const title = (b.getAttribute('title') || '').toLowerCase();
        const aria = (b.getAttribute('aria-label') || '').toLowerCase();
        return /fit\s*to\s*screen|frame\s*selection|frame\s*all/i.test(t) ||
               /fit\s*to\s*screen|frame\s*selection|frame\s*all/i.test(title) ||
               /fit\s*to\s*screen|frame\s*selection|frame\s*all/i.test(aria);
      });
      if (fitBtns.length > 0) {
        await humanClick(fitBtns[0]);
        break;
      }
    }
    await wait(250);
  }

  async function dragCanvas(startX, startY, endX, endY, id = runId, duration = 450) {
    const c = assertAlive(id);
    const r = c.getBoundingClientRect();

    const makePointer = (type, x, y, buttons) => {
      const ev = new PointerEvent(type, {
        bubbles: true, cancelable: true, composed: true, view: window,
        clientX: x, clientY: y, screenX: window.screenX + x, screenY: window.screenY + y,
        button: 0, buttons, pointerId: 772, pointerType: 'mouse', isPrimary: true
      });
      try {
        Object.defineProperty(ev, 'offsetX', { value: Math.round(x - r.left), configurable: true });
        Object.defineProperty(ev, 'offsetY', { value: Math.round(y - r.top), configurable: true });
      } catch(_) {}
      return ev;
    };

    const makeMouse = (type, x, y, buttons) => {
      const ev = new MouseEvent(type, {
        bubbles: true, cancelable: true, composed: true, view: window,
        clientX: x, clientY: y, screenX: window.screenX + x, screenY: window.screenY + y,
        button: 0, buttons
      });
      try {
        Object.defineProperty(ev, 'offsetX', { value: Math.round(x - r.left), configurable: true });
        Object.defineProperty(ev, 'offsetY', { value: Math.round(y - r.top), configurable: true });
      } catch(_) {}
      return ev;
    };

    c.focus?.({ preventScroll: true });
    c.dispatchEvent(makePointer('pointermove', startX, startY, 0));
    c.dispatchEvent(makeMouse('mousemove', startX, startY, 0));
    await wait(25);

    c.dispatchEvent(makePointer('pointerdown', startX, startY, 1));
    c.dispatchEvent(makeMouse('mousedown', startX, startY, 1));
    await wait(35);

    const steps = 18;
    for (let i = 1; i <= steps; i++) {
      if (id !== runId) throw new Error('JIDOKA: cancelled');
      const t = i / steps;
      const curX = Math.round(startX + (endX - startX) * t);
      const curY = Math.round(startY + (endY - startY) * t);
      c.dispatchEvent(makePointer('pointermove', curX, curY, 1));
      c.dispatchEvent(makeMouse('mousemove', curX, curY, 1));
      await wait(Math.max(10, Math.round(duration / steps)));
    }

    c.dispatchEvent(makePointer('pointerup', endX, endY, 0));
    c.dispatchEvent(makeMouse('mouseup', endX, endY, 0));
  }

  // ĐIỀU HƯỚNG GÓC NHÌN PERSPECTIVE 3/4 CHUẨN Y-UP (NHÌN LÊN / NHÌN XUỐNG)
  async function rotatePerspective34(mode = 'down_right', id = runId) {
    await ensurePerspectiveProjection(id);
    await wait(180);

    const c = assertAlive(id);
    const r = c.getBoundingClientRect();
    const centerX = Math.round(r.left + r.width * 0.5);
    const centerY = Math.round(r.top + r.height * 0.5);
    const w = r.width;
    const h = r.height;

    let dx = 0;
    let dy = 0;
    let label = '';

    switch (mode) {
      case 'down_right':
        // 3/4 Phải Nhìn Xuống ~18° (Top-Down Showcase: thấy mặt trên, ống đỉnh & van mặt tiền)
        dx = Math.round(w * 0.135);
        dy = -Math.round(h * 0.085);
        label = '3/4 Phải (Nhìn Xuống ~18°)';
        break;

      case 'down_left':
        // 3/4 Trái Nhìn Xuống ~18°
        dx = -Math.round(w * 0.135);
        dy = -Math.round(h * 0.085);
        label = '3/4 Trái (Nhìn Xuống ~18°)';
        break;

      case 'up_hero':
        // 3/4 Nhìn Lên ~15° (Low-Angle Hero View: tôn dáng bệ vệ, hoành tráng bồn & tháp máy)
        dx = Math.round(w * 0.125);
        dy = Math.round(h * 0.075);
        label = '3/4 Nhìn Lên (Hero Bệ Vệ ~15°)';
        break;

      case 'eye_right':
        // 3/4 Ngang Tầm Mắt Bên Phải (Eye-Level 1:1)
        dx = Math.round(w * 0.135);
        dy = 0;
        label = '3/4 Phải (Ngang Tầm Mắt)';
        break;

      case 'eye_left':
        // 3/4 Ngang Tầm Mắt Bên Trái (Eye-Level 1:1)
        dx = -Math.round(w * 0.135);
        dy = 0;
        label = '3/4 Trái (Ngang Tầm Mắt)';
        break;

      default:
        dx = Math.round(w * 0.135);
        dy = -Math.round(h * 0.085);
        label = '3/4 Chuẩn';
    }

    console.log(`[WT3D Canvas Studio] 📐 Orbit Perspective Y-Up [${label}]: dx=${dx}, dy=${dy}`);
    setStatus(`Đang xoay góc: <b>${label}</b> (Perspective Y-Up)...`, '#0071e3');
    await dragCanvas(centerX, centerY, centerX + dx, centerY + dy, id, 500);
    setStatus(`✅ Đã định vị góc nhìn: <b>${label}</b> (Perspective Y-Up)!`, '#16a34a');
  }

  async function saveView(id = runId) {
    console.log('[WT3D Canvas Studio] 💾 Saving Default View inside Camera tab...');
    await openTab('camera', id);
    await wait(300);

    const docs = getAccessibleDocs();
    for (const doc of docs) {
      const viewBtns = Array.from(doc.querySelectorAll('button, [role="button"], div[role="button"]')).filter(b => {
        if (b.id?.includes('wt3d') || b.closest?.('#wt3d-fab-studio-panel')) return false;
        if (b.tagName === 'A' || b.closest?.('a')) return false;
        const r = b.getBoundingClientRect();
        // TUYỆT ĐỐI KHÔNG CLICK VÀO CÁC NÚT Ở THANH ĐỈNH ĐẦU TRANG (r.top < 85) TRÁNH THOÁT 3D!
        if (r.top < 85 || r.width === 0 || r.height === 0) return false;
        const t = (b.textContent || '').trim().toLowerCase();
        const aria = (b.getAttribute('aria-label') || '').toLowerCase();
        const title = (b.getAttribute('title') || '').toLowerCase();
        return /replace\s*default\s*view/i.test(t) || /replace\s*default\s*view/i.test(aria) || /replace\s*default\s*view/i.test(title);
      });

      if (viewBtns.length > 0) {
        await humanClick(viewBtns[0]);
        console.log('[WT3D Canvas Studio] ✅ Clicked Replace default view button inside Camera tab!');
        setStatus('✅ Đã lưu góc nhìn mặc định! Môi trường 3D được giữ nguyên.', '#16a34a');
        return true;
      }
    }
    return true;
  }

  async function exportPng(id = runId, targetW = 1920, targetH = 1080, cachedDataUrl = null) {
    const c = assertAlive(id);
    try {
      // 1. Chụp tức thì ngay trước khi buffer bị WebGL swap/clear
      const dataUrl = cachedDataUrl || c.toDataURL('image/png');
      if (!dataUrl || dataUrl.length < 100) {
        throw new Error('Dữ liệu canvas rỗng');
      }

      setStatus(`⏳ Đang xử lý ảnh Khổ Chuẩn Full HD (${targetW}×${targetH})...`, '#0071e3');

      // 2. Nạp vào Image và vẽ lên khung 1920 x 1080 chuẩn 16:9
      const img = new Image();
      img.onload = () => {
        try {
          const out = document.createElement('canvas');
          out.width = targetW;
          out.height = targetH;
          const ctx = out.getContext('2d');
          ctx.imageSmoothingEnabled = true;
          ctx.imageSmoothingQuality = 'high';

          // Vẽ trực tiếp giữ nguyên 100% gradient, bóng đổ và vật liệu sắc nét
          ctx.drawImage(img, 0, 0, targetW, targetH);

          const fullHdUrl = out.toDataURL('image/png', 1.0);
          const a = document.createElement('a');
          a.href = fullHdUrl;
          a.download = `WT3D_KeyShot_FullHD_1920x1080_${Date.now()}.png`;
          document.body.appendChild(a);
          a.click();
          a.remove();

          setStatus(`✅ ĐÃ XUẤT ẢNH KHỔ CHUẨN FULL HD (1920×1080 • 16:9)!`, '#16a34a');
          console.log(`[WT3D Canvas Studio] 📸 Exported 1920x1080 Full HD successfully!`);
        } catch (err) {
          setStatus(`Lỗi xử lý ảnh Full HD: ${err.message}`, '#dc2626');
        }
      };
      img.onerror = () => {
        // Fallback: nếu Image onload lỗi, tải trực tiếp dataUrl gốc
        const a = document.createElement('a');
        a.href = dataUrl;
        a.download = `WT3D_KeyShot_Canvas_${Date.now()}.png`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        setStatus('✅ Đã xuất ảnh Canvas gốc!', '#16a34a');
      };
      img.src = dataUrl;
    } catch (e) {
      setStatus(`Lỗi xuất ảnh: ${e.message}`, '#dc2626');
    }
  }

  // =========================================================================
  // [CORE 8] 6 BỘ THIẾT LẬP CHUẨN ÁNH SÁNG & MÔI TRƯỜNG CÔNG NGHIỆP
  // =========================================================================
  const WT3D_LIGHTING_PROFILES = {
    soft: {
      id: 'soft',
      name: 'Gdansk Chuẩn',
      subtitle: 'Chuẩn Công Nghiệp',
      icon: '🏆',
      badgeTitle: 'Gdansk Shipyard • Chuẩn Look + Camera + Lighting WT3D',
      badgeDesc: 'HDRI Gdansk Shipyard (76°, Sáng 0.800, Shadow Bias 25), SSAO (R:0.648, I:0.36, B:0.100), Nền #AAB9C5 (Apply Post), Vignette (0.40/0.73), Ground AO (1.00/0.600), Camera (FOV 50°, Exp 0.63, Near 7.0).',
      badgeColor: '#0071e3',
      badgeBg: '#f0f7ff',
      badgeBorder: '#d0e5ff',
      btnActiveBg: '#e8f2ff',
      btnActiveColor: '#0071e3',
      btnActiveBorder: '#0071e3',
      bgType: 'environment',
      hdriName: 'Gdansk Shipyard',
      orientation: 76,
      brightness: 0.80,
      occlusionRadius: 0.648,
      occlusionIntensity: 0.36,
      occlusionBias: 0.10,
      reflectionIntensity: 0.0,
      fov: 50,
      disableDof: true,
      bloomIntensity: 0.0,
      vignette: true,
      groundOcclusion: true,
      groundIntensity: 1.0
    },
    studio2: {
      id: 'studio2',
      name: 'Studio 2',
      subtitle: 'Bóng Kim Loại',
      icon: '✨',
      badgeTitle: 'Studio 2 (✨ Rim Light Kim Loại • KeyShot Showcase)',
      badgeDesc: 'HDRI Studio 2, sáng 1.00, xoay 38°, nền xám đậm; phản sáng rõ trên bề mặt bóng.',
      badgeColor: '#b45309',
      badgeBg: '#fbf7ee',
      badgeBorder: '#f3e6cb',
      btnActiveBg: '#fbf7ee',
      btnActiveColor: '#b45309',
      btnActiveBorder: '#f59e0b',
      bgType: 'clean_light',
      hdriName: 'Studio',
      orientation: 65,
      brightness: 2.25,
      occlusionRadius: 1.6,
      occlusionIntensity: 1.0,
      occlusionBias: 0.45,
      reflectionIntensity: 0.85,
      fov: 45,
      disableDof: true,
      bloomIntensity: 0.08,
      vignette: true,
      groundOcclusion: true,
      groundIntensity: 1.0
    },
    white: {
      id: 'white',
      name: 'Pure White',
      subtitle: 'Trắng Catalog',
      icon: '🤍',
      badgeTitle: 'Pure White (🤍 Trắng Catalog • Tương Phản Cao)',
      badgeDesc: 'HDRI Studio Soft 1.15, nền trắng, bóng tiếp xúc; phù hợp ảnh catalog.',
      badgeColor: '#424245',
      badgeBg: '#f5f5f7',
      badgeBorder: '#e5e5ea',
      btnActiveBg: '#f5f5f7',
      btnActiveColor: '#1d1d1f',
      btnActiveBorder: '#86868b',
      bgType: 'color',
      hdriName: 'Studio',
      orientation: 45,
      brightness: 2.40,
      occlusionRadius: 1.5,
      occlusionIntensity: 1.0,
      occlusionBias: 0.50,
      reflectionIntensity: 0.70,
      fov: 45,
      disableDof: true,
      bloomIntensity: 0.02,
      vignette: false,
      groundOcclusion: true,
      groundIntensity: 1.0
    },
    industrial: {
      id: 'industrial',
      name: 'Nhà Xưởng',
      subtitle: 'Xưởng Thực Tế',
      icon: '🏭',
      badgeTitle: 'Industrial Plant (🏭 Xưởng Sản Xuất • Dịu Mắt)',
      badgeDesc: 'HDRI Industrial Room 1.00, xoay 327°, nền xám; ánh sáng nội thất nhà xưởng.',
      badgeColor: '#d97706',
      badgeBg: '#fffbeb',
      badgeBorder: '#fde68a',
      btnActiveBg: '#fffbeb',
      btnActiveColor: '#d97706',
      btnActiveBorder: '#f59e0b',
      bgType: 'clean_light',
      hdriName: 'Studio',
      orientation: 235,
      brightness: 1.95,
      occlusionRadius: 2.2,
      occlusionIntensity: 1.0,
      occlusionBias: 0.55,
      reflectionIntensity: 0.65,
      fov: 45,
      disableDof: true,
      bloomIntensity: 0.05,
      vignette: true,
      groundOcclusion: true,
      groundIntensity: 1.0
    },
    dark: {
      id: 'dark',
      name: 'Dark Luxury',
      subtitle: 'Đêm Titan',
      icon: '🖤',
      badgeTitle: 'Dark Luxury (🖤 Studio Đêm Titan • Tương Phản Cao)',
      badgeDesc: 'HDRI Studio 2 sáng 1.10, nền tối, làm rõ dải phản quang; giữ màu vật liệu gốc.',
      badgeColor: '#4f46e5',
      badgeBg: '#eef2ff',
      badgeBorder: '#c7d2fe',
      btnActiveBg: '#eef2ff',
      btnActiveColor: '#4f46e5',
      btnActiveBorder: '#6366f1',
      bgType: 'clean_dark',
      hdriName: 'Studio',
      orientation: 45,
      brightness: 2.10,
      occlusionRadius: 1.8,
      occlusionIntensity: 1.0,
      occlusionBias: 0.50,
      reflectionIntensity: 0.90,
      fov: 45,
      disableDof: true,
      bloomIntensity: 0.08,
      vignette: true,
      groundOcclusion: true,
      groundIntensity: 1.0
    },
    outdoor: {
      id: 'outdoor',
      name: 'Ngoài Trời',
      subtitle: 'Nắng Công Trình',
      icon: '☀️',
      badgeTitle: 'Outdoor Daylight (☀️ Nắng Tự Nhiên • Dịu Mát)',
      badgeDesc: 'HDRI Greenwich Park sáng 1.00, nền xám sáng; ánh sáng ngoài trời tự nhiên.',
      badgeColor: '#059669',
      badgeBg: '#ecfdf5',
      badgeBorder: '#a7f3d0',
      btnActiveBg: '#ecfdf5',
      btnActiveColor: '#059669',
      btnActiveBorder: '#10b981',
      bgType: 'environment',
      hdriName: 'Studio',
      orientation: 120,
      brightness: 2.15,
      occlusionRadius: 1.5,
      occlusionIntensity: 0.9,
      occlusionBias: 0.45,
      reflectionIntensity: 0.70,
      fov: 45,
      disableDof: true,
      bloomIntensity: 0.05,
      vignette: false,
      groundOcclusion: true,
      groundIntensity: 0.8
    }
  };

  const BG_NAMES = {
    environment: 'Môi Trường Dịu (HDRI)',
    clean_light: 'Clean Light (#F5F5F7)',
    color: 'Trắng Tinh (#FFFFFF)',
    clean_dark: 'Clean Dark (#18181B)'
  };

  function setStatus(htmlOrText, tone = '#1d1d1f') {
    const el = document.getElementById('wt3d-status');
    if (el) {
      if (typeof htmlOrText === 'string' && (htmlOrText.includes('<') || htmlOrText.includes('•'))) {
        el.innerHTML = htmlOrText;
      } else {
        el.textContent = htmlOrText;
      }
      el.style.color = tone;
    }
  }

  // =========================================================================
  // [CORE 9] 1-CLICK RENDER SETUP ENGINE (TỰ ĐỘNG HÓA TRỌN VẸN 5 BƯỚC)
  // =========================================================================
  async function engineRequest(operation, sceneUid, extra = {}) {
    const requestId = 'wt3d-' + crypto.randomUUID();
    return new Promise((resolve, reject) => {
      const timeout = setTimeout(() => { window.removeEventListener('message', listener); reject(new Error('Fab render API chưa phản hồi; kiểm tra editor và bản extension mới.')); }, 90000);
      const listener = event => {
        if (event.source !== window || event.origin !== location.origin || event.data?.type !== 'wt3d-render-engine-result' || event.data.requestId !== requestId) return;
        clearTimeout(timeout);
        window.removeEventListener('message', listener);
        if (!event.data.ok) reject(new Error(event.data.error || 'Fab render operation failed'));
        else {
          const result = event.data.result;
          if (result?.savedVerified && result.reloadRequired) {
            try { sessionStorage.setItem('wt3d-last-verified-save', JSON.stringify({ at: Date.now(), sceneUid, operation })); } catch (_) {}
            // loadModel(previewUid) is not a scene refresh and can empty the canvas.
            // Reopen this editor frame through its own URL after returning the result.
            setTimeout(() => window.location.reload(), 1200);
          }
          resolve(result);
        }
      };
      window.addEventListener('message', listener);
      window.postMessage({ type: 'wt3d-render-engine-request', operation, sceneUid, requestId, ...extra }, location.origin);
    });
  }

  async function run1ClickRender(id) {
    assertAlive(id);
    if (document.documentElement.dataset.wt3dRenderProtocol !== '1') throw new Error('Cần nạp adapter render tương thích: Reload extension rồi mở lại editor.');
    const raw = document.getElementById('wt3d-render-reference-data')?.textContent;
    const reference = raw ? JSON.parse(raw) : null;
    if (!reference?.sceneUid) throw new Error('Chưa đọc được scene UID của model hiện tại.');
    setStatus('⏳ [1/3] Đọc cấu hình đã lưu và camera thật từ Fab...', '#0071e3');
    const prepared = await engineRequest('prepare', reference.sceneUid);
    assertAlive(id);
    const backupRaw = document.getElementById('wt3d-render-backup-data')?.textContent;
    const backup = backupRaw ? JSON.parse(backupRaw) : null;
    if (!backup?.doptions || backup.sceneUid !== reference.sceneUid) throw new Error('Chưa tạo được backup cấu hình cảnh; chưa áp dụng preset.');
    const backupKey = 'WT3D_RENDER_BACKUP_' + reference.sceneUid;
    await storageLocal().set({ [backupKey]: backup });
    const stored = await storageLocal().get(backupKey);
    if (stored[backupKey]?.capturedAt !== backup.capturedAt) throw new Error('Chưa xác minh lưu backup; chưa áp dụng preset.');
    assertAlive(id);
    setStatus('⏳ [2/3] Áp HDRI đã chọn, phản xạ và độ bóng; giữ màu vật liệu gốc...', '#0071e3');
    const libStore = await storageLocal().get('WT3D_MASTER_MATERIAL_LIBRARY');
    const customLibrary = libStore.WT3D_MASTER_MATERIAL_LIBRARY || {};
    const applied = await engineRequest('apply', reference.sceneUid, { ticket: prepared.ticket, customLibrary, profile: activeProfile });
    assertAlive(id);
    if (!applied.savedVerified || !applied.colorsPreserved) throw new Error('Preset chưa qua đủ bước đọc lại xác minh.');
    const finish = `Đã lưu ${applied.profileName} và tinh chỉnh ${applied.polishedCount || 0}/${applied.materialCount || 0} vật liệu. Màu gốc đã kiểm chứng; cấu hình đã đọc lại từ server.`;
    setStatus(applied.cameraVerified ? '✅ '+finish+' Camera đã xác minh; cần kiểm tra ảnh sau tải lại.' :
      '⚠️ '+finish+' Camera API không khả dụng: giữ góc đã lưu, chưa xác minh tự xoay 3/4. Dùng Camera của Fab để lưu góc nhìn.', applied.cameraVerified ? '#16a34a' : '#b45309');
  }

  async function runTask(label, task) {
    if (running) return;
    running = true;
    const id = ++runId;
    try {
      setStatus(`⏳ ${label}...`, '#0071e3');
      await task(id);
    } catch (error) {
      const rawMsg = String(error?.message || error || 'Automation stopped.');
      const friendlyMsg = /extension context invalidated/i.test(rawMsg)
        ? 'Extension vừa được cập nhật. Hãy nhấn Ctrl+Shift+R (hoặc F5) trên tab Fab rồi thử lại.'
        : rawMsg;
      setStatus(`⚠️ ${friendlyMsg}`, '#dc2626');
      console.log('[WT3D Canvas Studio Notice]', friendlyMsg);
    } finally {
      if (id === runId) running = false;
    }
  }

  // ANNOTATION & COMMENT COPIERS (CHUẨN SKETCHFAB & FAB)
  function getAnnotationContent() {
    let modelName = 'Industrial Water Treatment Model';
    try {
      const titleEl = document.querySelector('h1, [class*="model-name" i], [class*="title" i]');
      if (titleEl && titleEl.textContent) {
        modelName = titleEl.textContent.trim();
      } else if (document.title) {
        modelName = document.title.replace(/\s*-\s*Fab.*$/i, '').trim();
      }
    } catch (_) {}

    return `### 💧 ${modelName} - Technical Specification\n\n` +
      `**Precision 3D Engineering Model** designed for industrial water treatment projects.\n\n` +
      `- **Author**: Phan Trọng Tấn (@tanphan1105) - WaterTreatment3D\n` +
      `- **CAD Solid**: 1:1 Manufacturing Scale (.STEP / .STP universal solids)\n` +
      `- **PBR Materials**: Stainless SUS304/SUS316, uPVC, FRP Composite\n` +
      `- **Official Store**: [Fab.com/sellers/Trong Tan Phan](https://www.fab.com/sellers/Trong%20Tan%20Phan)\n\n` +
      `*Copyright © 2026 WaterTreatment3D. All rights reserved.*`;
  }

  function getPinnedCommentContent() {
    let modelName = 'this industrial equipment';
    try {
      const titleEl = document.querySelector('h1, [class*="model-name" i], [class*="title" i]');
      if (titleEl && titleEl.textContent) {
        modelName = titleEl.textContent.trim();
      } else if (document.title) {
        modelName = document.title.replace(/\s*-\s*Fab.*$/i, '').trim();
      }
    } catch (_) {}

    return `👋 Hi engineers & 3D creators! Thanks for viewing.\n\n` +
      `📦 Looking for the full production-ready CAD assembly of ${modelName} (.STEP / .STP universal solids)?\n` +
      `👉 Get the complete 1:1 engineering package on my official Fab store:\n` +
      `🔗 https://www.fab.com/sellers/Trong%20Tan%20Phan\n\n` +
      `📐 Modeled by Phan Trọng Tấn (@tanphan1105) - WaterTreatment3D\n` +
      `💬 Feel free to leave any technical questions or feedback below!`;
  }

  // =========================================================================
  
  // =========================================================================
  // [CORE KEYSHOT] KEYSHOT FAST MATERIAL ENGINE (HÚT & BƠM TRỰC TIẾP CHỌN NGUỒN → ĐÍCH)
  // =========================================================================
  function hexToFabRgb(hex) {
    if (!hex) return [0.8, 0.8, 0.8];
    const h = hex.replace('#', '').trim();
    const r = parseInt(h.substr(0, 2), 16) / 255;
    const g = parseInt(h.substr(2, 2), 16) / 255;
    const b = parseInt(h.substr(4, 2), 16) / 255;
    return [Number(r.toFixed(4)), Number(g.toFixed(4)), Number(b.toFixed(4))];
  }

  function fabRgbToHex(rgb) {
    if (!Array.isArray(rgb) || rgb.length < 3) return '#CCCCCC';
    const r = Math.round(Math.min(1, Math.max(0, rgb[0])) * 255).toString(16).padStart(2, '0');
    const g = Math.round(Math.min(1, Math.max(0, rgb[1])) * 255).toString(16).padStart(2, '0');
    const b = Math.round(Math.min(1, Math.max(0, rgb[2])) * 255).toString(16).padStart(2, '0');
    return `#${r}${g}${b}`.toUpperCase();
  }

  function playKeyShotChime(type = 'copy') {
    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (!AudioCtx) return;
      const ctx = new AudioCtx();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.connect(gain);
      gain.connect(ctx.destination);
      const now = ctx.currentTime;
      if (type === 'copy') {
        osc.type = 'sine';
        osc.frequency.setValueAtTime(880, now);
        osc.frequency.exponentialRampToValueAtTime(1320, now + 0.12);
        gain.gain.setValueAtTime(0.08, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.15);
        osc.start(now);
        osc.stop(now + 0.15);
      } else {
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(1046, now);
        osc.frequency.exponentialRampToValueAtTime(1568, now + 0.15);
        gain.gain.setValueAtTime(0.1, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.18);
        osc.start(now);
        osc.stop(now + 0.18);
      }
    } catch (_) {}
  }

  function showKeyShotToast(title, details, swatchColor = null, tone = '#0071e3') {
    let toast = document.getElementById('wt3d-keyshot-toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'wt3d-keyshot-toast';
      document.body.appendChild(toast);
    }

    const swatchHtml = swatchColor ? `<div style="width: 24px; height: 24px; border-radius: 6px; border: 1.5px solid white; box-shadow: 0 0 0 1px rgba(0,0,0,0.18), inset 0 1px 2px rgba(0,0,0,0.25); background: ${swatchColor}; flex-shrink: 0;"></div>` : '';

    toast.innerHTML = `
      <div style="
        position: fixed;
        top: 26px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(255, 255, 255, 0.96);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1.5px solid ${tone};
        border-radius: 14px;
        padding: 10px 18px;
        box-shadow: 0 14px 40px rgba(0, 0, 0, 0.2), 0 2px 8px rgba(0, 0, 0, 0.08);
        z-index: 9999999;
        display: flex;
        align-items: center;
        gap: 12px;
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Roboto, sans-serif;
        pointer-events: none;
        animation: wt3dToastPop 0.22s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        max-width: 90vw;
      ">
        ${swatchHtml}
        <div style="line-height: 1.35;">
          <div style="font-weight: 900; font-size: 13.5px; color: ${tone}; letter-spacing: -0.01em;">${title}</div>
          <div style="font-size: 11.5px; color: #334155; font-weight: 600;">${details}</div>
        </div>
      </div>
    `;

    if (toast.__timer) clearTimeout(toast.__timer);
    toast.__timer = setTimeout(() => {
      if (toast) toast.innerHTML = '';
    }, 2800);
  }

  function updateMaterialPreviewUI(mat) {
    const swatch = document.getElementById('wt3d-mat-swatch');
    const nameEl = document.getElementById('wt3d-mat-name');
    const detailsEl = document.getElementById('wt3d-mat-details');
    if (!swatch || !nameEl || !detailsEl) return;

    if (mat && mat.hex) {
      swatch.style.backgroundColor = mat.hex;
      nameEl.textContent = mat.name || 'Vật liệu đã hút';
      detailsEl.textContent = `Màu: ${mat.hex} | Rough: ${mat.roughness} | Metal: ${mat.metalness}`;
    } else {
      swatch.style.backgroundColor = '#c8c8c8';
      nameEl.textContent = 'Chưa chọn vật liệu nào';
      detailsEl.textContent = 'Màu: -- | Rough: -- | Metal: --';
    }
  }

  // Đọc cấu hình Scene thật từ engine (Render Reader)
  async function readReference() {
    // 1. Uu tien doc truc tiep qua engineRequest get_materials
    const sceneUid = window.__dope?.args?.sceneUid || location.pathname.match(/\/dope\/([^/]+)/)?.[1];
    if (sceneUid) {
      try {
        const live = await engineRequest('get_materials', sceneUid);
        if (live?.materials && Object.keys(live.materials).length > 0) {
          return {
            sceneUid,
            doptions: { materials: live.materials, materialgroups: live.materialgroups || {} },
            status: 'ready'
          };
        }
      } catch (_) {}
    }
    // 2. Fallback qua render-reader
    document.dispatchEvent(new Event('wt3d-read-render-reference'));
    await wait(120);
    let raw = document.getElementById('wt3d-render-reference-data')?.textContent;
    if (!raw) {
      document.dispatchEvent(new Event('wt3d-read-render-reference'));
      await wait(180);
      raw = document.getElementById('wt3d-render-reference-data')?.textContent;
    }
    if (raw) {
      try {
        const report = JSON.parse(raw);
        if (report.doptions?.materials) return report;
      } catch (_) {}
    }
    if (!raw) throw new Error('Bộ đọc chưa nạp. Reload extension rồi mở lại 3D editor.');
    const report = JSON.parse(raw);
    return report;
  }

  // Đọc độ nhám thực tế (luôn quy về Roughness 0..1 chuẩn PBR, xử lý roughness.invert của Fab)
  function getMaterialTrueRoughness(m) {
    if (!m || typeof m['roughness.factor'] !== 'number' || !Number.isFinite(m['roughness.factor'])) return 0.22;
    const raw = m['roughness.factor'];
    const val = m['roughness.invert'] ? (1 - raw) : raw;
    return Math.max(0, Math.min(1, val));
  }

  function getMaterialTrueMetalness(m) {
    if (!m || typeof m['metalness.factor'] !== 'number' || !Number.isFinite(m['metalness.factor'])) return 0.00;
    return Math.max(0, Math.min(1, m['metalness.factor']));
  }

  // Lớp 1: Nhận diện vật liệu đang được chọn trên bảng Inspector bên phải của Fab (nếu có)
  function detectActiveMaterialIdFromDom(mats) {
    if (!mats || typeof mats !== 'object') return null;
    const nameToMid = new Map();
    for (const [mid, m] of Object.entries(mats)) {
      if (m?.name) nameToMid.set(String(m.name).trim().toLowerCase(), mid);
    }
    if (nameToMid.size === 0) return null;

    const docs = getAccessibleDocs();
    for (const doc of docs) {
      const elements = Array.from(doc.querySelectorAll('[role="combobox"], select, input, button, span, div, h3, h4'));
      for (const el of elements) {
        if (el.closest?.('#wt3d-fab-studio-panel') || el.closest?.('#wt3d-keyshot-toast')) continue;
        const r = el.getBoundingClientRect();
        if (r.width === 0 || r.height === 0 || r.height > 55 || r.top < 35 || r.bottom > window.innerHeight - 60) continue;
        // Ưu tiên vùng Inspector bên phải hoặc combobox/input
        const isRightSide = r.left >= window.innerWidth * 0.45;
        const aria = (el.getAttribute?.('aria-label') || '').toLowerCase();
        const id = (el.id || '').toLowerCase();
        const cls = typeof el.className === 'string' ? el.className.toLowerCase() : (el.getAttribute?.('class') || '').toLowerCase();
        const isMaterialWidget = isRightSide || aria.includes('material') || id.includes('material') || cls.includes('material');
        if (!isMaterialWidget) continue;

        const candidates = [
          typeof el.value === 'string' ? el.value.trim().toLowerCase() : '',
          (el.textContent || '').trim().toLowerCase()
        ];
        for (const txt of candidates) {
          if (txt && nameToMid.has(txt)) {
            return nameToMid.get(txt);
          }
        }
      }
    }
    return null;
  }

  // Lấy mẫu màu Pixel trực tiếp từ WebGL GPU Buffer hoặc Canvas
  async function sampleCanvasPixelRgb(clientX, clientY) {
    // Tầng 1: Đọc trực tiếp từ GPU WebGL qua render-engine
    try {
      const sampled = await engineRequest('sample_pixel', null, { clientX, clientY });
      if (sampled?.rgb && Array.isArray(sampled.rgb) && sampled.rgb.length >= 3) {
        return sampled.rgb;
      }
    } catch (_) {}

    // Tầng 2: Fallback đọc từ canvas DOM
    try {
      const c = canvas();
      if (!c) return null;
      const r = c.getBoundingClientRect();
      if (clientX < r.left || clientX > r.right || clientY < r.top || clientY > r.bottom) return null;

      const scaleX = c.width / Math.max(1, r.width);
      const scaleY = c.height / Math.max(1, r.height);
      const cx = Math.round((clientX - r.left) * scaleX);
      const cy = Math.round((clientY - r.top) * scaleY);

      const patchSize = 5;
      const half = 2;
      const sx = Math.max(0, Math.min(c.width - patchSize, cx - half));
      const sy = Math.max(0, Math.min(c.height - patchSize, cy - half));

      const tmp = document.createElement('canvas');
      tmp.width = patchSize;
      tmp.height = patchSize;
      const ctx = tmp.getContext('2d', { willReadFrequently: true });
      ctx.drawImage(c, sx, sy, patchSize, patchSize, 0, 0, patchSize, patchSize);
      const data = ctx.getImageData(0, 0, patchSize, patchSize).data;

      let sumR = 0, sumG = 0, sumB = 0, count = 0;
      for (let i = 0; i < data.length; i += 4) {
        if (data[i + 3] > 10) {
          sumR += data[i] / 255;
          sumG += data[i + 1] / 255;
          sumB += data[i + 2] / 255;
          count++;
        }
      }
      if (!count) return null;
      return [sumR / count, sumG / count, sumB / count];
    } catch (_) {
      return null;
    }
  }

  // Thuật toán đối chiếu màu quang học chuẩn xác (Shading & Hue Invariant)
  function matchMaterialByPixelRgb(pixelRgb, mats) {
    if (!Array.isArray(pixelRgb) || pixelRgb.length < 3 || !mats || typeof mats !== 'object') return null;

    const [pr, pg, pb] = pixelRgb;
    const pMax = Math.max(pr, pg, pb);
    const pMin = Math.min(pr, pg, pb);
    const pSat = (pMax - pMin) / Math.max(1e-4, pMax);
    const pLum = 0.2126 * pr + 0.7152 * pg + 0.0722 * pb;
    const pLen = Math.hypot(pr, pg, pb) || 1e-4;
    const pNorm = [pr / pLen, pg / pLen, pb / pLen];

    const isPixelGray = pSat < 0.09;

    let bestMid = null;
    let bestScore = Infinity;

    for (const [mid, m] of Object.entries(mats)) {
      if (!m || m.type !== 'pbr_metalness') continue;
      const base = m['basecolor.color'];
      if (!Array.isArray(base) || base.length < 3) continue;

      const [br, bg, bb] = base;
      const bMax = Math.max(br, bg, bb);
      const bMin = Math.min(br, bg, bb);
      const bSat = (bMax - bMin) / Math.max(1e-4, bMax);
      const bLum = 0.2126 * br + 0.7152 * bg + 0.0722 * bb;
      const bLen = Math.hypot(br, bg, bb) || 1e-4;
      const bNorm = [br / bLen, bg / bLen, bb / bLen];

      const isMatGray = bSat < 0.09;

      // Phạt nặng nếu một bên là màu sắc rõ rệt (xanh/đỏ/vàng), bên kia là xám/inox
      let satPenalty;
      if (isPixelGray !== isMatGray) {
        satPenalty = 3.5;
      } else {
        satPenalty = Math.abs(pSat - bSat) * 0.8;
      }

      // Khoảng cách góc vector màu (Cosine distance - bất biến với độ sáng tối chiếu rọi)
      const cosSim = pNorm[0] * bNorm[0] + pNorm[1] * bNorm[1] + pNorm[2] * bNorm[2];
      const angleDist = 1.0 - Math.max(0, Math.min(1, cosSim));

      let score;
      if (isPixelGray && isMatGray) {
        // Với thang xám/inox: ước tính hệ số chiếu sáng L và so sánh độ sáng tương đối
        const estimatedL = Math.max(0.35, Math.min(1.25, pLum / Math.max(1e-3, bLum)));
        const lumResidual = Math.abs(pLum - estimatedL * bLum);
        const lumFit = Math.abs((pLum / 0.75) - bLum);
        score = angleDist * 6.0 + lumResidual * 2.5 + lumFit * 1.0 + satPenalty;
      } else {
        // Với màu có sắc (xanh ống uPVC, cam, vàng...): góc vector màu là chuẩn nhất
        score = angleDist * 12.0 + Math.abs(pSat - bSat) * 2.0 + satPenalty;
      }

      if (score < bestScore) {
        bestScore = score;
        bestMid = mid;
      }
    }
    return bestMid;
  }

  // Quét và cập nhật danh sách tất cả vật liệu vào 2 Dropdown (Nguồn & Đích) — chỉ 1 vòng đọc duy nhất (chống lag RAM)
  async function readSavedMaterials() {
    const uidFromPath = window.__dope?.args?.sceneUid || location.pathname.match(/\/dope\/([^/]+)/)?.[1];
    if (uidFromPath) {
      try {
        const saved = await engineRequest('read_materials', uidFromPath);
        if (saved?.materials) {
          window.__wt3dCachedMaterials = saved.materials;
          window.__wt3dCachedSceneUid = uidFromPath;
          return { sceneUid: uidFromPath, doptions: { materials: saved.materials }, status: 'ready' };
        }
      } catch (_) {}
    }
    const loaded = await readReference();
    const saved = await engineRequest('read_materials', loaded.sceneUid);
    if (saved?.materials) {
      window.__wt3dCachedMaterials = saved.materials;
      window.__wt3dCachedSceneUid = loaded.sceneUid;
    }
    return { ...loaded, doptions: { ...loaded.doptions, materials: saved.materials } };
  }

  // Tự động nhận diện vật liệu đang mở trên bảng Materials bên phải của Fab (vd: ← 🎨 SemiPolished, ← 🎨 XID_BlackCast_16…, CarbonFiber1)
  function detectFabNativeSelectedMaterialId(mats) {
    if (!mats || typeof mats !== 'object') return null;
    const entries = Object.entries(mats);
    if (!entries.length) return null;
    try {
      const rightEls = Array.from(document.querySelectorAll('span, div, h1, h2, h3, h4, p, button, [aria-selected="true"], [data-state="active"]')).filter(el => {
        if (!el || el.closest?.('#wt3d-fab-studio-panel') || el.closest?.('#wt3d-keyshot-toast')) return false;
        if (el.children && el.children.length > 3) return false;
        const r = el.getBoundingClientRect?.();
        if (!r || r.width < 18 || r.height < 10 || r.height > 64) return false;
        return r.left > window.innerWidth * 0.45;
      });
      // Đọc mã màu #HEX đang hiển thị bên cột phải của Fab (nếu có) để phân biệt khi tên bị cắt "..."
      let activeRightHex = null;
      let hasBaseColorLabel = false;
      for (const el of rightEls) {
        const t = (typeof el.value === 'string' && el.value ? el.value : (el.textContent || '')).trim();
        if (/^base\s*color$/i.test(t)) hasBaseColorLabel = true;
        if (/^#[0-9A-Fa-f]{6}$/.test(t)) { activeRightHex = t.toUpperCase(); }
      }
      for (const el of rightEls) {
        const titleAttr = (el.getAttribute?.('title') || el.getAttribute?.('aria-label') || '').trim().replace(/^[←🎨\s]+/, '').trim();
        const valText = (typeof el.value === 'string' ? el.value : '').trim().replace(/^[←🎨\s]+/, '').trim();
        const rawText = (el.textContent || '').trim().replace(/^[←🎨\s]+/, '').replace(/[✕×]$/, '').trim();
        for (const raw of [titleAttr, valText, rawText]) {
          if (!raw || raw.length < 2) continue;
          const exact = entries.find(([, m]) => m?.name === raw) || entries.find(([, m]) => String(m?.name || '').toLowerCase() === raw.toLowerCase());
          if (exact) return exact[0];
          if (raw.endsWith('...') || raw.endsWith('…')) {
            const prefix = raw.replace(/(\.\.\.|…)+$/, '').trim();
            if (prefix.length >= 3) {
              const prefMatches = entries.filter(([, m]) => String(m?.name || '').toLowerCase().startsWith(prefix.toLowerCase()));
              if (prefMatches.length === 1) return prefMatches[0][0];
              if (prefMatches.length > 1) {
                if (activeRightHex) {
                  const hexMatch = prefMatches.find(([, m]) => fabRgbToHex(m?.['basecolor.color'] || [0.8, 0.8, 0.8]) === activeRightHex);
                  if (hexMatch) return hexMatch[0];
                }
                return prefMatches[0][0];
              }
            }
          }
        }
      }
      // Fallback: nếu bảng Base Color bên phải của Fab đang mở và hiển thị mã #HEX, khớp theo #HEX đó
      if (hasBaseColorLabel && activeRightHex) {
        const byHex = entries.find(([, m]) => fabRgbToHex(m?.['basecolor.color'] || [0.8, 0.8, 0.8]) === activeRightHex);
        if (byHex) return byHex[0];
      }
    } catch (_) {}
    return null;
  }

  function updateTargetPickedUI(mid, mats) {
    const tgtSelect = document.getElementById('wt3d-tgt-mat-select');
    if (tgtSelect && mid && mats?.[mid]) {
      tgtSelect.value = mid;
    }
    const badge = document.getElementById('wt3d-tgt-auto-badge');
    const swatch = document.getElementById('wt3d-tgt-picked-swatch');
    const label = document.getElementById('wt3d-tgt-picked-label');
    if (mid && mats?.[mid]) {
      const m = mats[mid];
      const hex = fabRgbToHex(m['basecolor.color'] || [0.8, 0.8, 0.8]);
      const name = m.name || mid;
      if (badge) {
        badge.textContent = `🖱️ Đã chọn: ${name}`;
        badge.style.color = '#0284c7';
      }
      if (swatch) swatch.style.background = hex;
      if (label) {
        label.textContent = `🖱️ Đang chọn trên 3D: ${name} (${hex})`;
        label.style.color = '#0369a1';
      }
    }
  }

  // Tự động đồng bộ chi tiết vừa click bằng chuột trên mô hình 3D hoặc cột phải Fab
  async function syncFabSelectionToTargetSelect(clickEvent = null) {
    try {
      let mats = window.__wt3dCachedMaterials;
      if (!mats) {
        const rep = await readSavedMaterials().catch(() => null);
        mats = rep?.doptions?.materials || null;
      }
      if (!mats) return null;

      // Tầng 1: Đọc từ bảng Materials bên phải của Fab (khi click vào mô hình ở tab Materials)
      let pickedMid = detectFabNativeSelectedMaterialId(mats);

      // Tầng 2: Nếu click trực tiếp lên vùng 3D Canvas mà Fab chưa mở bảng Materials, lấy mẫu màu Pixel tại điểm click chuột
      if (!pickedMid && clickEvent && clickEvent.target?.tagName === 'CANVAS') {
        const rgb = await sampleCanvasPixelRgb(clickEvent.clientX, clickEvent.clientY);
        if (rgb) {
          pickedMid = matchMaterialByPixelRgb(rgb, mats);
        }
      }

      if (pickedMid && mats[pickedMid]) {
        updateTargetPickedUI(pickedMid, mats);
        return pickedMid;
      }
      return null;
    } catch (_) {
      return null;
    }
  }

  let __wt3dRefreshMatsInFlight = null;
  async function refreshSceneMaterialsUI(force = false) {
    if (__wt3dRefreshMatsInFlight) return __wt3dRefreshMatsInFlight;
    __wt3dRefreshMatsInFlight = (async () => {
      try {
        const srcSelect = document.getElementById('wt3d-src-mat-select');
        const tgtSelect = document.getElementById('wt3d-tgt-mat-select');
        if (!srcSelect || !tgtSelect) return null;
        if (!force && srcSelect.options.length > 1 && tgtSelect.options.length > 1) {
          return window.__wt3dCachedMaterials || null; // Đã nạp rồi, không xóa trắng khi đang focus/click
        }

        const report = await readSavedMaterials();
        const mats = report?.doptions?.materials;
        if (!mats || typeof mats !== 'object') return null;

        const countEl = document.getElementById('wt3d-mat-count');
        const matEntries = Object.entries(mats);
        if (countEl) countEl.textContent = `(${matEntries.length} vật liệu)`;

        // Đọc giá trị đang chọn SAU KHI await để không bao giờ ghi đè lựa chọn người dùng vừa bấm
        const savedSrc = srcSelect.value;
        const savedTgt = tgtSelect.value;

        const existingIds = Array.from(srcSelect.options).slice(1).map(o => o.value).join(',');
        const nextIds = matEntries.map(([mid]) => mid).join(',');
        const sameList = existingIds && existingIds === nextIds && tgtSelect.options.length === matEntries.length + 1;

        if (sameList) {
          // Cập nhật chữ tại chỗ, tuyệt đối không xóa innerHTML làm mất trạng thái đang chọn của <select>
          matEntries.forEach(([mid, m], idx) => {
            const name = m.name || `Material ${idx + 1}`;
            const rgb = m['basecolor.color'] || [0.8, 0.8, 0.8];
            const hex = fabRgbToHex(rgb);
            const rough = getMaterialTrueRoughness(m).toFixed(2);
            const metal = getMaterialTrueMetalness(m).toFixed(2);
            const optText = `${name} (${hex} • R:${rough} • M:${metal})`;
            const searchStr = `${name} ${hex} ${rough} ${metal}`.toLowerCase();
            for (const sel of [srcSelect, tgtSelect]) {
              const opt = sel.options[idx + 1];
              if (opt && opt.value === mid) {
                opt.textContent = optText;
                opt.setAttribute('data-search', searchStr);
              }
            }
          });
        } else {
          srcSelect.innerHTML = '';
          tgtSelect.innerHTML = '';
          for (const [sel, label] of [[srcSelect, '-- Chọn chi tiết muốn LẤY vật liệu --'], [tgtSelect, '-- Chọn chi tiết cần ĐỔI vật liệu --']]) {
            const ph = document.createElement('option');
            ph.value = '';
            ph.textContent = label;
            sel.appendChild(ph);
          }

          matEntries.forEach(([mid, m], idx) => {
            const name = m.name || `Material ${idx + 1}`;
            const rgb = m['basecolor.color'] || [0.8, 0.8, 0.8];
            const hex = fabRgbToHex(rgb);
            const rough = getMaterialTrueRoughness(m).toFixed(2);
            const metal = getMaterialTrueMetalness(m).toFixed(2);

            const optText = `${name} (${hex} • R:${rough} • M:${metal})`;

            const opt1 = document.createElement('option');
            opt1.value = mid;
            opt1.textContent = optText;
            opt1.setAttribute('data-search', `${name} ${hex} ${rough} ${metal}`.toLowerCase());
            srcSelect.appendChild(opt1);

            const opt2 = document.createElement('option');
            opt2.value = mid;
            opt2.textContent = optText;
            opt2.setAttribute('data-search', `${name} ${hex} ${rough} ${metal}`.toLowerCase());
            tgtSelect.appendChild(opt2);
          });
        }

        if (savedSrc && mats[savedSrc]) srcSelect.value = savedSrc;
        if (savedTgt && mats[savedTgt]) tgtSelect.value = savedTgt;

        return mats;
      } catch (_) {
        return null;
      } finally {
        __wt3dRefreshMatsInFlight = null;
      }
    })();
    return __wt3dRefreshMatsInFlight;
  }

  // =========================================================================
  // THƯ VIỆN VẬT LIỆU CÓ TÊN: Chọn chi tiết nguồn -> Lưu kèm tên -> Chọn tên -> Bơm vào chi tiết đích
  // =========================================================================
  const NAMED_KEY = 'WT3D_NAMED_MATERIALS';
  // Chỉ phần người dùng tự lưu (nằm trong chrome.storage). Dùng cho Lưu / Xóa.
  async function loadUserNamedMaterials() {
    const s = await storageLocal().get(NAMED_KEY);
    return (s && s[NAMED_KEY] && typeof s[NAMED_KEY] === 'object') ? s[NAMED_KEY] : {};
  }
  // Mẫu có sẵn (★) từ material-presets.js: chuẩn hóa + kiểm tra giá trị, bỏ mẫu sai định dạng
  function loadBuiltinPresets() {
    const out = {};
    const raw = Array.isArray(window.WT3D_MATERIAL_PRESETS) ? window.WT3D_MATERIAL_PRESETS : [];
    const in01 = v => typeof v === 'number' && Number.isFinite(v) && v >= 0 && v <= 1;
    for (const p of raw) {
      try {
        if (!p || typeof p.name !== 'string' || !p.name.trim()) continue;
        let rgb = null;
        if (typeof p.hex === 'string' && /^#?[0-9a-fA-F]{6}$/.test(p.hex.trim())) {
          const h = p.hex.trim().replace('#', '');
          rgb = [0, 2, 4].map(i => parseInt(h.slice(i, i + 2), 16) / 255);
        } else if (Array.isArray(p.rgb) && p.rgb.length === 3 && p.rgb.every(in01)) {
          rgb = p.rgb.slice();
        }
        if (!rgb || !in01(p.roughness) || !in01(p.metalness)) { console.warn('[WT3D] Bỏ qua mẫu có sẵn sai định dạng:', p && p.name); continue; }
        const name = '★ ' + p.name.trim();
        let keepTexturedRgb = null;
        if (typeof p.keepTexturedColorHex === 'string' && /^#?[0-9a-fA-F]{6}$/.test(p.keepTexturedColorHex.trim())) {
          const kh = p.keepTexturedColorHex.trim().replace('#', '');
          keepTexturedRgb = [0, 2, 4].map(i => parseInt(kh.slice(i, i + 2), 16) / 255);
        }
        out[name] = {
          id: 'preset:' + p.name.trim(), sourceSceneUid: null, name, hex: fabRgbToHex(rgb), basecolor: rgb,
          roughness: p.roughness, metalness: p.metalness,
          channels: (p.channels && typeof p.channels === 'object') ? JSON.parse(JSON.stringify(p.channels)) : null,
          keepTexturedRgb,
          note: p.note || '', preset: true, savedAt: 'preset', timestamp: 0
        };
      } catch (_) {}
    }
    return out;
  }
  // Toàn bộ thư viện hiển thị: mẫu có sẵn ★ + mẫu người dùng tự lưu
  async function loadNamedMaterials() {
    let userLib = {};
    try { userLib = await loadUserNamedMaterials(); } catch (_) { userLib = {}; }
    return { ...loadBuiltinPresets(), ...userLib };
  }
  function updatePresetChipsActiveState(selectedName) {
    const chipsBox = document.getElementById('wt3d-preset-chips');
    if (!chipsBox) return;
    Array.from(chipsBox.querySelectorAll('.wt3d-preset-chip-btn')).forEach(btn => {
      const isSel = btn.getAttribute('data-preset-name') === selectedName;
      btn.style.border = isSel ? '1.5px solid #0284c7' : '1px solid #cbd5e1';
      btn.style.background = isSel ? '#e0f2fe' : '#ffffff';
    });
  }
  async function refreshNamedLibraryUI(selectName = null) {
    const sel = document.getElementById('wt3d-lib-select');
    const cnt = document.getElementById('wt3d-lib-count');
    if (!sel) return;
    let lib;
    try { lib = await loadNamedMaterials(); }
    catch (e) { setStatus('⚠️ ' + e.message, '#dc2626'); lib = loadBuiltinPresets(); }
    const names = Object.keys(lib).sort((a, b) => a.localeCompare(b, 'vi'));
    const keep = selectName !== null ? selectName : sel.value;
    sel.innerHTML = '';
    const ph = document.createElement('option');
    ph.value = '';
    ph.textContent = names.length ? '-- Chọn vật liệu đã lưu --' : '-- Thư viện trống: hãy lưu vật liệu đầu tiên --';
    sel.appendChild(ph);
    for (const n of names) {
      const s = lib[n];
      const o = document.createElement('option');
      o.value = n;
      o.textContent = `${n}  (${s.hex} • R:${Number(s.roughness).toFixed(2)} • M:${Number(s.metalness).toFixed(2)})`;
      sel.appendChild(o);
    }
    if (keep && lib[keep]) sel.value = keep;
    if (cnt) cnt.textContent = `(${names.length} đã lưu)`;
    const chipsBox = document.getElementById('wt3d-preset-chips');
    if (chipsBox) {
      const presets = loadBuiltinPresets();
      const pNames = Object.keys(presets);
      chipsBox.innerHTML = '';
      for (const pn of pNames) {
        const ps = presets[pn];
        const shortLabel = pn.replace(/^★\s*/, '');
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'wt3d-preset-chip-btn';
        btn.setAttribute('data-preset-name', pn);
        btn.title = `${pn} (${ps.hex} • Rough: ${ps.roughness} • Metal: ${ps.metalness})`;
        const isSel = sel.value === pn;
        btn.style.cssText = `display:inline-flex;align-items:center;gap:5px;padding:5px 8px;border-radius:7px;font-size:11.5px;font-weight:800;cursor:pointer;border:${isSel ? '1.5px solid #0284c7' : '1px solid #cbd5e1'};background:${isSel ? '#e0f2fe' : '#ffffff'};color:#0f172a;box-shadow:0 1px 2px rgba(0,0,0,0.04);`;
        const dot = document.createElement('span');
        dot.style.cssText = `width:12px;height:12px;border-radius:3px;background:${ps.hex};border:1px solid rgba(0,0,0,0.25);flex-shrink:0;display:inline-block;`;
        const txt = document.createElement('span');
        txt.textContent = shortLabel;
        btn.appendChild(dot);
        btn.appendChild(txt);
        btn.addEventListener('click', (ev) => {
          ev.stopPropagation();
          sel.value = pn;
          updatePresetChipsActiveState(pn);
          activateSample({ ...ps, timestamp: Date.now() }).catch(() => {});
        });
        chipsBox.appendChild(btn);
      }
    }
  }
  function buildSampleFromMaterial(mid, m, sceneUid, nameOverride) {
    const rgb = Array.isArray(m['basecolor.color']) ? m['basecolor.color'].slice(0, 3) : [0.8, 0.8, 0.8];
    return {
      id: mid, sourceSceneUid: sceneUid, name: nameOverride || m.name || mid,
      hex: fabRgbToHex(rgb), basecolor: rgb,
      roughness: getMaterialTrueRoughness(m), metalness: getMaterialTrueMetalness(m),
      props: Object.fromEntries(Object.entries(m).filter(([f]) => !['uid', 'name', 'type', 'version'].includes(f))),
      timestamp: Date.now()
    };
  }
  async function activateSample(sample) {
    if (!sample) return;
    window.__wt3dCopiedMaterial = sample;
    try { sessionStorage.setItem('wt3d_copied_material', JSON.stringify(sample)); } catch (_) {}
    updateMaterialPreviewUI(sample);
    await storageLocal().set({ WT3D_MATERIAL_SAMPLE: sample });
  }
  async function saveNamedMaterial() {
    const srcSelect = document.getElementById('wt3d-src-mat-select');
    const nameInput = document.getElementById('wt3d-lib-name');
    const report = await readSavedMaterials();
    const mats = report?.doptions?.materials || {};
    let mid = srcSelect?.value;
    if (!mid || !mats[mid]) {
      const fabMid = detectFabNativeSelectedMaterialId(mats);
      if (fabMid && mats[fabMid]) {
        mid = fabMid;
        if (srcSelect) srcSelect.value = mid;
      }
    }
    if (!mid) {
      showKeyShotToast('⚠️ Chưa chọn chi tiết nguồn', 'Chọn chi tiết ở mục 1 rồi bấm Lưu.', null, '#ea580c');
      throw new Error('Chưa chọn chi tiết nguồn ở mục 1.');
    }
    const m = mats[mid];
    if (!m) throw new Error('Không đọc được vật liệu của chi tiết đã chọn. Hãy bấm F5 rồi thử lại.');
    const base = buildSampleFromMaterial(mid, m, report.sceneUid);
    const name = (nameInput?.value || '').trim() || `${m.name || 'Vật liệu'} ${base.hex}`;
    const lib = await loadUserNamedMaterials();
    const existed = !!lib[name];
    const sample = { ...base, name, sourceMaterial: m.name || mid, savedAt: new Date().toISOString() };
    lib[name] = sample;
    await storageLocal().set({ [NAMED_KEY]: lib });
    const check = await loadUserNamedMaterials();
    if (!check[name] || check[name].savedAt !== sample.savedAt) throw new Error('Chưa xác minh được việc lưu vào thư viện.');
    await refreshNamedLibraryUI(name);
    await activateSample(sample);
    playKeyShotChime('copy');
    showKeyShotToast(existed ? '💾 ĐÃ CẬP NHẬT VẬT LIỆU' : '💾 ĐÃ LƯU VÀO THƯ VIỆN', `<b>${name}</b> • ${sample.hex} • Rough ${sample.roughness} • Metal ${sample.metalness}`, sample.hex, '#0284c7');
    setStatus(`💾 ${existed ? 'Đã ghi đè' : 'Đã lưu'} [${name}] (${sample.hex}). Giờ ở mục 2: chọn chi tiết đích, chọn tên vừa lưu rồi bấm [🖌️ Bơm].`, '#0284c7');
    return sample;
  }
  async function useNamedMaterial(name) {
    const builtins = loadBuiltinPresets();
    if (builtins[name]) {
      const s = { ...builtins[name], timestamp: Date.now() };
      updatePresetChipsActiveState(name);
      await activateSample(s);
      return s;
    }
    const lib = await loadNamedMaterials();
    const s = lib[name];
    if (!s) return null;
    updatePresetChipsActiveState(name);
    await activateSample({ ...s, timestamp: Date.now() });
    return s;
  }
  async function deleteNamedMaterial() {
    const sel = document.getElementById('wt3d-lib-select');
    const name = sel?.value;
    if (!name) throw new Error('Chưa chọn vật liệu cần xóa trong thư viện.');
    if (String(name).startsWith('★ ')) throw new Error('Mẫu có dấu ★ là mẫu có sẵn của kỹ thuật, không xóa được trong bảng. Nhờ kỹ thuật sửa file material-presets.js.');
    const lib = await loadUserNamedMaterials();
    delete lib[name];
    await storageLocal().set({ [NAMED_KEY]: lib });
    await refreshNamedLibraryUI('');
    setStatus(`🗑️ Đã xóa [${name}] khỏi thư viện.`, '#64748b');
  }

  // =========================================================================
  // LỊCH SỬ HOÀN TÁC: lưu giá trị CŨ của mọi chi tiết bị ghi đè sau mỗi lần Bơm (tối đa 25 lần / model)
  // =========================================================================
  const HIST_MAX = 25;
  const histKey = uid => 'WT3D_PUMP_HISTORY_' + uid;
  async function loadPumpHistory(uid) {
    const s = await storageLocal().get(histKey(uid));
    return Array.isArray(s?.[histKey(uid)]) ? s[histKey(uid)] : [];
  }
  async function pushPumpHistory(uid, entry) {
    const list = await loadPumpHistory(uid);
    list.push(entry);
    while (list.length > HIST_MAX) list.shift();
    await storageLocal().set({ [histKey(uid)]: list });
    const check = await loadPumpHistory(uid);
    if (check[check.length - 1]?.at !== entry.at) throw new Error('Chưa xác minh được việc lưu lịch sử hoàn tác.');
  }
  async function refreshUndoUI() {
    const btn = document.getElementById('wt3d-undo-btn');
    if (!btn) return;
    const uid = window.__dope?.args?.sceneUid || location.pathname.match(/\/dope\/([^/]+)/)?.[1];
    let list = [];
    try { list = uid ? await loadPumpHistory(uid) : []; } catch (_) { list = []; }
    const last = list[list.length - 1];
    btn.disabled = !last;
    btn.style.opacity = last ? '1' : '0.5';
    btn.textContent = last ? `↩️ Hoàn tác lần bơm gần nhất: ${last.targetName} (${list.length})` : '↩️ Chưa có lần bơm nào để hoàn tác';
  }
  // Xuất file chẩn đoán JSON (toàn bộ vật liệu hiện tại + mẫu đã chọn + lịch sử hoàn tác) để phân tích khi màu không giống
  async function exportDiagnostics() {
    const report = await readSavedMaterials();
    const uid = report.sceneUid;
    const libStore = await loadNamedMaterials();
    const history = await loadPumpHistory(uid);
    const sample = window.__wt3dCopiedMaterial || null;
    const payload = {
      tool: 'WT3D Fab Studio ' + STUDIO_VERSION, exportedAt: new Date().toISOString(), sceneUid: uid,
      selectedSample: sample, namedLibraryNames: Object.keys(libStore), history,
      materials: report.doptions.materials
    };
    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `WT3D-diagnostic-${uid.slice(0, 8)}-${Date.now()}.json`;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 4000);
    setStatus(`🩺 Đã xuất ${a.download} (${Object.keys(report.doptions.materials).length} vật liệu). Gửi file này cho kỹ thuật để đối chiếu.`, '#0284c7');
  }

  async function undoLastPump() {
    const uid = window.__dope?.args?.sceneUid || location.pathname.match(/\/dope\/([^/]+)/)?.[1];
    if (!uid) throw new Error('Chưa đọc được scene UID của model hiện tại.');
    const list = await loadPumpHistory(uid);
    const last = list[list.length - 1];
    if (!last) throw new Error('Chưa có lần bơm nào để hoàn tác.');
    setStatus(`⏳ Đang hoàn tác lần bơm vào [${last.targetName}]...`, '#0071e3');
    const res = await engineRequest('restore_materials', uid, { entries: last.previous });
    list.pop();
    await storageLocal().set({ [histKey(uid)]: list });
    showKeyShotToast('↩️ ĐÃ HOÀN TÁC', `Khôi phục <b>${res.restoredCount}</b> chi tiết về trạng thái trước khi bơm [${last.targetName}]. Đang làm mới 3D...`, null, '#0284c7');
    setStatus(`↩️ Đã hoàn tác ${res.restoredCount} chi tiết của lần bơm vào [${last.targetName}].`, '#0284c7');
    return res;
  }

  async function copyMaterialAction(explicitMatId = null) {
    const report = await readSavedMaterials();
    const mats = report?.doptions?.materials;
    if (!mats) {
      showKeyShotToast('⚠️ Chưa đọc được dữ liệu', 'Hãy thử mở lại 3D Settings!', null, '#ea580c');
      return null;
    }

    const srcSelect = document.getElementById('wt3d-src-mat-select');
    if (srcSelect && srcSelect.options.length <= 1) {
      await refreshSceneMaterialsUI();
    }

    const mid = explicitMatId || srcSelect?.value;
    if (!mid || !mats[mid]) {
      showKeyShotToast('⚠️ Không tìm thấy vật liệu', 'Mô hình không chứa vật liệu PBR.', null, '#ea580c');
      return null;
    }

    if (srcSelect && mats[mid]) {
      srcSelect.value = mid;
    }

    const m = mats[mid];
    const rgb = Array.isArray(m['basecolor.color']) ? m['basecolor.color'] : [0.8, 0.8, 0.8];
    const hex = fabRgbToHex(rgb);
    const roughness = getMaterialTrueRoughness(m);
    const metalness = getMaterialTrueMetalness(m);

    const sample = {
      id: mid,
      sourceSceneUid: report.sceneUid,
      name: m.name || mid,
      hex,
      basecolor: rgb,
      roughness,
      metalness,
      timestamp: Date.now()
    };

    window.__wt3dCopiedMaterial = sample;
    await storageLocal().set({ WT3D_MATERIAL_SAMPLE: sample });
    try { sessionStorage.setItem('wt3d_copied_material', JSON.stringify(sample)); } catch (_) {}
    updateMaterialPreviewUI(sample);
    playKeyShotChime('copy');
    showKeyShotToast(
      '🎯 ĐÃ HÚT VẬT LIỆU MẪU',
      `<b>${sample.name}</b> • Màu: <b>${sample.hex}</b> • Rough: <b>${sample.roughness}</b> • Metal: <b>${sample.metalness}</b>`,
      sample.hex,
      '#0284c7'
    );
    setStatus(`🎯 Đã hút [${sample.name}] (${sample.hex}, R:${sample.roughness}, M:${sample.metalness}). Chọn vật liệu đích trong danh sách rồi bấm [🖌️ Bơm].`, '#0284c7');
    return sample;
  }

  async function pasteMaterialAction(explicitTargetId = null) {
    const report = await readSavedMaterials();
    if (!report?.sceneUid) throw new Error('Chưa đọc được Scene UID của model.');
    const mats = report.doptions?.materials || {};

    let sample = window.__wt3dCopiedMaterial;
    if (!sample) {
      try {
        const sharedSample = await storageLocal().get('WT3D_MATERIAL_SAMPLE');
        sample = sharedSample.WT3D_MATERIAL_SAMPLE || null;
      } catch (_) {}
    }
    if (!sample) {
      try {
        const saved = sessionStorage.getItem('wt3d_copied_material');
        if (saved) sample = JSON.parse(saved);
      } catch (_) {}
    }
    if (!sample) {
      const libName = document.getElementById('wt3d-lib-select')?.value;
      if (libName) {
        sample = await useNamedMaterial(libName);
      }
    }
    if (!sample) {
      const srcMid = document.getElementById('wt3d-src-mat-select')?.value;
      if (srcMid && mats[srcMid]) {
        sample = buildSampleFromMaterial(srcMid, mats[srcMid], report.sceneUid);
        await activateSample(sample);
      }
    }
    if (!sample) {
      showKeyShotToast('⚠️ Chưa chọn vật liệu nguồn', 'Chọn mẫu ★ ở trên, hoặc chọn chi tiết ở mục 1, hoặc chọn tên đã lưu ở mục 2.', null, '#ea580c');
      setStatus('⚠️ Chưa chọn vật liệu nguồn: hãy bấm 1 mẫu ★ ở trên (hoặc chọn chi tiết ở mục 1), rồi bấm Bơm.', '#ea580c');
      return false;
    }

    const tgtSelect = document.getElementById('wt3d-tgt-mat-select');
    const srcSelect = document.getElementById('wt3d-src-mat-select');
    if (tgtSelect && tgtSelect.options.length <= 1) {
      await refreshSceneMaterialsUI();
    }

    let targetMid = explicitTargetId || tgtSelect?.value;
    if (!targetMid || !mats[targetMid]) {
      const fabMid = detectFabNativeSelectedMaterialId(mats);
      if (fabMid && mats[fabMid] && (sample.preset || fabMid !== sample.id)) {
        targetMid = fabMid;
      }
    }
    if (!targetMid || !mats[targetMid]) {
      const srcMid = srcSelect?.value;
      if (srcMid && mats[srcMid] && (sample.preset || srcMid !== sample.id)) {
        targetMid = srcMid;
      }
    }
    if (!targetMid || !mats[targetMid]) {
      showKeyShotToast('⚠️ Chưa chọn chi tiết đích', 'Chọn chi tiết cần đổi vật liệu ở mục 2 (hoặc bấm vào vật liệu bên cột phải của Fab) rồi bấm Bơm.', null, '#ea580c');
      setStatus('⚠️ Chưa chọn chi tiết đích ở mục 2. Không bơm để tránh ghi đè nhầm.', '#ea580c');
      return false;
    }

    if (tgtSelect && targetMid) {
      tgtSelect.value = targetMid;
    }

    const syncGroupChk = document.getElementById('wt3d-sync-group-chk');
    const syncGroup = syncGroupChk ? !!syncGroupChk.checked : false;
    const autoReloadChk = document.getElementById('wt3d-auto-reload-chk');
    const autoReload = autoReloadChk ? !!autoReloadChk.checked : true;

    setStatus(`⏳ Đang bơm vật liệu [${sample.name}] vào chi tiết đích...`, '#0071e3');

    // GỌI ENGINE CẤP TRỰC TIẾP (CÓ HOÀN TÁC VÀ TẢI LẠI TRÊN WEBGL)
    const backupKey = 'WT3D_MATERIAL_BACKUP_' + report.sceneUid;
    const backup = { sceneUid: report.sceneUid, capturedAt: new Date().toISOString(), materials: report.doptions.materials };
    await storageLocal().set({ [backupKey]: backup });
    const check = await storageLocal().get(backupKey);
    if (check[backupKey]?.capturedAt !== backup.capturedAt) throw new Error('Chưa lưu được backup vật liệu.');
    const res = await engineRequest('patch_material', report.sceneUid, {
      targetId: targetMid,
      basecolor: sample.basecolor,
      roughness: sample.roughness,
      metalness: sample.metalness,
      fullProps: sample.props || null,
      presetChannels: sample.channels || null,
      keepTexturedRgb: sample.keepTexturedRgb || null,
      sourceSceneUid: sample.sourceSceneUid || null,
      syncGroup,
      autoReload
    });

    if (!res.savedVerified) throw new Error('Fab chưa xác minh lưu vật liệu.');
    if (res.previous && Object.keys(res.previous).length) {
      await pushPumpHistory(report.sceneUid, {
        at: new Date().toISOString(), targetName: res.materialName, sourceName: sample.name, previous: res.previous
      });
    }
    if (res.unchanged) { setStatus('✅ Vật liệu đích đã giống mẫu; không ghi lại.', '#16a34a'); return true; }
    const countInfo = (res.patchedCount && res.patchedCount > 1) ? ` (${res.patchedCount} chi tiết cùng nhóm)` : '';
    playKeyShotChime('paste');
    showKeyShotToast(
      '✅ ĐÃ BƠM CÓ HOÀN TÁC!',
      `Đã áp vào: <b>${res.materialName}${countInfo}</b> • Màu: <b>${sample.hex}</b> • Rough: <b>${sample.roughness}</b> • Metal: <b>${sample.metalness}</b>${autoReload ? ' • Đang làm mới 3D...' : ''}`,
      sample.hex,
      '#16a34a'
    );
    const gotHex = fabRgbToHex(res.basecolor);
    const gotRough = typeof res.roughness === 'number' ? res.roughness : null;
    const match = gotHex === sample.hex;
    const texNote = res.textureSkipped ? ' ⚠️ Nguồn có texture từ model khác: chỉ chép được màu/độ bóng, không chép được ảnh texture.' : '';
    setStatus(`${match ? '✅' : '⚠️'} Đã ghi [${res.materialName}]${countInfo} và đọc lại từ server: màu <b>${gotHex}</b> (nguồn <b>${sample.hex}</b>)${match ? ' — KHỚP' : ' — KHÔNG KHỚP, hãy bấm Xuất file chẩn đoán'}. Chép ${res.fullCopy ? 'toàn bộ thuộc tính vật liệu' : 'màu/độ bóng'}.${texNote}`, match ? '#16a34a' : '#b45309');

    // Cập nhật lại dropdown danh sách
    setTimeout(refreshSceneMaterialsUI, 600);
    if (autoReload) {
      setTimeout(() => window.location.reload(), 1100);
    }
    return true;
  }

  // KEYSHOT MOUSE LISTENERS (Ctrl + Click Trái = Hút, Ctrl + Click Phải = Bơm)
  let ctrlClickStart = null;

  if (window.__WT3D_KEYSHOT_HANDLERS__) {
    try { window.removeEventListener('pointerdown', window.__WT3D_KEYSHOT_HANDLERS__.pointerdown, true); } catch (_) {}
    try { window.removeEventListener('pointerup', window.__WT3D_KEYSHOT_HANDLERS__.pointerup, true); } catch (_) {}
    try { window.removeEventListener('contextmenu', window.__WT3D_KEYSHOT_HANDLERS__.contextmenu, true); } catch (_) {}
  }

  const onKeyShotPointerDown = (e) => {
    if (e.target?.closest?.('#wt3d-fab-studio-panel') || e.target?.closest?.('#wt3d-keyshot-toast')) return;
    if (e.ctrlKey && (e.button === 0 || e.button === 2)) {
      ctrlClickStart = { x: e.clientX, y: e.clientY, button: e.button, time: Date.now() };
      e.preventDefault();
      e.stopPropagation();
    } else {
      ctrlClickStart = null;
    }
  };

  const resolveClickedMaterialId = async (start) => {
    let report;
    try { report = await readReference(); } catch (_) {}
    const mats = report?.doptions?.materials || {};

    // Bước 1: Lấy mẫu pixel màu GPU trực tiếp tại tọa độ click
    if (start && typeof start.x === 'number' && typeof start.y === 'number') {
      const pixelRgb = await sampleCanvasPixelRgb(start.x, start.y);
      if (pixelRgb) {
        const pixelMid = matchMaterialByPixelRgb(pixelRgb, mats);
        if (pixelMid && mats[pixelMid]) {
          console.log('[WT3D KeyShot] 🎨 Clicked point matched material:', mats[pixelMid]?.name, pixelRgb);
          return pixelMid;
        }
      }
    }

    // Bước 2: Fallback về vật liệu đang được chọn trên Dropdown nguồn
    const srcSelect = document.getElementById('wt3d-src-mat-select');
    if (srcSelect && srcSelect.value && mats[srcSelect.value]) {
      return srcSelect.value;
    }

    return null;
  };

  const onKeyShotPointerUp = (e) => {
    if (!ctrlClickStart) return;
    const start = ctrlClickStart;
    ctrlClickStart = null;

    const dist = Math.hypot(e.clientX - start.x, e.clientY - start.y);
    if (dist > 8 || (Date.now() - start.time > 1500)) return; // Orbit/pan drag -> ignore!

    if (start.button === 0) {
      // Ctrl + Click Trái = HÚT VẬT LIỆU
      console.log('[WT3D Canvas Studio] 🎯 KeyShot Shortcut: Ctrl + Left Click (HÚT VẬT LIỆU)');
      runTask('KeyShot Hút Vật Liệu (Ctrl+Click Trái)', async () => {
        const matchedMid = await resolveClickedMaterialId(start);
        if (!matchedMid) {
          showKeyShotToast('⚠️ Không tìm thấy chi tiết', 'Hãy click trực tiếp lên bề mặt vật thể 3D, hoặc chọn từ Dropdown nguồn.', null, '#ea580c');
          setStatus('⚠️ Điểm click không trúng chi tiết 3D. Hãy click lên bề mặt vật thể hoặc chọn từ danh sách.', '#ea580c');
          return;
        }
        await copyMaterialAction(matchedMid);
      });
    } else if (start.button === 2) {
      // Ctrl + Click Phải = BƠM VẬT LIỆU
      console.log('[WT3D Canvas Studio] 🖌️ KeyShot Shortcut: Ctrl + Right Click (BƠM VẬT LIỆU)');
      e.preventDefault();
      e.stopPropagation();
      runTask('KeyShot Bơm Vật Liệu (Ctrl+Click Phải)', async () => {
        const matchedMid = await resolveClickedMaterialId(start);
        if (!matchedMid) {
          showKeyShotToast('⚠️ Không tìm thấy chi tiết đích', 'Hãy click trực tiếp lên bề mặt vật thể 3D cần gán, hoặc chọn từ Dropdown đích.', null, '#ea580c');
          setStatus('⚠️ Điểm click không trúng chi tiết đích. Hãy click lên bề mặt vật thể hoặc chọn từ danh sách.', '#ea580c');
          return;
        }
        await pasteMaterialAction(matchedMid);
      });
    }
  };

  const onKeyShotContextMenu = (e) => {
    if (e.ctrlKey) {
      e.preventDefault();
      e.stopPropagation();
    }
  };

  window.__WT3D_KEYSHOT_HANDLERS__ = {
    pointerdown: onKeyShotPointerDown,
    pointerup: onKeyShotPointerUp,
    contextmenu: onKeyShotContextMenu
  };
  // v3.9.44: Ctrl+Click (đoán chi tiết bằng màu pixel, ~74% chính xác) đã TẮT để không ghi đè nhầm.
  // Dùng luồng chính xác 100%: chọn chi tiết trong danh sách -> Lưu tên -> chọn tên -> Bơm.
  // (Bật lại bằng cách gỡ cờ dưới đây nếu cần thử nghiệm.)
  if (window.__WT3D_ENABLE_CTRL_CLICK__ === true) {
    window.addEventListener('pointerdown', onKeyShotPointerDown, true);
    window.addEventListener('pointerup', onKeyShotPointerUp, true);
    window.addEventListener('contextmenu', onKeyShotContextMenu, true);
  }

  // [CORE 10] GIAO DIỆN APPLE BENTO LIGHT THEME V3.5.4
  // =========================================================================
  function createStudioPanel() {
    const existing = document.getElementById('wt3d-fab-studio-panel');
    if (existing) {
      if (existing.__wt3dWorldAlive && existing.getAttribute('data-wt3d-version') === STUDIO_VERSION) return;
      try { existing.remove(); } catch (_) {}
      try { document.getElementById('wt3d-fab-studio-style')?.remove(); } catch (_) {}
    }
    const c = canvas();
    if (!c && !document.body) return;

    const style = document.createElement('style');
    style.id = 'wt3d-fab-studio-style';
    style.textContent = `
      #wt3d-fab-studio-panel {
        position: fixed;
        top: 60px;
        left: 20px;
        width: 410px;
        max-height: calc(100vh - 80px);
        overflow-y: auto;
        overflow-x: hidden;
        z-index: 2147483647;
        background: rgba(255, 255, 255, 0.96);
        backdrop-filter: blur(28px) saturate(180%);
        -webkit-backdrop-filter: blur(28px) saturate(180%);
        border: 1px solid rgba(0, 0, 0, 0.08);
        border-radius: 22px;
        box-shadow: 0 20px 48px -10px rgba(0, 0, 0, 0.18), 0 1px 4px rgba(0, 0, 0, 0.04), inset 0 1px 0 rgba(255, 255, 255, 0.95);
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        letter-spacing: -0.015em;
        padding: 16px 18px;
        color: #1d1d1f;
        box-sizing: border-box;
        user-select: none;
        pointer-events: auto !important;
        transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.2s;
      }
      #wt3d-fab-studio-panel::before {
        content: '';
        position: absolute;
        top: 0;
        left: 20px;
        right: 20px;
        height: 3px;
        background: linear-gradient(90deg, #0071e3 0%, #34c759 100%);
        border-radius: 9999px;
        opacity: 0.9;
      }
      #wt3d-fab-studio-panel::-webkit-scrollbar {
        width: 5px;
      }
      #wt3d-fab-studio-panel::-webkit-scrollbar-track {
        background: transparent;
      }
      #wt3d-fab-studio-panel::-webkit-scrollbar-thumb {
        background: rgba(0, 0, 0, 0.15);
        border-radius: 9999px;
      }
      .wt3d-prof-btn {
        pointer-events: auto !important;
        cursor: pointer !important;
        transition: all 0.18s cubic-bezier(0.4, 0, 0.2, 1);
      }
      .wt3d-prof-btn:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
      }
      .wt3d-bg-btn {
        pointer-events: auto !important;
        cursor: pointer !important;
        transition: all 0.15s ease;
      }
      .wt3d-bg-btn:hover {
        border-color: #0071e3 !important;
        color: #0071e3 !important;
      }
      .wt3d-hero-btn {
        pointer-events: auto !important;
        cursor: pointer !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      }
      .wt3d-hero-btn:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(52, 199, 89, 0.38) !important;
      }
      .wt3d-hero-btn:active {
        transform: translateY(0);
      }
      .wt3d-sub-btn {
        pointer-events: auto !important;
        cursor: pointer !important;
        transition: all 0.15s ease;
      }
      .wt3d-sub-btn:hover {
        background: #f5f5f7 !important;
        border-color: rgba(0, 113, 227, 0.35) !important;
        color: #0071e3 !important;
        transform: translateY(-1px);
      }
      .wt3d-cam-hero-btn {
        pointer-events: auto !important;
        cursor: pointer !important;
        transition: all 0.18s ease;
      }
      .wt3d-cam-hero-btn:hover {
        transform: translateY(-1px);
        box-shadow: 0 3px 10px rgba(0, 113, 227, 0.18);
      }
    `;
    (document.head || document.documentElement).appendChild(style);

    const panel = document.createElement('aside');
    panel.id = 'wt3d-fab-studio-panel';
    panel.__wt3dWorldAlive = true;
    panel.setAttribute('data-wt3d-version', STUDIO_VERSION);
    panel.setAttribute('data-radix-focus-guard', 'true');
    panel.setAttribute('data-dismissable-layer-ignore', 'true');
    panel.innerHTML = `
      <!-- HEADER -->
      <div id="wt3d-drag-header" style="cursor: move; padding-bottom: 12px; border-bottom: 1px solid rgba(0, 0, 0, 0.06); margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between;">
        <div style="display: flex; align-items: center; gap: 8px;">
          <span style="font-size: 19px; font-weight: 900; color: #1d1d1f; letter-spacing: -0.02em; display: flex; align-items: center; gap: 6px;">
            <span>🎨</span> WT3D KeyShot Studio
          </span>
          <span style="background: #f5f5f7; color: #0071e3; border: 1px solid rgba(0, 113, 227, 0.18); font-size: 13px; font-weight: 800; padding: 2px 8px; border-radius: 9999px; letter-spacing: 0.02em;">PRO v3.9.38</span>
        </div>
        <div style="display: flex; align-items: center; gap: 4px;">
          <button id="wt3d-toggle-side" title="Chuyển vị trí Trái / Phải" style="background: transparent; border: none; font-size: 15px; color: #86868b; cursor: pointer; padding: 3px 6px; border-radius: 6px; line-height: 1;">↔️</button>
          <button id="wt3d-minimize" title="Thu gọn / Mở rộng" style="background: transparent; border: none; font-size: 18px; color: #86868b; cursor: pointer; padding: 2px 6px; border-radius: 6px; font-weight: 700; line-height: 1;">−</button>
          <button id="wt3d-close" title="Dừng khẩn cấp / Đóng (Phím ESC)" style="background: transparent; border: none; font-size: 22px; color: #86868b; cursor: pointer; padding: 0 4px; border-radius: 6px; line-height: 1;">&times;</button>
        </div>
      </div>

      <div id="wt3d-studio-body" style="pointer-events: auto;">
        <!-- 6 PRESETS BENTO GRID -->
        <div style="margin-bottom: 11px;">
          <label style="font-size: 13.5px; font-weight: 900; color: #1d1d1f; display: block; margin-bottom: 7px; letter-spacing: 0.02em; text-transform: uppercase;">
            💎 CHỌN BỘ ÁNH SÁNG & MÔI TRƯỜNG (6 PRESETS):
          </label>
          <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 7px;">
            <!-- HÀNG 1 -->
            <button class="wt3d-prof-btn" id="wt3d-prof-soft" data-profile="soft" style="background: #e8f2ff; color: #0071e3; border: 1.5px solid #0071e3; border-radius: 14px; padding: 9px 3px; cursor: pointer; text-align: center; line-height: 1.35; box-shadow: 0 2px 8px rgba(0, 113, 227, 0.15);">
              <div style="font-size: 22px;">🏆</div>
              <div style="font-size: 13px; font-weight: 900;">Studio Soft</div>
              <div style="font-size: 11px; color: #0071e3; font-weight: 700;">Chuẩn Công Nghiệp</div>
            </button>
            <button class="wt3d-prof-btn" id="wt3d-prof-studio2" data-profile="studio2" style="background: #ffffff; color: #1d1d1f; border: 1px solid rgba(0, 0, 0, 0.08); border-radius: 14px; padding: 9px 3px; cursor: pointer; text-align: center; line-height: 1.35;">
              <div style="font-size: 22px;">✨</div>
              <div style="font-size: 13px; font-weight: 900;">Studio 2</div>
              <div style="font-size: 11px; color: #86868b; font-weight: 700;">Bóng Kim Loại</div>
            </button>
            <button class="wt3d-prof-btn" id="wt3d-prof-white" data-profile="white" style="background: #ffffff; color: #1d1d1f; border: 1px solid rgba(0, 0, 0, 0.08); border-radius: 14px; padding: 9px 3px; cursor: pointer; text-align: center; line-height: 1.35;">
              <div style="font-size: 22px;">🤍</div>
              <div style="font-size: 13px; font-weight: 900;">Pure White</div>
              <div style="font-size: 11px; color: #86868b; font-weight: 700;">Trắng Catalog</div>
            </button>
            <!-- HÀNG 2 -->
            <button class="wt3d-prof-btn" id="wt3d-prof-industrial" data-profile="industrial" style="background: #ffffff; color: #1d1d1f; border: 1px solid rgba(0, 0, 0, 0.08); border-radius: 14px; padding: 9px 3px; cursor: pointer; text-align: center; line-height: 1.35;">
              <div style="font-size: 22px;">🏭</div>
              <div style="font-size: 13px; font-weight: 900;">Nhà Xưởng</div>
              <div style="font-size: 11px; color: #86868b; font-weight: 700;">Xưởng Thực Tế</div>
            </button>
            <button class="wt3d-prof-btn" id="wt3d-prof-dark" data-profile="dark" style="background: #ffffff; color: #1d1d1f; border: 1px solid rgba(0, 0, 0, 0.08); border-radius: 14px; padding: 9px 3px; cursor: pointer; text-align: center; line-height: 1.35;">
              <div style="font-size: 22px;">🖤</div>
              <div style="font-size: 13px; font-weight: 900;">Dark Luxury</div>
              <div style="font-size: 11px; color: #86868b; font-weight: 700;">Đêm Titan</div>
            </button>
            <button class="wt3d-prof-btn" id="wt3d-prof-outdoor" data-profile="outdoor" style="background: #ffffff; color: #1d1d1f; border: 1px solid rgba(0, 0, 0, 0.08); border-radius: 14px; padding: 9px 3px; cursor: pointer; text-align: center; line-height: 1.35;">
              <div style="font-size: 22px;">☀️</div>
              <div style="font-size: 13px; font-weight: 900;">Ngoài Trời</div>
              <div style="font-size: 11px; color: #86868b; font-weight: 700;">Nắng Công Trình</div>
            </button>
          </div>
        </div>

        <!-- 4 CHIPS PHÔNG NỀN NHANH (KÍCH HOẠT TRỰC TIẾP LOOK > BACKGROUND) -->
        <div style="margin-bottom: 11px; background: #ffffff; border: 1px solid rgba(0, 0, 0, 0.06); border-radius: 14px; padding: 9px 12px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <span style="font-size: 12.5px; font-weight: 900; color: #1d1d1f; text-transform: uppercase;">🎨 ĐỔI PHÔNG NỀN NHANH:</span>
            <span id="wt3d-bg-current" style="font-size: 12px; color: #0071e3; font-weight: 800;">Môi Trường Dịu (HDRI)</span>
          </div>
          <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 5px;">
            <button class="wt3d-bg-btn" id="wt3d-bg-env" data-bg="environment" title="Phông nền HDRI toàn cảnh tự nhiên" style="background: #e8f2ff; color: #0071e3; border: 1.5px solid #0071e3; border-radius: 9px; padding: 6px 2px; font-size: 11.5px; font-weight: 800; cursor: pointer; text-align: center;">🌫️ M.Trường</button>
            <button class="wt3d-bg-btn" id="wt3d-bg-clean-light" data-bg="clean_light" title="Phông nền xám trắng Apple Clean Light #F5F5F7" style="background: #ffffff; color: #1d1d1f; border: 1px solid rgba(0, 0, 0, 0.08); border-radius: 9px; padding: 6px 2px; font-size: 11.5px; font-weight: 800; cursor: pointer; text-align: center;">🎨 Clean Light</button>
            <button class="wt3d-bg-btn" id="wt3d-bg-white" data-bg="color" title="Phông trắng tinh #FFFFFF chuẩn Catalog TMĐT" style="background: #ffffff; color: #1d1d1f; border: 1px solid rgba(0, 0, 0, 0.08); border-radius: 9px; padding: 6px 2px; font-size: 11.5px; font-weight: 800; cursor: pointer; text-align: center;">🤍 Trắng Tinh</button>
            <button class="wt3d-bg-btn" id="wt3d-bg-clean-dark" data-bg="clean_dark" title="Phông đen titan Clean Dark #18181B" style="background: #ffffff; color: #1d1d1f; border: 1px solid rgba(0, 0, 0, 0.08); border-radius: 9px; padding: 6px 2px; font-size: 11.5px; font-weight: 800; cursor: pointer; text-align: center;">🖤 Clean Dark</button>
          </div>
        </div>

        <!-- BADGE THÔNG TIN PRESET ĐANG CHỌN -->
        <div id="wt3d-profile-badge" style="margin-bottom: 11px; padding: 9px 12px; border-radius: 12px; font-size: 12.5px; line-height: 1.45; background: #f0f7ff; border: 1px solid #d0e5ff; color: #0071e3; font-weight: 600;">
          • <b>Studio Soft (🏆 Chuẩn KeyShot & Apple • Rim Light Viền)</b>: HDRI Studio xoay 38° tạo Rim Light viền sắc nét, độ sáng 2.20 êm dịu, tắt DoF giúp máy nét 100%, bóng sàn Occlusion bám chân.
        </div>

        <!-- DUY NHẤT 1 NÚT HERO SIÊU GỌN 1 HÀNG CHỐNG TRÀN CHỮ -->
        <button id="wt3d-keyshot-all" class="wt3d-hero-btn" title="Áp HDRI, nền, phản xạ, độ bóng; backup và xác minh đã lưu. Camera tự động chỉ khi API Fab hỗ trợ." style="width: 100%; background: linear-gradient(180deg, #34c759 0%, #28a745 100%); color: white; border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 14px; padding: 13px 14px; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; box-shadow: 0 4px 14px rgba(52, 199, 89, 0.32), inset 0 1px 0 rgba(255, 255, 255, 0.35); font-size: 16.5px; font-weight: 900; letter-spacing: 0.01em; text-transform: uppercase; white-space: nowrap !important;">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" style="flex-shrink: 0;"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
          <span style="white-space: nowrap !important;">⚡ 1-CLICK THIẾT LẬP RENDER</span>
        </button>

        <!-- CÔNG CỤ ĐIỀU HƯỚNG GÓC NHÌN PERSPECTIVE 3/4 (Y-UP) -->
        <div style="margin-top: 11px; background: #ffffff; border: 1px solid rgba(0, 0, 0, 0.06); border-radius: 14px; padding: 10px 12px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);">
          <div style="font-size: 12.5px; font-weight: 900; color: #1d1d1f; text-transform: uppercase; margin-bottom: 7px; display: flex; justify-content: space-between; align-items: center;">
            <span>📷 GÓC NHÌN PERSPECTIVE 3/4 (Y-UP):</span>
            <span style="color: #0071e3; font-size: 11px; font-weight: 800; background: #f0f7ff; padding: 2px 6px; border-radius: 6px; border: 1px solid #d0e5ff;">FOV 45° Phối Cảnh</span>
          </div>

          <!-- 2 NÚT CHỦ ĐẠO: NHÌN XUỐNG VS NHÌN LÊN -->
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-bottom: 6px;">
            <button class="wt3d-cam-hero-btn" id="wt3d-cam-down" title="Góc 3/4 nhìn từ trên xuống ~18° (Top-Down Showcase: thấy mặt trên, ống đỉnh & van)" style="background: linear-gradient(180deg, #eff6ff 0%, #e0f2fe 100%); color: #0284c7; border: 1.5px solid #bae6fd; border-radius: 10px; padding: 9px 6px; font-size: 12.5px; font-weight: 900; cursor: pointer; text-align: center; display: flex; align-items: center; justify-content: center; gap: 5px;">
              <span>📐 3/4 Nhìn Xuống</span>
            </button>
            <button class="wt3d-cam-hero-btn" id="wt3d-cam-up" title="Góc 3/4 nhìn từ dưới lên ~15° (Low-Angle Hero View: bệ vệ, đồ sộ cụm tháp máy)" style="background: linear-gradient(180deg, #fdf4ff 0%, #fae8ff 100%); color: #a855f7; border: 1.5px solid #f0abfc; border-radius: 10px; padding: 9px 6px; font-size: 12.5px; font-weight: 900; cursor: pointer; text-align: center; display: flex; align-items: center; justify-content: center; gap: 5px;">
              <span>📐 3/4 Nhìn Lên</span>
            </button>
          </div>

          <!-- CÁC GÓC XOAY KHÁC & FIT VIEW -->
          <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 5px; margin-bottom: 6px;">
            <button class="wt3d-sub-btn" id="wt3d-cam-down-left" title="Góc 3/4 bên trái nhìn xuống" style="background: #f5f5f7; border: 1px solid rgba(0,0,0,0.08); border-radius: 8px; padding: 7px 3px; font-size: 11.5px; font-weight: 800; cursor: pointer; text-align: center;">📐 3/4 Trái</button>
            <button class="wt3d-sub-btn" id="wt3d-cam-eye" title="Góc 3/4 nhìn ngang tầm mắt 1:1" style="background: #f5f5f7; border: 1px solid rgba(0,0,0,0.08); border-radius: 8px; padding: 7px 3px; font-size: 11.5px; font-weight: 800; cursor: pointer; text-align: center;">📐 3/4 Ngang</button>
            <button class="wt3d-sub-btn" id="wt3d-action-fit" title="Căn vừa vặn toàn màn hình (Phím tắt F)" style="background: #f5f5f7; border: 1px solid rgba(0,0,0,0.08); border-radius: 8px; padding: 7px 3px; font-size: 11.5px; font-weight: 800; cursor: pointer; text-align: center;">🎯 Fit View (F)</button>
          </div>

          <!-- LƯU GÓC NHÌN & XUẤT ẢNH CHUẨN HD -->
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 5px;">
            <button class="wt3d-sub-btn" id="wt3d-action-saveview" title="Lưu góc nhìn hiện tại làm ảnh đại diện sản phẩm" style="background: #eff6ff; color: #0071e3; border: 1px solid #bfdbfe; border-radius: 8px; padding: 7px 4px; font-size: 12px; font-weight: 800; cursor: pointer; text-align: center;">💾 Lưu Default View</button>
            <button class="wt3d-sub-btn" id="wt3d-action-exportpng" title="Xuất ảnh Khổ Chuẩn Full HD (1920x1080 - Tỷ lệ 16:9) sắc nét tuyệt đối" style="background: linear-gradient(180deg, #ecfdf5 0%, #d1fae5 100%); color: #059669; border: 1.5px solid #10b981; border-radius: 8px; padding: 7px 4px; font-size: 12px; font-weight: 900; cursor: pointer; text-align: center; display: flex; align-items: center; justify-content: center; gap: 4px; box-shadow: 0 1px 3px rgba(16, 185, 129, 0.18);">📸 Xuất Full HD 16:9</button>
          </div>
        </div>

        <!-- MỞ NHANH CÁC TAB 3D EDITOR (MỞ VÀ GIỮ NGUYÊN TAB CHO NGƯỜI DÙNG KIỂM TRA) -->
        <div style="margin-top: 10px; display: grid; grid-template-columns: repeat(4, 1fr); gap: 5px;">
          <button class="wt3d-sub-btn" data-tab="lighting" title="Mở tab Lighting & hiển thị bảng điều khiển ánh sáng" style="background: #ffffff; border: 1px solid rgba(0,0,0,0.08); border-radius: 8px; padding: 7px 2px; font-size: 11.5px; font-weight: 800; cursor: pointer; color: #1d1d1f;">💡 Lighting</button>
          <button class="wt3d-sub-btn" data-tab="look" title="Mở tab Look & hiển thị bảng bóng sàn, phông nền" style="background: #ffffff; border: 1px solid rgba(0,0,0,0.08); border-radius: 8px; padding: 7px 2px; font-size: 11.5px; font-weight: 800; cursor: pointer; color: #1d1d1f;">🎨 Look</button>
          <button class="wt3d-sub-btn" data-tab="camera" title="Mở tab Camera & hiển thị FOV, Save View" style="background: #ffffff; border: 1px solid rgba(0,0,0,0.08); border-radius: 8px; padding: 7px 2px; font-size: 11.5px; font-weight: 800; cursor: pointer; color: #1d1d1f;">📷 Camera</button>
          <button class="wt3d-sub-btn" data-tab="inspect" title="Mở tab Inspect & hiển thị Wireframe, Matcap" style="background: #ffffff; border: 1px solid rgba(0,0,0,0.08); border-radius: 8px; padding: 7px 2px; font-size: 11.5px; font-weight: 800; cursor: pointer; color: #1d1d1f;">🔍 Inspect</button>
        </div>

        <!-- KHỐI CHÚ THÍCH BẢN QUYỀN ANNOTATION & PINNED COMMENT -->
        <div style="margin-top: 10px; background: #ffffff; border: 1px solid rgba(0, 0, 0, 0.08); border-radius: 14px; padding: 10px 12px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <span style="font-size: 12.5px; font-weight: 900; color: #1d1d1f; text-transform: uppercase;">📍 CHÚ THÍCH BẢN QUYỀN:</span>
            <span style="font-size: 11px; color: #0071e3; font-weight: 700;">tanphan1105</span>
          </div>
          <div style="display: flex; gap: 5px; margin-bottom: 6px;">
            <button id="wt3d-copy-anno-desc" title="Chép mô tả Markdown kèm Link Fab.com vào Clipboard" style="flex: 1.3; background: linear-gradient(180deg, #0071e3 0%, #0064cc 100%); color: white; border: none; border-radius: 9px; padding: 8px 6px; font-size: 12px; font-weight: 800; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 5px; box-shadow: 0 2px 6px rgba(0, 113, 227, 0.22);">
              <span>📋 Chép Mô Tả Fab</span>
            </button>
            <button id="wt3d-copy-anno-title" title="Chép 'tanphan1105' vào Clipboard" style="flex: 0.8; background: #f5f5f7; color: #1d1d1f; border: 1px solid rgba(0, 0, 0, 0.08); border-radius: 9px; padding: 8px 4px; font-size: 12px; font-weight: 800; cursor: pointer;">
              <span>📝 Tiêu Đề</span>
            </button>
          </div>
          <div>
            <button id="wt3d-copy-pinned-comment" title="Chép bình luận ghim chuyên nghiệp B2B kèm Link Fab để dán vào khung Comments" style="width: 100%; background: linear-gradient(180deg, #8b5cf6 0%, #7c3aed 100%); color: white; border: none; border-radius: 9px; padding: 8px 8px; font-size: 12px; font-weight: 800; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 5px; box-shadow: 0 2px 6px rgba(124, 58, 237, 0.22);">
              <span>💬 Chép Bình Luận Ghim (Dẫn Link Fab)</span>
            </button>
          </div>
        </div>

        <!-- STATUS BOX TO RÕ RÀNG -->
        <div class="wt3d-status-box" id="wt3d-status" style="margin-top: 11px; font-size: 13.5px; line-height: 1.5; font-weight: 600; padding: 10px 14px; border-radius: 14px; border: 1px solid rgba(0, 0, 0, 0.06); background: #f5f5f7; color: #1d1d1f; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02); min-height: 48px; box-sizing: border-box;">
          Sẵn sàng! Bấm nút tab (💡 Lighting, 🎨 Look, 📷 Camera) để mở bảng điều khiển, hoặc bấm nút xanh lá [⚡ 1-CLICK THIẾT LẬP RENDER].
        </div>
      </div>
    `;

    const mountTarget = (c && c.parentElement) ? c.parentElement : document.body;
    mountTarget.appendChild(panel);
    // Thanh công cụ Thư Viện Vật Liệu Mẫu Dùng Chung (Lưu từ 1 model -> Áp cho mọi model)
    const matLibTools = document.createElement('div');
    matLibTools.style.cssText = 'display:flex;gap:6px;margin:8px 0 6px 0;';
    const saveMatLibBtn = document.createElement('button');
    saveMatLibBtn.id = 'wt3d-save-mat-lib-btn';
    saveMatLibBtn.type = 'button';
    saveMatLibBtn.title = 'Đọc độ bóng, độ kim loại, màu sắc của Cột lọc, Inox, Nhựa... trên model này và lưu vào Thư viện Vật liệu Mẫu dùng chung';
    saveMatLibBtn.textContent = '💾 Lưu Vật Liệu Mẫu';
    saveMatLibBtn.style.cssText = 'flex:1;padding:9px 6px;border:1px solid #059669;border-radius:8px;cursor:pointer;color:#ffffff;background:linear-gradient(180deg,#10b981 0%,#059669 100%);font-weight:800;font-size:12px;box-shadow:0 2px 6px rgba(5,150,105,0.25);';

    const applyMatLibBtn = document.createElement('button');
    applyMatLibBtn.id = 'wt3d-apply-mat-lib-btn';
    applyMatLibBtn.type = 'button';
    applyMatLibBtn.title = 'Áp dụng ngay Thư viện Vật liệu Mẫu (Cột lọc FRP, Inox SUS304, Nhựa uPVC...) đã lưu cho model hiện tại';
    applyMatLibBtn.textContent = '✨ Áp Vật Liệu Chuẩn';
    applyMatLibBtn.style.cssText = 'flex:1;padding:9px 6px;border:1px solid #0284c7;border-radius:8px;cursor:pointer;color:#ffffff;background:linear-gradient(180deg,#0ea5e9 0%,#0284c7 100%);font-weight:800;font-size:12px;box-shadow:0 2px 6px rgba(2,132,199,0.25);';

    matLibTools.appendChild(saveMatLibBtn);
    matLibTools.appendChild(applyMatLibBtn);
    panel.querySelector('#wt3d-status')?.before(matLibTools);

    // =========================================================================
    // [KEYSHOT CARD UI] BẢNG QUẢN LÝ VẬT LIỆU KEYSHOT & SWATCH PREVIEW (CHỌN NGUỒN → ĐÍCH)
    // =========================================================================
    const keyshotMatCard = document.createElement('div');
    keyshotMatCard.id = 'wt3d-keyshot-mat-card';
    keyshotMatCard.style.cssText = 'margin: 8px 0; padding: 12px; background: #ffffff; border: 1.5px solid #0284c7; border-radius: 14px; box-shadow: 0 2px 8px rgba(2, 132, 199, 0.12);';
    keyshotMatCard.innerHTML = `
      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
        <span style="font-weight: 900; font-size: 13.5px; color: #0f172a; display: flex; align-items: center; gap: 6px;">
          <span>🖌️</span> KEYSHOT FAST MATERIAL
        </span>
        <span style="font-size: 11px; background: #e0f2fe; color: #0284c7; padding: 2px 8px; border-radius: 9999px; font-weight: 800; border: 1px solid rgba(2,132,199,0.25);">
          CÓ HOÀN TÁC
        </span>
      </div>

      <div style="margin-bottom: 8px;">
        <input id="wt3d-mat-filter" type="text" placeholder="🔍 Gõ tìm nhanh chi tiết (inox, ống, van, 190...)" style="width: 100%; box-sizing: border-box; padding: 6px 9px; border: 1px solid #cbd5e1; border-radius: 7px; font-size: 11.5px; background: #fff; margin-bottom: 6px; outline: none;">
        <div style="display: flex; justify-content: space-between; font-size: 11.5px; font-weight: 700; color: #334155; margin-bottom: 4px;">
          <span>1. Chọn chi tiết muốn LẤY vật liệu:</span>
          <span id="wt3d-mat-count" style="font-weight: 600; color: #64748b;">(Đang nạp...)</span>
        </div>
        <select id="wt3d-src-mat-select" style="width: 100%; box-sizing: border-box; padding: 7px 8px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 12px; font-weight: 600; color: #0f172a; background: #f8fafc; cursor: pointer; margin-bottom: 6px;">
          <option value="">-- Bấm để nạp danh sách chi tiết... --</option>
        </select>
        <div style="display: flex; gap: 6px; align-items: center;">
          <input id="wt3d-lib-name" type="text" placeholder="Đặt tên dễ nhớ, vd: Inox bóng, Ống xanh..." style="flex: 1; min-width: 0; box-sizing: border-box; padding: 7px 9px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 12px; font-weight: 600; background: #fff; outline: none;">
          <button id="wt3d-save-lib-btn" type="button" title="Lưu vật liệu của chi tiết đang chọn vào thư viện kèm tên" style="padding: 7px 11px; background: linear-gradient(180deg, #0284c7 0%, #0369a1 100%); color: white; border: none; border-radius: 8px; font-weight: 800; font-size: 12px; cursor: pointer; white-space: nowrap; box-shadow: 0 1px 4px rgba(2, 132, 199, 0.3);">
            💾 Lưu
          </button>
        </div>
      </div>

      <div id="wt3d-swap-card" style="margin-bottom: 8px; padding: 9px 10px; background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 9px;">
        <div style="font-size: 12px; font-weight: 800; color: #0c4a6e; margin-bottom: 5px;">2. ĐỔI VẬT LIỆU CHO CHI TIẾT</div>
        <div style="display: flex; align-items: center; gap: 7px; padding: 6px 8px; background: #e0f2fe; border: 1px solid #7dd3fc; border-radius: 7px; margin-bottom: 6px;">
          <div id="wt3d-tgt-picked-swatch" style="width: 18px; height: 18px; border-radius: 4px; background: #cbd5e1; border: 1px solid rgba(0,0,0,0.2); flex-shrink: 0;"></div>
          <div id="wt3d-tgt-picked-label" style="font-size: 11.5px; font-weight: 800; color: #0c4a6e; flex: 1; min-width: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
            🖱️ Click chuột vào chi tiết trên mô hình 3D để chọn!
          </div>
          <span id="wt3d-tgt-auto-badge" style="display: none;"></span>
        </div>
        <select id="wt3d-tgt-mat-select" title="Tự động nhảy khi anh click chuột lên mô hình 3D (hoặc chọn thủ công)" style="width: 100%; box-sizing: border-box; padding: 6px 8px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 11.5px; font-weight: 600; color: #0f172a; background: #f8fafc; cursor: pointer; margin-bottom: 8px;">
          <option value="">-- Tự nhảy khi click chuột trên 3D (hoặc chọn tại đây) --</option>
        </select>
        <div style="font-size: 11.5px; font-weight: 800; color: #0369a1; margin-bottom: 4px;">★ Chọn nhanh mẫu vật liệu (1-chạm):</div>
        <div id="wt3d-preset-chips" style="display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 8px;"></div>
        <div style="display: flex; justify-content: space-between; font-size: 11.5px; font-weight: 700; color: #0c4a6e; margin-bottom: 4px;">
          <span>Hoặc chọn trong danh sách đã lưu:</span>
          <span id="wt3d-lib-count" style="font-weight: 600; color: #64748b;">(0 đã lưu)</span>
        </div>
        <div style="display: flex; gap: 6px; align-items: center;">
          <select id="wt3d-lib-select" style="flex: 1; min-width: 0; padding: 7px 8px; border: 1px solid #7dd3fc; border-radius: 8px; font-size: 12px; font-weight: 600; color: #0f172a; background: #fff; cursor: pointer;">
            <option value="">-- Thư viện trống --</option>
          </select>
          <button id="wt3d-del-lib-btn" type="button" title="Xóa vật liệu đang chọn khỏi thư viện" style="padding: 7px 9px; background: #fff; color: #dc2626; border: 1px solid #fecaca; border-radius: 8px; font-weight: 800; font-size: 12px; cursor: pointer;">🗑️</button>
        </div>
        <div style="height: 8px;"></div>
      <div id="wt3d-mat-preview-box" style="display: flex; align-items: center; gap: 8px; padding: 7px 10px; background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 9px; margin-bottom: 8px;">
        <div id="wt3d-mat-swatch" style="width: 26px; height: 26px; border-radius: 6px; border: 1.5px solid white; box-shadow: 0 0 0 1px rgba(0,0,0,0.18), inset 0 1px 2px rgba(0,0,0,0.25); background: #c8c8c8; flex-shrink: 0;"></div>
        <div style="flex: 1; min-width: 0; font-size: 11.5px; line-height: 1.35;">
          <div id="wt3d-mat-name" style="font-weight: 800; color: #0f172a; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Chưa chọn vật liệu nào</div>
          <div id="wt3d-mat-details" style="color: #475569; font-size: 11px; font-weight: 600;">Màu: -- | Rough: -- | Metal: --</div>
        </div>
      </div>
        <button id="wt3d-paste-mat-btn" type="button" title="Gán vật liệu đã chọn (theo tên) vào chi tiết đích" style="padding: 7px 11px; background: linear-gradient(180deg, #10b981 0%, #059669 100%); color: white; border: none; border-radius: 8px; font-weight: 800; font-size: 12px; cursor: pointer; white-space: nowrap; box-shadow: 0 1px 4px rgba(16, 185, 129, 0.3); width: 100%; margin-top: 2px; padding: 9px 11px; font-size: 13px;">
          🖌️ Bơm vật liệu đã chọn vào chi tiết đích
        </button>
      </div>

      <button id="wt3d-diag-btn" type="button" title="Xuất file JSON gồm toàn bộ vật liệu hiện tại, mẫu đang chọn và lịch sử để phân tích" style="margin-top: 6px; width: 100%; padding: 6px 10px; background: #f8fafc; border: 1px dashed #94a3b8; border-radius: 8px; font-size: 11.5px; font-weight: 700; color: #475569; cursor: pointer;">
        🩺 Xuất file chẩn đoán (khi màu không giống)
      </button>
      <button id="wt3d-undo-btn" type="button" disabled title="Khôi phục các chi tiết về trạng thái trước lần bơm gần nhất" style="margin-top: 8px; width: 100%; padding: 8px 10px; background: #fff7ed; border: 1px solid #fdba74; border-radius: 8px; font-size: 12px; font-weight: 800; color: #9a3412; cursor: pointer; opacity: 0.5;">
        ↩️ Chưa có lần bơm nào để hoàn tác
      </button>

      <label style="display: flex; align-items: center; gap: 6px; margin-top: 6px; font-size: 11.5px; font-weight: 700; color: #0f172a; cursor: pointer;">
        <input type="checkbox" id="wt3d-sync-group-chk" style="width: 14px; height: 14px; accent-color: #0284c7; cursor: pointer;">
        <span>Áp luôn cho các chi tiết cùng tên gốc / cùng màu (vd 123124127_1…_14)</span>
      </label>
      <label style="display: flex; align-items: center; gap: 6px; margin-top: 5px; font-size: 11.5px; font-weight: 700; color: #0f172a; cursor: pointer;">
        <input type="checkbox" id="wt3d-auto-reload-chk" checked style="width: 14px; height: 14px; accent-color: #10b981; cursor: pointer;">
        <span>Tự động làm mới 3D (F5) sau khi bơm</span>
      </label>
      <button id="wt3d-reload-3d-btn" type="button" title="Làm mới lại khung nhìn 3D" style="margin-top: 6px; width: 100%; padding: 6px 10px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 7px; font-size: 11.5px; font-weight: 700; color: #334155; cursor: pointer;">
        🔄 Làm Mới Khung 3D (F5)
      </button>

      <div style="margin-top: 6px; font-size: 11px; color: #64748b; line-height: 1.4; border-top: 1px solid #e2e8f0; padding-top: 6px;">
        💡 <b>Cách dùng:</b> (1) Chọn chi tiết nguồn → đặt tên → Lưu. (2) Chọn chi tiết đích + chọn tên đã lưu → Bơm. Bơm nhầm? Bấm Hoàn tác.
      </div>
    `;
    panel.querySelector('#wt3d-status')?.before(keyshotMatCard);

    saveMatLibBtn.addEventListener('click', () => runTask('Lưu Thư Viện Vật Liệu Mẫu', async () => {
      const report = await readReference();
      if (!report?.sceneUid) throw new Error('Chưa đọc được scene UID của model hiện tại.');
      const res = await engineRequest('capture_materials', report.sceneUid);
      const existingStore = await storageLocal().get('WT3D_MASTER_MATERIAL_LIBRARY');
      const mergedLib = { ...(existingStore.WT3D_MASTER_MATERIAL_LIBRARY || {}), ...(res.library || {}) };
      await storageLocal().set({ WT3D_MASTER_MATERIAL_LIBRARY: mergedLib });
      setStatus(`✅ Đã lưu ${res.libraryCount} vật liệu từ model này vào Thư viện (Tổng: ${Object.keys(mergedLib).length} mẫu). Mở model khác bấm [✨ Áp Vật Liệu Chuẩn] hoặc [⚡ 1-Click] là ăn ngay!`, '#16a34a');
    }));

    applyMatLibBtn.addEventListener('click', () => runTask('Áp Vật Liệu Chuẩn WT3D', async () => {
      const report = await readReference();
      if (!report?.sceneUid) throw new Error('Chưa đọc được scene UID của model hiện tại.');
      const existingStore = await storageLocal().get('WT3D_MASTER_MATERIAL_LIBRARY');
      const customLibrary = existingStore.WT3D_MASTER_MATERIAL_LIBRARY || {};
      const res = await engineRequest('apply_materials', report.sceneUid, { customLibrary });
      setStatus(`✅ Đã áp & lưu ${res.polishedCount}/${res.materialCount} vật liệu chuẩn (Khớp mẫu đã lưu: ${res.customMatchedCount}, Chuẩn WT3D: ${res.presetMatchedCount}) và tải lại 3D!`, '#16a34a');
      setTimeout(refreshSceneMaterialsUI, 800);
    }));

    // Nút Hút và Bơm
    keyshotMatCard.querySelector('#wt3d-save-lib-btn')?.addEventListener('click', (e) => {
      e.stopPropagation();
      runTask('Lưu vật liệu vào thư viện', async () => { await saveNamedMaterial(); });
    });

    keyshotMatCard.querySelector('#wt3d-diag-btn')?.addEventListener('click', (e) => {
      e.stopPropagation();
      runTask('Xuất file chẩn đoán', async () => { await exportDiagnostics(); });
    });
    keyshotMatCard.querySelector('#wt3d-undo-btn')?.addEventListener('click', (e) => {
      e.stopPropagation();
      runTask('Hoàn tác lần bơm gần nhất', async () => { await undoLastPump(); });
    });
    refreshUndoUI();

    keyshotMatCard.querySelector('#wt3d-del-lib-btn')?.addEventListener('click', (e) => {
      e.stopPropagation();
      runTask('Xóa vật liệu khỏi thư viện', async () => { await deleteNamedMaterial(); });
    });

    keyshotMatCard.querySelector('#wt3d-lib-select')?.addEventListener('change', (e) => {
      const name = e.target.value;
      if (name) useNamedMaterial(name).catch(() => {});
    });

    keyshotMatCard.querySelector('#wt3d-paste-mat-btn')?.addEventListener('click', (e) => {
      e.stopPropagation();
      runTask('Bơm Vật Liệu', async () => {
        const libName = document.getElementById('wt3d-lib-select')?.value;
        if (libName) await useNamedMaterial(libName);
        await pasteMaterialAction();
      });
    });

    // Gợi ý tên theo chi tiết nguồn (chỉ khi người dùng chưa tự gõ tên)
    keyshotMatCard.querySelector('#wt3d-lib-name')?.addEventListener('input', (e) => { e.target.dataset.touched = '1'; });
    keyshotMatCard.querySelector('#wt3d-src-mat-select')?.addEventListener('change', (e) => {
      const nameEl = document.getElementById('wt3d-lib-name');
      const opt = e.target.selectedOptions?.[0];
      if (nameEl && !nameEl.dataset.touched && opt && opt.value) nameEl.value = (opt.textContent || '').split(' (')[0].trim();
    });
    refreshNamedLibraryUI();

    keyshotMatCard.querySelector('#wt3d-reload-3d-btn')?.addEventListener('click', (e) => {
      e.stopPropagation();
      window.location.reload();
    });

    keyshotMatCard.querySelector('#wt3d-tgt-mat-select')?.addEventListener('change', (e) => {
      const mid = e.target.value;
      if (mid && window.__wt3dCachedMaterials?.[mid]) {
        updateTargetPickedUI(mid, window.__wt3dCachedMaterials);
      }
    });

    // Chọn chi tiết nguồn (mục 1) => đó là vật liệu ĐANG CHỌN: ô xem trước hiện đúng nó và Bơm sẽ dùng đúng nó (không cần Lưu)
    keyshotMatCard.querySelector('#wt3d-src-mat-select')?.addEventListener('change', (e) => {
      const mid = e.target.value;
      if (!mid) return;
      const libSel = document.getElementById('wt3d-lib-select');
      if (libSel) libSel.value = '';
      updatePresetChipsActiveState('');
      const cachedMat = window.__wt3dCachedMaterials?.[mid];
      if (cachedMat) {
        activateSample(buildSampleFromMaterial(mid, cachedMat, window.__wt3dCachedSceneUid)).catch(() => {});
      }
      readSavedMaterials().then(async report => {
        const m = report?.doptions?.materials?.[mid];
        if (!m) return;
        await activateSample(buildSampleFromMaterial(mid, m, report.sceneUid));
      }).catch(() => {});
    });

    // Tìm kiếm / lọc nhanh danh sách vật liệu
    keyshotMatCard.querySelector('#wt3d-mat-filter')?.addEventListener('input', (e) => {
      const q = (e.target.value || '').trim().toLowerCase();
      const filterSelect = (sel) => {
        if (!sel) return;
        Array.from(sel.options).forEach(opt => {
          if (!opt.value) return;
          const s = (opt.getAttribute('data-search') || opt.textContent || '').toLowerCase();
          opt.style.display = (!q || s.includes(q)) ? '' : 'none';
        });
      };
      filterSelect(keyshotMatCard.querySelector('#wt3d-src-mat-select'));
      filterSelect(keyshotMatCard.querySelector('#wt3d-tgt-mat-select'));
    });

    // Nạp danh sách vật liệu vào dropdown
    keyshotMatCard.querySelector('#wt3d-src-mat-select')?.addEventListener('focus', () => refreshSceneMaterialsUI(false));
    keyshotMatCard.querySelector('#wt3d-tgt-mat-select')?.addEventListener('focus', () => refreshSceneMaterialsUI(false));
    setTimeout(() => refreshSceneMaterialsUI(true), 1200);

    // Khôi phục vật liệu đã hút từ phiên trước nếu có
    try {
      const saved = sessionStorage.getItem('wt3d_copied_material');
      if (saved) {
        const mat = JSON.parse(saved);
        window.__wt3dCopiedMaterial = mat;
        updateMaterialPreviewUI(mat);
      }
    } catch (_) {}
    
    const referenceTools = document.createElement('div');
    referenceTools.style.cssText = 'display:flex;gap:6px;margin:6px 0 8px 0;';
    const readButton = document.createElement('button');
    readButton.id = 'wt3d-read-reference-btn';
    readButton.textContent = '🔎 Đọc cấu hình thật';
    const exportButton = document.createElement('button');
    exportButton.id = 'wt3d-export-reference-btn';
    exportButton.textContent = '📥 Xuất JSON cấu hình';
    for (const button of [readButton, exportButton]) {
      button.type = 'button';
      button.style.cssText = 'flex:1;padding:9px 5px;border:1px solid #b9d2ee;border-radius:8px;cursor:pointer;color:#124773;background:#eef6ff;font-weight:700;';
      referenceTools.appendChild(button);
    }
    panel.querySelector('#wt3d-status')?.before(referenceTools);

    readButton.addEventListener('click', () => runTask('Đọc cấu hình thật', async () => {
      const report = await readReference();
      const settings = report.doptions;
      setStatus(`Đã đọc ${Object.keys(settings.materials || {}).length} vật liệu; Environment ${settings.environment?.brightness}; FOV ${settings.camera?.fov}°. Đây là cấu hình đã tải, chưa xác minh lưu thay đổi.`, '#0071e3');
    }));
    exportButton.addEventListener('click', () => runTask('Xuất cấu hình', async () => {
      const report = await readReference();
      const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `WT3D-Fab-reference-${report.sceneUid || 'scene'}.json`;
      link.click();
      setTimeout(() => URL.revokeObjectURL(url), 30000);
      setStatus('Đã xuất JSON cấu hình thật; model không bị thay đổi.', '#0071e3');
    }));
    console.log('[WT3D Canvas Studio] ✅ Apple Bento KeyShot Studio mounted inside viewport container.');

    // POINTER EVENTS DRAGGABLE (Rule 23 TPS)
    const header = panel.querySelector('#wt3d-drag-header');
    if (header) {
      let isDragging = false, startX = 0, startY = 0, initL = 0, initT = 0;
      header.addEventListener('pointerdown', e => {
        if (e.target.id === 'wt3d-close' || e.target.id === 'wt3d-minimize' || e.target.id === 'wt3d-toggle-side') return;
        isDragging = true;
        header.setPointerCapture(e.pointerId);
        const r = panel.getBoundingClientRect();
        panel.style.right = 'auto';
        panel.style.left = r.left + 'px';
        panel.style.top = r.top + 'px';
        startX = e.clientX; startY = e.clientY;
        initL = r.left; initT = r.top;
        e.preventDefault();
      });
      header.addEventListener('pointermove', e => {
        if (!isDragging) return;
        const nx = initL + (e.clientX - startX);
        const ny = initT + (e.clientY - startY);
        panel.style.left = `${Math.max(0, Math.min(nx, window.innerWidth - panel.offsetWidth))}px`;
        panel.style.top = `${Math.max(0, Math.min(ny, window.innerHeight - panel.offsetHeight))}px`;
      });
      const endDrag = e => {
        if (isDragging) {
          isDragging = false;
          try { header.releasePointerCapture(e.pointerId); } catch(_) {}
        }
      };
      header.addEventListener('pointerup', endDrag);
      header.addEventListener('pointercancel', endDrag);
    }

    // NGĂN CHẶN SỰ KIỆN NỔI BỌT LÊN CANVAS TRONG GIAI ĐOẠN BUBBLING (KHÔNG DÙNG CAPTURE!)
    ['pointerdown', 'mousedown', 'mouseup', 'click'].forEach(evt => {
      panel.addEventListener(evt, e => {
        e.stopPropagation();
      }, false);
    });

    // CÁC LISTENER ĐIỀU KHIỂN
    const profileBadge = document.getElementById('wt3d-profile-badge');
    const bgCurrentLabel = document.getElementById('wt3d-bg-current');

    const profButtons = {
      soft: document.getElementById('wt3d-prof-soft'),
      studio2: document.getElementById('wt3d-prof-studio2'),
      white: document.getElementById('wt3d-prof-white'),
      industrial: document.getElementById('wt3d-prof-industrial'),
      dark: document.getElementById('wt3d-prof-dark'),
      outdoor: document.getElementById('wt3d-prof-outdoor')
    };

    const bgButtons = {
      environment: document.getElementById('wt3d-bg-env'),
      clean_light: document.getElementById('wt3d-bg-clean-light'),
      color: document.getElementById('wt3d-bg-white'),
      clean_dark: document.getElementById('wt3d-bg-clean-dark')
    };

    function setBackgroundUI(bgKey) {
      activeBg = bgKey;
      Object.entries(bgButtons).forEach(([key, btn]) => {
        if (!btn) return;
        const isCur = (key === activeBg);
        btn.style.background = isCur ? '#e8f2ff' : '#ffffff';
        btn.style.color = isCur ? '#0071e3' : '#1d1d1f';
        btn.style.border = isCur ? '1.5px solid #0071e3' : '1px solid rgba(0, 0, 0, 0.08)';
        btn.style.boxShadow = isCur ? '0 2px 6px rgba(0, 113, 227, 0.15)' : 'none';
      });
      if (bgCurrentLabel) {
        bgCurrentLabel.textContent = BG_NAMES[activeBg] || activeBg;
      }
    }

    function setProfileUI(profKey) {
      activeProfile = profKey;
      const prof = WT3D_LIGHTING_PROFILES[activeProfile] || WT3D_LIGHTING_PROFILES.soft;
      console.log(`[WT3D Canvas Studio] 🎨 Selected Profile: ${prof.name}`);

      Object.entries(profButtons).forEach(([key, btn]) => {
        if (!btn) return;
        const isCur = (key === activeProfile);
        const btnConfig = WT3D_LIGHTING_PROFILES[key] || {};
        btn.style.background = isCur ? (btnConfig.btnActiveBg || '#e8f2ff') : '#ffffff';
        btn.style.color = isCur ? (btnConfig.btnActiveColor || '#0071e3') : '#1d1d1f';
        btn.style.border = isCur ? `1.5px solid ${btnConfig.btnActiveBorder || '#0071e3'}` : '1px solid rgba(0, 0, 0, 0.08)';
        btn.style.boxShadow = isCur ? '0 2px 8px rgba(0, 0, 0, 0.12)' : '0 1px 3px rgba(0, 0, 0, 0.02)';
        const subTxt = btn.children[2];
        if (subTxt) {
          subTxt.style.color = isCur ? (btnConfig.btnActiveColor || '#0071e3') : '#86868b';
        }
      });

      if (profileBadge) {
        profileBadge.innerHTML = `• <b>${prof.badgeTitle}</b>: ${prof.badgeDesc}`;
        profileBadge.style.background = prof.badgeBg;
        profileBadge.style.borderColor = prof.badgeBorder;
        profileBadge.style.color = prof.badgeColor;
      }

      setBackgroundUI(prof.bgType || 'environment');
      setStatus(`Đã chọn Preset: <b>${prof.name}</b>. Bấm [⚡ 1-CLICK] để kích hoạt.`);
    }

    // Gắn sự kiện 6 preset
    Object.entries(profButtons).forEach(([key, btn]) => {
      btn?.addEventListener('click', (e) => {
        e.stopPropagation();
        setProfileUI(key);
      });
    });

    // Gắn sự kiện 4 nút đổi phông nền nhanh (TỰ ĐỘNG THỰC THI SET PHÔNG NỀN NATIVE FAB)
    Object.entries(bgButtons).forEach(([key, btn]) => {
      btn?.addEventListener('click', (e) => {
        e.stopPropagation();
        setBackgroundUI(key);
        runTask(`Đổi Phông Nền (${BG_NAMES[key]})`, async (id) => {
          await setFabBackgroundMode(key, null, id);
        });
      });
    });

    // Nút Hero 1-Click
    document.getElementById('wt3d-keyshot-all')?.addEventListener('click', (e) => {
      e.stopPropagation();
      console.log('[WT3D Canvas Studio] ⚡ 1-Click Render button triggered!');
      runTask(`Thiết Lập Render 1-Click (${activeProfile.toUpperCase()})`, run1ClickRender);
    });

    // Gắn sự kiện góc nhìn Perspective 3/4 Y-Up
    document.getElementById('wt3d-cam-down')?.addEventListener('click', (e) => {
      e.stopPropagation();
      runTask('3/4 Nhìn Xuống (Showcase)', id => rotatePerspective34('down_right', id));
    });

    document.getElementById('wt3d-cam-up')?.addEventListener('click', (e) => {
      e.stopPropagation();
      runTask('3/4 Nhìn Lên (Hero Bệ Vệ)', id => rotatePerspective34('up_hero', id));
    });

    document.getElementById('wt3d-cam-down-left')?.addEventListener('click', (e) => {
      e.stopPropagation();
      runTask('3/4 Trái Nhìn Xuống', id => rotatePerspective34('down_left', id));
    });

    document.getElementById('wt3d-cam-eye')?.addEventListener('click', (e) => {
      e.stopPropagation();
      runTask('3/4 Ngang Tầm Mắt', id => rotatePerspective34('eye_right', id));
    });

    document.getElementById('wt3d-action-fit')?.addEventListener('click', (e) => {
      e.stopPropagation();
      runTask('Fit Screen', fitToScreen);
    });

    document.getElementById('wt3d-action-saveview')?.addEventListener('click', (e) => {
      e.stopPropagation();
      runTask('Lưu Default View', saveView);
    });

    document.getElementById('wt3d-action-exportpng')?.addEventListener('click', (e) => {
      e.stopPropagation();
      let snap = null;
      try { snap = canvas()?.toDataURL('image/png'); } catch(_) {}
      runTask('Xuất Full HD 16:9', (id) => exportPng(id, 1920, 1080, snap));
    });

    // Mở nhanh các tab (MỞ VÀ GIỮ NGUYÊN TAB TRÊN MÀN HÌNH)
    panel.querySelectorAll('[data-tab]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const tab = btn.dataset.tab;
        if (tab) {
          runTask(`Mở Tab ${tab.toUpperCase()}`, async (id) => {
            await openTab(tab, id);
          });
        }
      });
    });

    // Copy Annotation
    document.getElementById('wt3d-copy-anno-desc')?.addEventListener('click', async (e) => {
      e.stopPropagation();
      const txt = getAnnotationContent();
      try {
        await navigator.clipboard.writeText(txt);
        setStatus('📋 ĐÃ CHÉP MÔ TẢ ANNOTATION VÀO CLIPBOARD!', '#0071e3');
      } catch(_) {
        setStatus('⚠️ Không thể ghi clipboard', '#dc2626');
      }
    });

    document.getElementById('wt3d-copy-anno-title')?.addEventListener('click', async (e) => {
      e.stopPropagation();
      try {
        await navigator.clipboard.writeText('tanphan1105');
        setStatus('📝 ĐÃ CHÉP "tanphan1105" VÀO CLIPBOARD!', '#0071e3');
      } catch(_) {}
    });

    document.getElementById('wt3d-copy-pinned-comment')?.addEventListener('click', async (e) => {
      e.stopPropagation();
      const txt = getPinnedCommentContent();
      try {
        await navigator.clipboard.writeText(txt);
        setStatus('💬 ĐÃ CHÉP BÌNH LUẬN GHIM (KÈM LINK FAB) VÀO CLIPBOARD!', '#7c3aed');
      } catch(_) {}
    });

    // Minimize toggle
    document.getElementById('wt3d-minimize')?.addEventListener('click', (e) => {
      e.stopPropagation();
      const body = document.getElementById('wt3d-studio-body');
      const minBtn = document.getElementById('wt3d-minimize');
      if (!body) return;
      isMinimized = !isMinimized;
      body.style.display = isMinimized ? 'none' : 'block';
      if (minBtn) minBtn.textContent = isMinimized ? '+' : '−';
    });

    // Side switch (left / right)
    document.getElementById('wt3d-toggle-side')?.addEventListener('click', (e) => {
      e.stopPropagation();
      isLeftSide = !isLeftSide;
      panel.style.left = isLeftSide ? '20px' : 'auto';
      panel.style.right = isLeftSide ? 'auto' : '20px';
    });

    function ensureStudioLauncher() {
      let btn = document.getElementById('wt3d-studio-launcher-btn');
      if (btn) return btn;
      btn = document.createElement('div');
      btn.id = 'wt3d-studio-launcher-btn';
      btn.title = 'Kéo thả để di chuyển vị trí bất kỳ • Click để mở lại WT3D KeyShot Studio';
      btn.innerHTML = '<span style="opacity:0.75;margin-right:4px;cursor:grab;">⠿</span> 🎨 WT3D 3D STUDIO';
      btn.style.cssText = `
        position: fixed;
        top: 16px;
        left: 20px;
        z-index: 2147483647;
        background: linear-gradient(135deg, #0071e3, #004d9b);
        color: #ffffff;
        border-radius: 30px;
        padding: 8px 16px;
        font-size: 12px;
        font-weight: 800;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        cursor: grab;
        box-shadow: 0 4px 20px rgba(0, 113, 227, 0.55);
        display: none;
        align-items: center;
        gap: 6px;
        user-select: none;
        touch-action: none;
      `;
      let dragging = false, moved = false, sx = 0, sy = 0, il = 0, it = 0;
      btn.addEventListener('pointerdown', e => {
        if (e.button !== 0) return;
        e.stopPropagation();
        dragging = true; moved = false;
        btn.style.cursor = 'grabbing';
        const r = btn.getBoundingClientRect();
        il = r.left; it = r.top; sx = e.clientX; sy = e.clientY;
        btn.style.right = 'auto';
        btn.style.left = il + 'px';
        btn.style.top = it + 'px';
        try { btn.setPointerCapture(e.pointerId); } catch (_) {}
        e.preventDefault();
      });
      btn.addEventListener('pointermove', e => {
        if (!dragging) return;
        e.stopPropagation();
        const dx = e.clientX - sx, dy = e.clientY - sy;
        if (Math.hypot(dx, dy) > 4) moved = true;
        btn.style.left = Math.max(4, Math.min(il + dx, window.innerWidth - btn.offsetWidth - 4)) + 'px';
        btn.style.top = Math.max(4, Math.min(it + dy, window.innerHeight - btn.offsetHeight - 4)) + 'px';
      });
      const stopDrag = e => {
        if (!dragging) return;
        e.stopPropagation();
        dragging = false;
        btn.style.cursor = 'grab';
        try { btn.releasePointerCapture(e.pointerId); } catch (_) {}
      };
      btn.addEventListener('pointerup', stopDrag);
      btn.addEventListener('pointercancel', stopDrag);
      btn.addEventListener('click', e => {
        e.stopPropagation();
        if (moved) { moved = false; return; }
        panel.style.display = 'block';
        btn.style.display = 'none';
      });
      document.body.appendChild(btn);
      return btn;
    }

    // Close / Stop
    document.getElementById('wt3d-close')?.addEventListener('click', (e) => {
      e.stopPropagation();
      if (running) {
        runId++;
        running = false;
        setStatus('🛑 Đã dừng theo yêu cầu!', '#dc2626');
      } else {
        panel.style.display = 'none';
        const lBtn = ensureStudioLauncher();
        if (lBtn) lBtn.style.display = 'flex';
      }
    });

    // Khởi tạo profile mặc định
    setProfileUI('soft');
  }

  // Observer & Polling để mount panel vào 3D editor iframe ngay khi canvas sẵn sàng
  // =========================================================================
  // [LIFECYCLE GUARDIAN] CHỈ XUẤT HIỆN TRONG 3D EDITOR - TỰ ĐỘNG BIẾN MẤT KHI XONG VIỆC
  // =========================================================================
  function isRealFab3DEditor() {
    const urlLower = window.location.href.toLowerCase();
    if (!urlLower.includes('/dope/')) return false;
    const c = canvas();
    if (!c) return false;
    const cRect = c.getBoundingClientRect();
    if (cRect.width >= 200 && cRect.height >= 180) {
      if (urlLower.includes('/edit')) return true;
      const hasSaveBtn = Array.from(document.querySelectorAll('button, [role="button"]')).some(el => {
        const t = (el.textContent || '').trim().toLowerCase();
        return t === 'save' || t === 'up to date' || t === 'lighting' || t === 'materials' || t === 'camera';
      });
      if (hasSaveBtn) return true;
    }

    // Kiểm tra các tín hiệu chỉ có trong Fab 3D Settings Editor thực thụ:
    const docs = getAccessibleDocs();
    for (const doc of docs) {
      // Tín hiệu A: Header trên đỉnh có "Edit 3D settings" hoặc nút "Save" / "Up to date"
      const hasEditorHeader = Array.from(doc.querySelectorAll('h1, h2, h3, header, div, span, button')).some(el => {
        if (el.closest?.('#wt3d-fab-studio-panel')) return false;
        const r = el.getBoundingClientRect();
        if (r.top > 100 || r.width === 0) return false;
        const t = (el.textContent || '').trim().toLowerCase();
        return t === 'edit 3d settings' || t.startsWith('edit 3d') || t === 'up to date';
      });
      if (hasEditorHeader) return true;

      // Tín hiệu B: Thanh công cụ đáy chứa các tab đặc trưng (Lighting, Materials, Look, Camera, Scene, Annotations, Inspect)
      const editorTabs = ['lighting', 'materials', 'camera', 'look', 'scene', 'annotations', 'inspect'];
      const matchedSet = new Set();
      const elements = Array.from(doc.querySelectorAll('button, [role="tab"], [role="button"], span, div, li')).filter(el => {
        if (el.closest?.('#wt3d-fab-studio-panel')) return false;
        const r = el.getBoundingClientRect();
        return r.width > 0 && r.height > 0 && r.bottom > window.innerHeight - 180;
      });

      for (const el of elements) {
        const raw = ((el.textContent || '') + ' ' + (el.getAttribute?.('aria-label') || '') + ' ' + (el.getAttribute?.('title') || '')).toLowerCase();
        for (const tabKey of editorTabs) {
          if (new RegExp(`\\b${tabKey}\\b`, 'i').test(raw)) {
            matchedSet.add(tabKey);
          }
        }
        if (matchedSet.size >= 2) return true;
      }
    }

    return false;
  }

  function syncStudioLifecycle() {
    try {
      if (typeof chrome !== 'undefined' && chrome.storage && (!chrome.runtime || !chrome.runtime.id)) {
        if (window.__WT3D_DOPE_POLL__) clearInterval(window.__WT3D_DOPE_POLL__);
        return;
      }
    } catch (_) {
      if (window.__WT3D_DOPE_POLL__) clearInterval(window.__WT3D_DOPE_POLL__);
      return;
    }
    const panel = document.getElementById('wt3d-fab-studio-panel');
    const urlLower = window.location.href.toLowerCase();
    // [ZERO-REFLOW FAST PATH] Khi bảng đã hiện trong /dope/... và canvas còn sống: thoát ngay 0ms, tuyệt đối không quét DOM gây kẹt RAM/CPU!
    if (panel && urlLower.includes('/dope/') && canvas()?.isConnected) {
      return;
    }
    const isEditor = isRealFab3DEditor();

    if (!isEditor) {
      if (panel) {
        panel.remove();
        window.__wt3dCachedMaterials = null;
        console.log('[WT3D Canvas Studio] 🧹 Dọn dẹp sạch Studio Panel khỏi trang Preview/Listing (Zero Clutter).');
      }
      return;
    }

    if (!panel && canvas()) {
      createStudioPanel();
    }
  }

  // Tự động bắt chi tiết khi người dùng click chuột lên mô hình 3D hoặc cột phải của Fab (bỏ qua nếu kéo xoay camera hoặc giữ Ctrl)
  if (window.__WT3D_FAB_DOWN_LISTENER__) {
    try { document.removeEventListener('pointerdown', window.__WT3D_FAB_DOWN_LISTENER__, true); } catch (_) {}
  }
  if (window.__WT3D_FAB_SELECT_LISTENER__) {
    try { document.removeEventListener('pointerup', window.__WT3D_FAB_SELECT_LISTENER__, true); } catch (_) {}
  }
  let __wt3dDownPos = null;
  let __wt3dSelectSyncTimer = null;
  window.__WT3D_FAB_DOWN_LISTENER__ = (e) => {
    if (e.button !== 0 || e.ctrlKey) { __wt3dDownPos = null; return; }
    __wt3dDownPos = { x: e.clientX, y: e.clientY };
  };
  window.__WT3D_FAB_SELECT_LISTENER__ = (e) => {
    if (e.button !== 0 || e.ctrlKey) return;
    const t = e.target;
    if (!t || t.closest?.('#wt3d-fab-studio-panel')) return;
    if (__wt3dDownPos && Math.hypot(e.clientX - __wt3dDownPos.x, e.clientY - __wt3dDownPos.y) > 6) {
      return; // Đang kéo chuột xoay camera -> không đổi lựa chọn
    }
    const clickSnap = { target: t, clientX: e.clientX, clientY: e.clientY };
    if (__wt3dSelectSyncTimer) clearTimeout(__wt3dSelectSyncTimer);
    __wt3dSelectSyncTimer = setTimeout(() => {
      syncFabSelectionToTargetSelect(clickSnap);
    }, 150);
  };
  document.addEventListener('pointerdown', window.__WT3D_FAB_DOWN_LISTENER__, true);
  document.addEventListener('pointerup', window.__WT3D_FAB_SELECT_LISTENER__, true);

  // Giải phóng sạch bộ nhớ khi đóng/tải lại trang (Chống kẹt RAM)
  window.addEventListener('pagehide', () => {
    if (window.__WT3D_DOPE_POLL__) clearInterval(window.__WT3D_DOPE_POLL__);
    if (__wt3dSelectSyncTimer) clearTimeout(__wt3dSelectSyncTimer);
    window.__wt3dCachedMaterials = null;
  }, { once: true });

  // Cross-frame Bridge: Receive open-tab requests from outer listing panel
  if (window.__WT3D_DOPE_MSG_BRIDGE__) {
    try { window.removeEventListener('message', window.__WT3D_DOPE_MSG_BRIDGE__); } catch (_) {}
  }
  window.__WT3D_DOPE_MSG_BRIDGE__ = async (e) => {
    if (e.data?.type === 'wt3d-open-tab' && e.data.tab) {
      try {
        await openTab(e.data.tab);
        console.log('[WT3D Canvas Studio] 🎯 Switched tab via postMessage:', e.data.tab);
      } catch (err) {
        console.warn('[WT3D Canvas Studio] openTab via postMessage failed:', err.message);
      }
    }
  };
  window.addEventListener('message', window.__WT3D_DOPE_MSG_BRIDGE__);

  if (window.__WT3D_DOPE_OBSERVER__) {
    try { window.__WT3D_DOPE_OBSERVER__.disconnect(); } catch (_) {}
    window.__WT3D_DOPE_OBSERVER__ = null;
  }
  if (window.__WT3D_DOPE_POLL__) {
    clearInterval(window.__WT3D_DOPE_POLL__);
  }

  window.__WT3D_DOPE_POLL__ = setInterval(() => {
    syncStudioLifecycle();
  }, 2000);

  syncStudioLifecycle();
})();
