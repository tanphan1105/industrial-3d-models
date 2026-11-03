// Pure, deterministic preset planner & WT3D Reusable Material Library engine (v3.9.56).
// Uses only verified Fab pbr_metalness channels (roughness.factor, metalness.factor, basecolor.color)
// to prevent HTTP 400 schema rejection when clearcoatroughness.invert is null.
((root, factory) => {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else Object.defineProperty(root, 'WT3DRenderPreset', { value: api, configurable: true });
})(typeof globalThis === 'object' ? globalThis : this, () => {
  'use strict';
  const SOURCE_SCENE = 'ee6ff6e9-a957-429f-a650-234082bae031';
  const REFERENCE = {
    environment: { enabled: true, brightness: 1.95, rotation: 1.32645, shadowEnabled: false, shadowBias: 25 },
    background: { enabled: true, type: 'COLOR', color: [0.666667, 0.72549, 0.772549], applyPostProcesses: true },
    ground: { enabled: true, displayAO: true, displayTextureShadows: false, displayRaytraceShadows: false, intensity: 1.0, borderFade: 0, diffusion: 0.55 },
    camera: { fov: 45, autoExposure: false, exposure: 1.05, nearFarRatio: 0.007 },
    postprocess: {
      useDOF: false, useBloom: true, bloomFactor: 0.12, useGrain: false, useChroma: false,
      useSSAO: true, ssaoRadius: 0.75, ssaoIntensity: 0.42, ssaoBias: 0.06,
      useSSR: true, useVignette: true, vignetteAmount: 0.08, vignetteHardness: 0.85,
      useColorBalance: true, colorBalanceLow: [0, 0, 0], colorBalanceMid: [0, 0, 0], colorBalanceHigh: [0.01, 0.01, 0.02],
      useToneMapping: true, toneMethod: 0, toneExposure: 1.12,
      toneBrightness: 0.05, toneContrast: 0.04, toneSaturation: 1.06,
      useTAA: true, useFXAA: true, sharpnessFactor: 1.15
    }
  };

  // Bảng vật liệu chuẩn công nghiệp WT3D (chỉ dùng metalness & roughness đã enabled sẵn trên Fab để tuyệt đối không gây lỗi HTTP 400)
  const DEFAULT_WT3D_MATERIAL_PROFILES = {
    // 1. Inox SUS304 / SUS316 / Chrome sáng bóng (Độ phản xạ chuẩn KeyShot công nghiệp)
    '190,188,186': { category: 'stainless_steel', metalness: 0.95, roughness: 0.16 },
    '224,223,219': { category: 'stainless_steel', metalness: 0.95, roughness: 0.16 },
    '180,178,167': { category: 'stainless_steel', metalness: 0.95, roughness: 0.16 },
    '162,163,167': { category: 'stainless_steel', metalness: 0.95, roughness: 0.16 },
    '178,178,178': { category: 'stainless_steel', metalness: 0.95, roughness: 0.16 },
    'xid_semipolished': { category: 'stainless_steel', metalness: 1.0, roughness: 0.18 },
    'xid_stainlesspolished': { category: 'stainless_steel', metalness: 1.0, roughness: 0.10 },
    'xid_stainlesssteelbright': { category: 'stainless_steel', metalness: 1.0, roughness: 0.08 },
    'xid_inoxbong': { category: 'stainless_steel', metalness: 1.0, roughness: 0.08 },
    'xid_steelpolished': { category: 'stainless_steel', metalness: 0.95, roughness: 0.18 },
    // 2. Thép gia công / Inox xước mờ / Mặt bích & Khung skid Inox
    '129,130,133': { category: 'brushed_steel', metalness: 0.85, roughness: 0.25 },
    'xid_stainlessbrushed': { category: 'brushed_steel', metalness: 0.88, roughness: 0.24 },
    'xid_stainlesssatincoarsescreen': { category: 'brushed_steel', metalness: 0.88, roughness: 0.26 },
    '191,191,191': { category: 'cast_steel_flange', metalness: 0.85, roughness: 0.24 },
    '200,200,200': { category: 'anodized_aluminum', metalness: 0.75, roughness: 0.26 },
    // 3. Đồng thau / Brass (Van đồng, xả khí, rắc co đồng)
    '203,154,59':  { category: 'brass', metalness: 0.92, roughness: 0.18 },
    '191,153,15':  { category: 'brass', metalness: 0.92, roughness: 0.18 },
    'xid_brasssatin': { category: 'brass', metalness: 0.92, roughness: 0.20 },
    // 4. Vỏ cột lọc Composite FRP Gelcoat & Vỏ tủ sơn tĩnh điện bóng cao cấp
    '155,173,136': { category: 'frp_vessel', metalness: 0.02, roughness: 0.14 },
    '191,187,166': { category: 'frp_vessel', metalness: 0.02, roughness: 0.14 },
    '197,194,148': { category: 'frp_vessel', metalness: 0.02, roughness: 0.14 },
    '199,191,174': { category: 'frp_vessel', metalness: 0.02, roughness: 0.14 },
    '255,227,181': { category: 'frp_vessel', metalness: 0.02, roughness: 0.14 },
    '229,226,188': { category: 'frp_vessel', metalness: 0.02, roughness: 0.14 },
    '212,175,55':  { category: 'frp_vessel', metalness: 0.02, roughness: 0.14 },
    '240,215,140': { category: 'frp_vessel', metalness: 0.02, roughness: 0.14 },
    '31,31,180':   { category: 'frp_vessel_blue', metalness: 0.02, roughness: 0.14 },
    '0,102,204':   { category: 'frp_vessel_blue', metalness: 0.02, roughness: 0.14 },
    '25,84,166':   { category: 'frp_vessel_blue', metalness: 0.02, roughness: 0.14 },
    'xid_bluewallpaintglossy': { category: 'frp_vessel_blue', metalness: 0.02, roughness: 0.14 },
    'xid_smoothyellow': { category: 'frp_vessel', metalness: 0.02, roughness: 0.14 },
    'xid_smoothdarkseagreen': { category: 'frp_vessel', metalness: 0.02, roughness: 0.14 },
    '235,235,235': { category: 'gloss_cabinet_frp', metalness: 0.02, roughness: 0.14 },
    '240,240,238': { category: 'gloss_cabinet_frp', metalness: 0.02, roughness: 0.14 },
    '242,242,255': { category: 'gloss_cabinet_frp', metalness: 0.02, roughness: 0.14 },
    '244,244,244': { category: 'gloss_cabinet_frp', metalness: 0.02, roughness: 0.14 },
    '245,245,245': { category: 'gloss_cabinet_frp', metalness: 0.02, roughness: 0.14 },
    '245,246,246': { category: 'gloss_cabinet_frp', metalness: 0.02, roughness: 0.14 },
    '255,251,240': { category: 'gloss_cabinet_frp', metalness: 0.02, roughness: 0.14 },
    '255,254,246': { category: 'gloss_cabinet_frp', metalness: 0.02, roughness: 0.14 },
    '255,255,255': { category: 'gloss_cabinet_frp', metalness: 0.02, roughness: 0.14 },
    '230,233,236': { category: 'gloss_cabinet_frp', metalness: 0.02, roughness: 0.14 },
    'xid_smoothwhite': { category: 'gloss_cabinet_frp', metalness: 0.02, roughness: 0.14 },
    'xid_smootwoffwhite': { category: 'gloss_cabinet_frp', metalness: 0.02, roughness: 0.14 },
    // 5. Đường ống & Phụ kiện nhựa uPVC Sch80 / PPR xanh lá / Khung sơn tĩnh điện
    '123,124,127': { category: 'upvc_pipe', metalness: 0.0, roughness: 0.24 },
    '128,128,128': { category: 'upvc_pipe', metalness: 0.0, roughness: 0.24 },
    '97,103,121':  { category: 'upvc_pipe', metalness: 0.0, roughness: 0.24 },
    '89,96,114':   { category: 'upvc_pipe', metalness: 0.0, roughness: 0.24 },
    '46,138,87':   { category: 'ppr_pipe_green', metalness: 0.0, roughness: 0.22 },
    '0,102,170':   { category: 'skid_frame_blue', metalness: 0.10, roughness: 0.22 },
    '1,128,171':   { category: 'skid_frame_blue', metalness: 0.10, roughness: 0.22 },
    'xid_smoothmediumgray': { category: 'upvc_pipe', metalness: 0.0, roughness: 0.24 },
    'xid_smoothdarkforestgreen': { category: 'ppr_pipe_green', metalness: 0.0, roughness: 0.22 },
    // 6. Thân động cơ gang đúc (Cast Iron Motor) & Chi tiết cơ khí đen mờ
    '5,5,5':       { category: 'cast_iron_motor', metalness: 0.35, roughness: 0.32 },
    '47,47,47':    { category: 'cast_iron_motor', metalness: 0.30, roughness: 0.35 },
    '64,64,64':    { category: 'cast_iron_motor', metalness: 0.25, roughness: 0.38 },
    // 7. Cao su EPDM / Đế cột lọc / Gioăng làm kín đen mờ
    '0,0,0':       { category: 'rubber_matte', metalness: 0.0, roughness: 0.50 },
    '80,80,80':    { category: 'rubber_matte', metalness: 0.0, roughness: 0.48 },
    'xid_rubberblack': { category: 'rubber_matte', metalness: 0.0, roughness: 0.55 },
    // 8. Kính đo lưu lượng / Đồng hồ áp suất / Ống quan sát trong suốt
    'xid_clearglass': { category: 'clear_glass', metalness: 0.0, roughness: 0.04 },
    'glass_flowmeter': { category: 'clear_glass', metalness: 0.0, roughness: 0.04 }
  };

  const copy = v => JSON.parse(JSON.stringify(v));
  const isNumber = v => typeof v === 'number' && Number.isFinite(v);

  function normalizeMaterialKey(rawName) {
    const s = String(rawName || '').trim();
    if (!s) return '';
    // Trường hợp 1: Tên STEP/CAD dạng 'XID_StainlessPolished_B2F31C181E6A4A56A6A0E999BB4A0B8F_shader'
    const xidMatch = /^XID_([A-Za-z0-9]+?)_[0-9A-Fa-f]{16,}(?:_shader)?$/i.exec(s);
    if (xidMatch) {
      const cleanXid = xidMatch[1].replace(/\d+$/, '').toLowerCase();
      return 'xid_' + (cleanXid || xidMatch[1].toLowerCase());
    }
    // Trường hợp 2: Tên RGB Inventor/Blender dạng '190,188,186_1' hoặc '190,188,186.001'
    const base = s.split('_')[0].split('.')[0].trim().toLowerCase();
    return base || s.toLowerCase();
  }

  function extractMaterialLibrary(materials) {
    const lib = {};
    if (!materials || typeof materials !== 'object') return lib;
    for (const [, m] of Object.entries(materials)) {
      if (!m || typeof m !== 'object' || m.type !== 'pbr_metalness') continue;
      const name = String(m.name || '').trim();
      if (!name || name.startsWith('WT3D_Decal_')) continue;
      const key = normalizeMaterialKey(name);
      if (!key || key === 'xid') continue;
      const factor = m['roughness.factor'];
      const rough = isNumber(factor) ? (m['roughness.invert'] ? 1 - factor : factor) : undefined;
      lib[key] = {
        name,
        key,
        basecolor: (m['basecolor.enabled'] && Array.isArray(m['basecolor.color']) && m['basecolor.color'].length === 3) ? copy(m['basecolor.color']) : undefined,
        metalness: (m['metalness.enabled'] && isNumber(m['metalness.factor'])) ? m['metalness.factor'] : undefined,
        roughness: (m['roughness.enabled'] && isNumber(rough)) ? rough : undefined
      };
    }
    return lib;
  }

  function materialKey(m) {
    const key = normalizeMaterialKey(m.name), rgb = m['basecolor.color'];
    // FBX can strip commas. Match against this material's own RGB before normalizing.
    if (/^\d{3,9}$/.test(key) && Array.isArray(rgb) && rgb.length === 3 && rgb.every(isNumber)) {
      const bytes = rgb.map(v => Math.round(v * 255));
      if (bytes.join('') === key) return bytes.join(',');
    }
    return key;
  }

  function fitCamera(bounds, { aspect, upAxis, fov = 45, margin = 1.08 } = {}) {
    if (!['Y', 'Z'].includes(upAxis)) throw new Error('Model up-axis must be verified before fitting');
    if (!isNumber(aspect) || aspect <= 0 || !isNumber(fov) || fov <= 1 || fov >= 170 || !isNumber(margin) || margin < 1) throw new Error('Invalid viewport or field of view');
    const { min, max } = bounds || {};
    if (![min, max].every(a => Array.isArray(a) && a.length === 3 && a.every(isNumber)) || min.some((v,i) => v > max[i])) throw new Error('Invalid scene bounds');
    const target = min.map((v, i) => (v + max[i]) / 2);
    const radius = Math.hypot(...min.map((v,i) => max[i]-v)) / 2;
    if (radius <= 0) throw new Error('Degenerate scene bounds');
    const verticalHalf = fov * Math.PI / 360;
    const horizontalHalf = Math.atan(Math.tan(verticalHalf) * aspect);
    const distance = margin * radius / Math.sin(Math.min(verticalHalf, horizontalHalf));
    const direction = upAxis === 'Y' ? [1, 0.65, 1] : [1, -1, 0.65];
    const length = Math.hypot(...direction);
    return { target, eye: target.map((v,i) => v + direction[i] / length * distance), fov, distance, radius, upAxis };
  }

  function plan(current, options = {}) {
    if (!current || typeof current !== 'object') throw new Error('Missing scene settings');
    const patch = {};
    const unsupported = [];
    for (const [section, values] of Object.entries(REFERENCE)) {
      if (!current[section] || typeof current[section] !== 'object') {
        unsupported.push(section);
        continue;
      }
      const changes = {};
      for (const [key, value] of Object.entries(values)) {
        if (!Object.prototype.hasOwnProperty.call(current[section], key)) {
          unsupported.push(section + '.' + key);
          continue;
        }
        changes[key] = copy(value);
      }
      if (Object.keys(changes).length) patch[section] = changes;
    }
    if (current.light && typeof current.light === 'object') {
      const lightChanges = {};
      if ('rotation' in current.light) lightChanges.rotation = 0;
      if (Array.isArray(current.light.lights)) {
        lightChanges.lights = copy(current.light.lights).map(l => (l && typeof l === 'object') ? { ...l, enabled: false } : l);
      }
      if (Object.keys(lightChanges).length) patch.light = lightChanges;
    }
    if (isNumber(options.sceneScale) && options.sceneScale > 0 && current.postprocess && 'ssaoRadius' in current.postprocess) {
      patch.postprocess.ssaoRadius = 0.648 * options.sceneScale;
    }
    if (options.cameraFit) {
      const { eye, target } = options.cameraFit;
      if (![eye, target].every(a => Array.isArray(a) && a.length === 3 && a.every(isNumber))) throw new Error('Invalid camera fit');
      if (Math.hypot(...eye.map((v, i) => v - target[i])) <= 0) throw new Error('Camera eye equals target');
      patch.camera = { ...patch.camera, eye: copy(eye), target: copy(target) };
    }
    return { name: 'WT3D Reference Studio', sourceScene: SOURCE_SCENE, patch, unsupported,
      preserved: ['materials', 'materialgroups', 'models', 'environment.uid', 'ground.position', 'ground.groundScale'],
      needsFit: !options.cameraFit,
      needsEnvironmentMatch: true };
  }

  function verify(actual, patch, prefix = '') {
    const failures = [];
    for (const [key, expected] of Object.entries(patch)) {
      const path = prefix ? (prefix + '.' + key) : key;
      const value = actual?.[key];
      if (Array.isArray(expected)) {
        if (!Array.isArray(value) || value.length !== expected.length || expected.some((n, i) => isNumber(n) ? !isNumber(value[i]) || Math.abs(n - value[i]) > 1e-5 : (n && typeof n === 'object') ? verify(value[i], n, path + '[' + i + ']').length > 0 : n !== expected[i])) failures.push(path);
      } else if (expected && typeof expected === 'object') failures.push(...verify(value, expected, path));
      else if (isNumber(expected) ? !isNumber(value) || Math.abs(expected - value) > 1e-5 : value !== expected) failures.push(path);
    }
    return failures;
  }

  function polish(materials, customLibrary = null, { preserveColors = false } = {}) {
    const result = copy(materials), changed = [], skipped = [], customMatched = [], presetMatched = [];
    const userLib = (customLibrary && typeof customLibrary === 'object') ? customLibrary : {};

    for (const [uid, m] of Object.entries(result)) {
      const name = String(m?.name || '');
      const factor = m?.['roughness.factor'];
      const textured = !!(m?.['roughness.texture.uri'] || m?.['basecolor.texture.uri']);
      const transparent = (m?.['opacity.enabled'] && m?.['opacity.factor'] < 0.98) || m?.['transmission.enabled'];

      // Chỉ can thiệp trên vật liệu pbr_metalness có sẵn roughness.enabled === true và factor hợp lệ
      if (!m || m.type !== 'pbr_metalness' || !m['roughness.enabled'] || !isNumber(factor) || name.startsWith('WT3D_Decal_') || textured || transparent) {
        skipped.push(uid);
        continue;
      }

      const key = materialKey(m);

      // Ưu tiên 1: Khớp từ Thư Viện Vật Liệu Mẫu do người dùng bấm [💾 Lưu Vật Liệu Mẫu]
      if (key && key !== 'xid' && userLib[key]) {
        const saved = userLib[key];
        let didChange = false;
        if (!preserveColors && m['basecolor.enabled'] && Array.isArray(saved.basecolor) && saved.basecolor.length === 3 && saved.basecolor.every(v => isNumber(v) && v >= 0 && v <= 1) && Array.isArray(m['basecolor.color']) && m['basecolor.color'].length === 3) {
          m['basecolor.color'] = copy(saved.basecolor);
          didChange = true;
        }
        if (m['metalness.enabled'] && isNumber(saved.metalness) && isNumber(m['metalness.factor'])) {
          m['metalness.factor'] = Math.max(0, Math.min(1, saved.metalness));
          didChange = true;
        }
        if (isNumber(saved.roughness)) {
          const clampedRough = Math.max(0, Math.min(1, saved.roughness));
          m['roughness.factor'] = m['roughness.invert'] ? 1 - clampedRough : clampedRough;
          didChange = true;
        }
        if (didChange) {
          if (JSON.stringify(m) !== JSON.stringify(materials[uid])) changed.push(uid);
          customMatched.push(uid);
          continue;
        }
      }

      // Ưu tiên 2: Khớp từ Bảng Vật Liệu Công Nghiệp Chuẩn WT3D (Inox SUS304, Đồng, Cột lọc FRP, Ống uPVC, Cao su)
      if (key && DEFAULT_WT3D_MATERIAL_PROFILES[key]) {
        const prof = DEFAULT_WT3D_MATERIAL_PROFILES[key];
        let didChange = false;
        // RGB alone cannot distinguish painted steel, plastic and bare metal.
        if (key.startsWith('xid_') && m['metalness.enabled'] && isNumber(prof.metalness) && isNumber(m['metalness.factor'])) {
          m['metalness.factor'] = Math.max(0, Math.min(1, prof.metalness));
          didChange = true;
        }
        if (isNumber(prof.roughness)) {
          const clampedRough = Math.max(0, Math.min(1, prof.roughness));
          m['roughness.factor'] = m['roughness.invert'] ? 1 - clampedRough : clampedRough;
          didChange = true;
        }
        if (didChange) {
          if (JSON.stringify(m) !== JSON.stringify(materials[uid])) changed.push(uid);
          presetMatched.push(uid);
          continue;
        }
      }

      // Ưu tiên 3: Quy tắc chuốt bóng tổng quát cho các vật liệu còn lại
      const rgb = m['basecolor.color'];
      const rubber = /rubber|gasket|seal|foam|cloth|fabric|wood|concrete/i.test(name);
      const dark = Array.isArray(rgb) && Math.max(...rgb) < 0.10;
      if (rubber || dark) {
        skipped.push(uid);
        continue;
      }
      const rough = m['roughness.invert'] ? 1 - factor : factor;
      const maxRough = isNumber(m['metalness.factor']) && m['metalness.factor'] >= 0.8 ? 0.20 : 0.28;
      if (rough > maxRough + 1e-6) {
        m['roughness.factor'] = m['roughness.invert'] ? 1 - maxRough : maxRough;
        changed.push(uid);
      }
    }
    return { materials: result, changed, skipped, customMatched, presetMatched };
  }

  function polishRoughnessOnly(materials) {
    const result = copy(materials), changed = [], skipped = [];
    for (const [uid, m] of Object.entries(result)) {
      const name = String(m?.name || '');
      const rgb = m?.['basecolor.color'];
      const factor = m?.['roughness.factor'];
      const textured = !!m?.['roughness.texture.uri'];
      const transparent = (m?.['opacity.enabled'] && m?.['opacity.factor'] < 1) || m?.['transmission.enabled'];
      const rubber = /rubber|gasket|seal|foam|cloth|fabric|wood|concrete/i.test(name);
      const dark = Array.isArray(rgb) && Math.max(...rgb) < 0.10;
      if (m?.type !== 'pbr_metalness' || !m?.['roughness.enabled'] || !isNumber(factor) || textured || transparent || rubber || dark) {
        skipped.push(uid);
        continue;
      }
      const key = normalizeMaterialKey(name);
      const prof = key ? DEFAULT_WT3D_MATERIAL_PROFILES[key] : null;
      const rough = m['roughness.invert'] ? 1 - factor : factor;
      if (prof && isNumber(prof.roughness)) {
        const nextFactor = m['roughness.invert'] ? 1 - prof.roughness : prof.roughness;
        if (Math.abs(factor - nextFactor) > 1e-6) {
          m['roughness.factor'] = nextFactor;
          changed.push(uid);
        }
        continue;
      }
      const maxRough = isNumber(m['metalness.factor']) && m['metalness.factor'] >= 0.8 ? 0.26 : 0.32;
      if (rough > maxRough + 1e-6) {
        m['roughness.factor'] = m['roughness.invert'] ? 1 - maxRough : maxRough;
        changed.push(uid);
      }
    }
    return { materials: result, changed, skipped, customMatched: [], presetMatched: [] };
  }

  function hexToRgb(h) {
    if (!h) return [0.5, 0.5, 0.5];
    const clean = String(h).replace('#', '').trim();
    if (clean.length === 3) {
      return [
        parseInt(clean[0] + clean[0], 16) / 255,
        parseInt(clean[1] + clean[1], 16) / 255,
        parseInt(clean[2] + clean[2], 16) / 255
      ];
    }
    if (clean.length === 6) {
      return [
        parseInt(clean.slice(0, 2), 16) / 255,
        parseInt(clean.slice(2, 4), 16) / 255,
        parseInt(clean.slice(4, 6), 16) / 255
      ];
    }
    return [0.5, 0.5, 0.5];
  }

  function colorDist(c1, c2) {
    const r1 = c1[0], g1 = c1[1], b1 = c1[2];
    const r2 = c2[0], g2 = c2[1], b2 = c2[2];
    const rmean = (r1 + r2) / 2.0;
    const dr = r1 - r2;
    const dg = g1 - g2;
    const db = b1 - b2;
    const weightR = 2.0 + rmean;
    const weightG = 4.0;
    const weightB = 3.0 - rmean;
    return Math.sqrt(weightR * dr * dr + weightG * dg * dg + weightB * db * db);
  }

  function findBestPreset(material, presets) {
    if (!Array.isArray(presets) || !presets.length) return null;
    const name = String(material?.name || '').toLowerCase();
    const compact = name.replace(/[^a-z0-9]/g, '');
    const rawRgb = Array.isArray(material?.['basecolor.color']) && material['basecolor.color'].length === 3
      ? material['basecolor.color']
      : [0.5, 0.5, 0.5];
    const r = rawRgb[0], g = rawRgb[1], b = rawRgb[2];
    const maxVal = Math.max(r, g, b);
    const minVal = Math.min(r, g, b);
    const diff = maxVal - minVal;
    const isMono = diff < 0.06;
    const brightness = (r + g + b) / 3.0;
    const hasTrans = !!material?.['transmission.enabled'];
    const hasAlpha = !!(material?.['opacity.enabled'] && isNumber(material?.['opacity.factor']) && material['opacity.factor'] < 0.98);

    const findByName = (pName) => presets.find(p => p.name === pName) || null;

    // 1. Kênh kỹ thuật đặc biệt (Bảo toàn tuyệt đối Vật liệu Clear & Trong suốt)
    if (
      hasTrans ||
      /clear|transpar|kinh|glass|sight|rotameter|acrylic|polycarbonate|luu.luong/i.test(name) ||
      compact.startsWith('229229229') ||
      compact.startsWith('236241239') ||
      compact.startsWith('250250250') ||
      compact.startsWith('47159195') ||
      compact.startsWith('77202255') ||
      (hasAlpha && !name.toLowerCase().endsWith('_trans') && (isMono || (b > 0.65 && g > 0.55 && r < 0.45)))
    ) {
      return findByName('Ống uPVC clear');
    }
    if (
      /phin|housing|cartridge|binh.loc/i.test(name) ||
      compact.startsWith('162241') ||
      compact.startsWith('7777250') ||
      compact.startsWith('114233245') ||
      (hasAlpha && !name.toLowerCase().endsWith('_trans') && b > 0.45 && b >= r && b >= g)
    ) {
      return findByName('Thân phin lọc trong suốt');
    }

    // 2. Từ khóa tên chi tiết CAD (Inventor / STEP)
    if (/tay|handle|lever|do|red|van.do/i.test(name) || compact.startsWith('20400') || compact.startsWith('22038')) {
      return findByName('Tay van đỏ');
    }
    if (/thau|brass|dong|bronze/i.test(name) || compact.startsWith('20315459') || compact.startsWith('19115315')) {
      return findByName('Thau van điện');
    }
    if (!hasAlpha && (/ppr|forestgreen|xanh.la/i.test(name) || compact.startsWith('3313833') || compact.startsWith('1617174'))) {
      return findByName('Nhựa PPR');
    }
    if ((/skid|khung|frame/i.test(name) && /cam|orange/i.test(name)) || compact.startsWith('24411933') || compact.startsWith('207790')) {
      return findByName('Khung skid');
    }
    if (/frp|composite|cot.loc|carbon|vessel/i.test(name) || compact.startsWith('155173136') || compact.startsWith('191187166')) {
      return findByName('FRP cột lọc');
    }
    if (/ro.*frp|ro.*trang|membrane.*white|ro.*vessel/i.test(name)) {
      return findByName('Vỏ RO FRP trắng');
    }
    if (/bolt|bulong|oc|vit|nut|screw|washer|semipolished/i.test(name)) {
      return findByName('Bulong');
    }
    if (/inox|stainless|chrome|titanium/i.test(name)) {
      return findByName('Inox bóng');
    }
    if (/autovalve|runxin|clack|fleck|van.dien|head/i.test(name)) {
      return findByName('Đen autovalve');
    }
    if (/pump|bom/i.test(name)) {
      if (b > 0.45 && r < 0.3) return findByName('Xanh bơm');
      if (brightness < 0.25) return findByName('Đen bơm');
    }

    // 3. Phân loại màu cơ khí đặc thù
    if (r > 0.6 && g < 0.25 && b < 0.25) return findByName('Tay van đỏ');
    if (r > 0.75 && g > 0.35 && g < 0.65 && b < 0.20) return findByName('Khung skid');
    if (r > 0.65 && g > 0.50 && b < 0.35) return findByName('Thau van điện');
    if (g > 0.30 && g > r * 1.3 && g > b * 1.3) return findByName('Nhựa PPR');
    if (b > 0.70 && r < 0.35 && g < 0.35) return findByName('Nhựa xanh');
    if (b > 0.45 && r < 0.25 && g > 0.20 && g < 0.60) {
      return (g > 0.40) ? findByName('Xanh skid') : findByName('Xanh bơm');
    }
    if (b > 0.75 && g > 0.65 && r < 0.35) return findByName('Ống uPVC clear');

    // 4. Miền đơn sắc (Monochrome: Trắng -> Inox -> uPVC -> Đen)
    if (isMono || diff < 0.10) {
      if (brightness > 0.92) return findByName('Vỏ RO FRP trắng');
      if (brightness > 0.82) return findByName('Nhựa trắng');
      if (brightness >= 0.65 && brightness <= 0.82) return findByName('Inox bóng');
      if (brightness >= 0.44 && brightness < 0.65) return findByName('uPVC nhạt');
      if (brightness >= 0.20 && brightness < 0.44) return findByName('uPVC đậm');
      if (brightness >= 0.08 && brightness < 0.20) return findByName('PVC xám');
      if (brightness < 0.08) return findByName('Đen autovalve');
    }

    // 5. Khoảng cách màu Redmean tối ưu cho các màu còn lại
    let best = presets[0];
    let minD = 999;
    for (const p of presets) {
      const pRgb = p.rgb || hexToRgb(p.hex);
      const d = colorDist(rawRgb, pRgb);
      if (d < minD) {
        minD = d;
        best = p;
      }
    }
    return best;
  }

  function autoMapMaterials(materials, presetList) {
    const result = copy(materials);
    const changed = [];
    const report = [];
    const presets = Array.isArray(presetList) && presetList.length ? presetList : [];
    if (!presets.length) return { materials: result, changed, report };

    for (const [uid, m] of Object.entries(result)) {
      if (!m || typeof m !== 'object' || m.type !== 'pbr_metalness') continue;
      const name = String(m.name || '');
      if (name.startsWith('WT3D_Decal_')) continue;

      const compact = name.toLowerCase().replace(/[^a-z0-9]/g, '');
      const wasTrans = !!m['transmission.enabled'];
      const wasAlpha = !!(m['opacity.enabled'] && isNumber(m['opacity.factor']) && m['opacity.factor'] < 0.98);
      const origOpacityFactor = m['opacity.factor'];
      const origOpacityType = m['opacity.type'];
      const origOpacityInvert = m['opacity.invert'];
      const origColor = Array.isArray(m['basecolor.color']) ? copy(m['basecolor.color']) : null;
      const isInventorTintedTranslucent =
        compact.startsWith('2122070') ||
        compact.startsWith('102255128') ||
        compact.startsWith('17866209') ||
        compact.startsWith('215104221') ||
        (wasAlpha && compact.startsWith('1617174'));

      const p = findBestPreset(m, presets);
      if (!p) continue;

      const isClearOrHousingPreset = (p.name === 'Ống uPVC clear' || p.name === 'Thân phin lọc trong suốt');
      const keepCustomTranslucent = !isClearOrHousingPreset && (wasTrans || wasAlpha || isInventorTintedTranslucent);

      let didChange = false;
      const targetRgb = keepCustomTranslucent && origColor ? origColor : (p.rgb || hexToRgb(p.hex));

      // 1. Áp Base Color (giữ nguyên màu gốc nếu là chi tiết màu trong suốt đặc thù như vàng/xanh lá trong suốt)
      if (m['basecolor.enabled'] && Array.isArray(m['basecolor.color']) && m['basecolor.color'].length === 3) {
        m['basecolor.color'] = copy(targetRgb);
        didChange = true;
      }

      // 2. Áp Roughness (vật liệu trong suốt luôn giữ độ bóng kính 0.08 - 0.10)
      const targetRough = keepCustomTranslucent ? 0.10 : p.roughness;
      if (isNumber(targetRough)) {
        m['roughness.enabled'] = true;
        m['roughness.factor'] = m['roughness.invert'] ? 1 - targetRough : targetRough;
        didChange = true;
      }

      // 3. Áp Metalness (vật liệu trong suốt luôn có metalness = 0)
      const targetMetal = keepCustomTranslucent ? 0.0 : p.metalness;
      if (isNumber(targetMetal)) {
        m['metalness.enabled'] = true;
        m['metalness.factor'] = targetMetal;
        didChange = true;
      }

      // 4. Áp các kênh PBR mở rộng nếu có
      if (!keepCustomTranslucent && p.channels && typeof p.channels === 'object') {
        for (const [k, v] of Object.entries(p.channels)) {
          m[k] = copy(v);
          didChange = true;
        }
      }

      // 5. Bảo toàn tuyệt đối tính chất trong suốt / Clear nếu vật liệu gốc đã có Opacity hoặc Transmission
      if (keepCustomTranslucent) {
        if (wasTrans) {
          m['transmission.enabled'] = true;
        } else {
          m['opacity.enabled'] = true;
          m['opacity.type'] = origOpacityType || 'blending';
          m['opacity.factor'] = (isNumber(origOpacityFactor) && origOpacityFactor < 0.98) ? origOpacityFactor : 0.48;
          m['opacity.invert'] = !!origOpacityInvert;
        }
        didChange = true;
      }

      if (didChange) {
        changed.push(uid);
        report.push({
          uid,
          name,
          presetName: keepCustomTranslucent ? `${p.name} (Giữ trong suốt)` : p.name,
          hex: p.hex,
          roughness: targetRough,
          metalness: targetMetal,
          preservedTransparency: keepCustomTranslucent || isClearOrHousingPreset
        });
      }
    }

    return { materials: result, changed, report };
  }

  return {
    plan,
    verify,
    fitCamera,
    polish,
    polishRoughnessOnly,
    findBestPreset,
    autoMapMaterials,
    normalizeMaterialKey,
    extractMaterialLibrary,
    defaultProfiles: () => copy(DEFAULT_WT3D_MATERIAL_PROFILES),
    reference: () => copy(REFERENCE),
    sourceScene: SOURCE_SCENE
  };
});
