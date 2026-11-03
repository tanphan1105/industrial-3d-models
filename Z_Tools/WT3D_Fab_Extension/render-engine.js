// Native Fab editor adapter. The methods and payloads below were verified in
// Fab's editor JS and dataAccessModule (2026-10-22). No guessed runAction codes.
(() => {
  'use strict';
  if (!/^\/dope\/[^/]+\/edit\/?$/.test(location.pathname)) return;
  if (window.__wt3dRenderEngineMsgListener) {
    try { window.removeEventListener('message', window.__wt3dRenderEngineMsgListener); } catch (_) {}
  }
  if (window.__wt3dRenderEngineKeyListener) {
    try { window.removeEventListener('keydown', window.__wt3dRenderEngineKeyListener, true); } catch (_) {}
  }
  window.__wt3dVerifiedRenderAdapter = '3.9.38';
  document.documentElement.dataset.wt3dRenderAdapter = '3.9.38';
  document.documentElement.dataset.wt3dRenderProtocol = '1';
  const SOURCE_SCENE = 'ee6ff6e9-a957-429f-a650-234082bae031';
  const ENVIRONMENT = '08468d6fcf9846039cc3e51accddd9f9'; // Fallback Studio_Soft
  const PROFILES = {
    soft: { name: 'Gdansk Shipyard (Chuẩn WT3D)', uid: ENVIRONMENT, match: 'gdansk', brightness: 0.8, rotation: 1.32645, shadowBias: 25, color: [0.666667, 0.72549, 0.772549], applyPostProcesses: true },
    studio2: { name: 'Studio 2', uid: 'efd4ef0fc18a4ec0a1313d782fade965', brightness: 1, rotation: 0.66, color: [.24,.24,.24], applyPostProcesses: true },
    white: { name: 'Pure White', uid: ENVIRONMENT, brightness: 1.15, rotation: 0.66, color: [1,1,1], applyPostProcesses: false },
    industrial: { name: 'Industrial Room', uid: '9190e8da70694ef3b9d1d0c01541917e', brightness: 1, rotation: 5.707, color: [.32,.32,.32], applyPostProcesses: true },
    dark: { name: 'Dark Luxury', uid: 'efd4ef0fc18a4ec0a1313d782fade965', brightness: 1.1, rotation: 0.66, color: [.035,.035,.04], applyPostProcesses: true },
    outdoor: { name: 'Greenwich Park', uid: 'fcbb8844d24a428f8da17a415589a0c6', brightness: 1, rotation: 0.66, color: [.5,.5,.5], applyPostProcesses: true }
  };
  function resolveEnvUid(engine, profile, fallbackUid = ENVIRONMENT) {
    const envMap = engine?.envJson || {};
    if (profile?.match) {
      const re = profile.match instanceof RegExp ? profile.match : new RegExp(String(profile.match), 'i');
      for (const [k, v] of Object.entries(envMap)) {
        const text = typeof v === 'string' ? v : JSON.stringify(v || '');
        if (re.test(text)) return k;
      }
    }
    if (profile?.uid && envMap[profile.uid]) return profile.uid;
    if (fallbackUid && envMap[fallbackUid]) return fallbackUid;
    if (envMap[ENVIRONMENT]) return ENVIRONMENT;
    return Object.keys(envMap)[0] || null;
  }
  const OUTPUT = 'wt3d-render-engine-result';
  const BACKUP = 'wt3d-render-backup-data';
  const jsonCopy = value => JSON.parse(JSON.stringify(value));
  let prepared;
  let busy = false;
  let cancelled = false;
  const onKeyDown = event => { if (event.key === 'Escape') cancelled = true; };
  window.__wt3dRenderEngineKeyListener = onKeyDown;
  window.addEventListener('keydown', onKeyDown, true);
  const wait = ms => new Promise(resolve => setTimeout(resolve, ms));
  function publish(id, data) {
    let out = document.getElementById(OUTPUT);
    if (!out) {
      out = document.createElement('script');
      out.id = OUTPUT;
      out.type = 'application/json';
      document.documentElement.appendChild(out);
    }
    out.textContent = JSON.stringify({ requestId: id, ...data });
    window.postMessage({ type: 'wt3d-render-engine-result', requestId: id, ...data }, location.origin);
  }
  const stable = value => {
    if (Array.isArray(value)) return `[${value.map(stable).join(',')}]`;
    if (value && typeof value === 'object') return `{${Object.keys(value).sort().map(k => `${JSON.stringify(k)}:${stable(value[k])}`).join(',')}}`;
    return JSON.stringify(value);
  };
  function alive(engine, uid) {
    const c = document.querySelector('canvas');
    if (cancelled || !c?.isConnected || c.getBoundingClientRect().width < 100 || engine.args?.sceneUid !== uid) throw new Error('3D editor closed, cancelled, or model changed');
  }
  async function bounded(promise, label, ms = 15000) {
    let timer;
    try { return await Promise.race([promise, new Promise((_, reject) => { timer = setTimeout(() => reject(new Error(`${label} timed out`)), ms); })]); }
    finally { clearTimeout(timer); }
  }
  async function getSavedDoptions(engine, uid) {
    if (typeof engine.dataAccessModule?.fetchDoptions === 'function') {
      try {
        const data = await engine.dataAccessModule.fetchDoptions(uid);
        if (data?.materials) return data;
      } catch (_) {}
    }
    if (typeof engine.dataAccessModule?.getDoptions === 'function') {
      try {
        const data = await engine.dataAccessModule.getDoptions(uid);
        if (data?.materials) return data;
      } catch (_) {}
    }
    if (typeof window.fetch === 'function') {
      try {
        const response = await window.fetch('/i/previews/' + encodeURIComponent(uid) + '/doptions?_wt3d_read=' + crypto.randomUUID(), {
          credentials: 'same-origin', cache: 'no-store', headers: { Accept: 'application/json' }
        });
        if (response.ok) {
          const data = await response.json();
          if (data?.materials) return data;
        }
      } catch (_) {}
    }
    const fallback = engine.preloadedFetches?.doptions;
    if (fallback?.materials) return jsonCopy(fallback);
    throw new Error('Could not retrieve scene doptions');
  }
  function cameraData(raw) {
    if (raw?.error) throw new Error(String(raw.error));
    const view = raw?.camera || raw;
    const vector = x => Array.isArray(x) && x.length === 3 && x.every(n => typeof n === 'number' && Number.isFinite(n));
    if (!vector(view?.eye) || !vector(view?.target)) throw new Error(`Camera schema not supported yet: ${Object.keys(raw || {}).join(', ')}`);
    if (Math.hypot(...view.eye.map((x, i) => x - view.target[i])) < 1e-7) throw new Error('Engine camera is not initialized');
    return jsonCopy(view);
  }
  async function readCamera(engine) {
    if (typeof engine.getCameraView !== 'function' || typeof engine.setCameraView !== 'function') throw new Error('Native camera API unavailable');
    return cameraData(await bounded(engine.getCameraView(), 'Read camera'));
  }
  function fitKey() {
    const c = document.querySelector('canvas');
    c.focus({ preventScroll: true });
    for (const type of ['keydown', 'keyup']) {
      c.dispatchEvent(new KeyboardEvent(type, { key: 'f', code: 'KeyF', keyCode: 70, which: 70, bubbles: true, cancelable: true }));
    }
  }
  const protectedMaterials = materials => {
    const m = jsonCopy(materials);
    for (const value of Object.values(m)) {
      delete value['roughness.factor'];
      delete value['metalness.factor'];
      delete value['basecolor.color'];
    }
    return stable(m);
  };
  async function patchWithMaterialFallback(engine, uid, fresh, after, finish, label) {
    // 1. Gửi patch lên server Fab
    const res = await bounded(engine.dataAccessModule.patchDoptions(uid, after), label);

    // 2. Đồng bộ RAM cache ngay lập tức để getSavedDoptions và getDoptions trả về dữ liệu mới nhất
    try {
      const cached = await engine.dataAccessModule?.getDoptions?.(uid);
      if (cached && typeof cached === 'object') {
        for (const [k, v] of Object.entries(after)) {
          cached[k] = jsonCopy(v);
        }
      }
      if (engine.preloadedFetches) {
        engine.preloadedFetches.doptions = jsonCopy(after);
      }
    } catch (_) {}

    return { after, finish, fallbackUsed: false, serverResponse: res };
  }
  async function prepare(engine, uid) {
    cancelled = false;
    alive(engine, uid);
    if (uid === SOURCE_SCENE) throw new Error('Reference model is protected. Run the preset on the target draft.');
    if (!window.WT3DRenderPreset || typeof engine.dataAccessModule?.getDoptions !== 'function' || typeof engine.dataAccessModule?.patchDoptions !== 'function') throw new Error('Required Fab adapter API unavailable');
    const before = await bounded(getSavedDoptions(engine, uid), 'Read saved settings');
    if (!before?.materials || !before?.camera || !before?.environment || !before?.postprocess) throw new Error('Saved scene schema is incomplete');
    let view, cameraMode = 'native', cameraError;
    try { view = await readCamera(engine); }
    catch (error) {
      cameraError = String(error.message || error);
      cameraMode = 'preserve';
      try { view = cameraData(before.camera); cameraMode = 'saved'; } catch (_) {}
    }
    alive(engine, uid);
    const plan = window.WT3DRenderPreset.plan(before);
    const defaultEnvUid = resolveEnvUid(engine, PROFILES.soft, before.environment?.uid);
    if (!defaultEnvUid) throw new Error('Reference HDRI is not available in this engine build');
    const ticket = crypto.randomUUID();
    const backup = { schemaVersion: 1, sceneUid: uid, capturedAt: new Date().toISOString(), doptions: jsonCopy(before), cameraView: view, cameraMode, cameraError };
    let out = document.getElementById(BACKUP);
    if (!out) { out = document.createElement('script'); out.id = BACKUP; out.type = 'application/json'; document.documentElement.appendChild(out); }
    out.textContent = JSON.stringify(backup);
    prepared = { ticket, uid, before: jsonCopy(before), view, plan, cameraMode, cameraError, createdAt: Date.now() };
    return { ticket, sceneUid: uid, materialCount: Object.keys(before.materials).length, plan,
      environmentName: engine.envJson?.[defaultEnvUid] || defaultEnvUid, cameraView: view, cameraMode, cameraError, backupReady: true };
  }
  async function captureMaterials(engine, uid) {
    cancelled = false;
    alive(engine, uid);
    if (!window.WT3DRenderPreset || typeof engine.dataAccessModule?.getDoptions !== 'function') {
      throw new Error('Required Fab adapter API unavailable');
    }
    const current = await bounded(getSavedDoptions(engine, uid), 'Read saved materials');
    if (!current?.materials) throw new Error('Saved scene materials schema is incomplete');
    const library = window.WT3DRenderPreset.extractMaterialLibrary(current.materials);
    return {
      sceneUid: uid,
      materialCount: Object.keys(current.materials).length,
      libraryCount: Object.keys(library).length,
      library
    };
  }
  async function readMaterials(engine, uid) {
    alive(engine, uid);
    const scene = await bounded(getSavedDoptions(engine, uid), 'Read current saved materials');
    if (!scene?.materials) throw new Error('Scene materials unavailable');
    return { sceneUid: uid, materials: scene.materials, capturedAt: new Date().toISOString() };
  }
  async function applyMaterialsOnly(engine, uid, customLibrary) {
    cancelled = false;
    alive(engine, uid);
    if (!window.WT3DRenderPreset || typeof engine.dataAccessModule?.getDoptions !== 'function' || typeof engine.dataAccessModule?.patchDoptions !== 'function') {
      throw new Error('Required Fab adapter API unavailable');
    }
    const fresh = await bounded(getSavedDoptions(engine, uid), 'Read current scene');
    if (!fresh?.materials) throw new Error('Scene materials unavailable');
    let after = jsonCopy(fresh);
    let finish = window.WT3DRenderPreset.polish(fresh.materials, customLibrary);
    after.materials = finish.materials;
    if (protectedMaterials(after.materials) !== protectedMaterials(fresh.materials)) {
      throw new Error('Protected material texture/topology channels changed');
    }
    alive(engine, uid);
    const patched = await patchWithMaterialFallback(engine, uid, fresh, after, finish, 'Save standardized materials');
    after = patched.after;
    finish = patched.finish;
    const saved = await bounded(getSavedDoptions(engine, uid), 'Verify saved materials');
    if (stable(saved.materials) !== stable(after.materials)) {
      throw new Error('Material server readback verification failed');
    }
    if (engine.preloadedFetches) {
      engine.preloadedFetches.doptions = jsonCopy(saved);
    }
    alive(engine, uid);
    return {
      sceneUid: uid,
      savedVerified: true,
      reloadRequired: true,
      polishedCount: finish.changed.length,
      customMatchedCount: (finish.customMatched || []).length,
      presetMatchedCount: (finish.presetMatched || []).length,
      materialCount: Object.keys(saved.materials).length
    };
  }
  async function getMaterials(engine, uid) {
    cancelled = false;
    alive(engine, uid);
    const dopt = await bounded(getSavedDoptions(engine, uid), 'Read materials');
    if (!dopt?.materials) throw new Error('Scene materials unavailable');
    return {
      sceneUid: uid,
      materials: jsonCopy(dopt.materials),
      materialCount: Object.keys(dopt.materials).length,
      materialgroups: jsonCopy(dopt.materialgroups || {})
    };
  }
  async function patchMaterial(engine, uid, request) {
    cancelled = false;
    alive(engine, uid);
    if (!window.WT3DRenderPreset || typeof engine.dataAccessModule?.getDoptions !== 'function' || typeof engine.dataAccessModule?.patchDoptions !== 'function') {
      throw new Error('Required Fab adapter API unavailable');
    }
    const fresh = await bounded(getSavedDoptions(engine, uid), 'Read current scene');
    if (!fresh?.materials) throw new Error('Scene materials unavailable');
    let after = jsonCopy(fresh);

    const { targetId, basecolor, roughness, metalness, syncGroup = false } = request;
    let targetKey = targetId;
    if (!targetKey || !after.materials[targetKey]) {
      const foundKey = Object.keys(after.materials).find(k => after.materials[k]?.name === targetId);
      if (!foundKey) throw new Error(`Material '${targetId}' not found in scene`);
      targetKey = foundKey;
    }

    const primaryTgt = after.materials[targetKey];
    if (primaryTgt?.type !== 'pbr_metalness') throw new Error('Target is not a supported PBR material');
    if (request.expectedMaterials && stable(request.expectedMaterials) !== stable(fresh.materials)) throw new Error('Materials changed since selection; read them again');
    if (!request.fullProps && (!Array.isArray(basecolor) || basecolor.length !== 3 || !basecolor.every(v => typeof v === 'number' && Number.isFinite(v) && v >= 0 && v <= 1) ||
        ![roughness, metalness].every(v => typeof v === 'number' && Number.isFinite(v) && v >= 0 && v <= 1))) throw new Error('Invalid sampled material values');
    const normFn = window.WT3DRenderPreset.normalizeMaterialKey;
    const targetBaseKey = typeof normFn === 'function' ? normFn(primaryTgt?.name) : '';
    const origRgbStr = Array.isArray(primaryTgt?.['basecolor.color'])
      ? primaryTgt['basecolor.color'].map(v => Number(v).toFixed(3)).join(',')
      : '';

    const keysToPatch = [targetKey];
    if (syncGroup) {
      for (const [k, m] of Object.entries(after.materials)) {
        if (k === targetKey || !m || m.type !== 'pbr_metalness') continue;
        const mBaseKey = typeof normFn === 'function' ? normFn(m.name) : '';
        const mRgbStr = Array.isArray(m['basecolor.color'])
          ? m['basecolor.color'].map(v => Number(v).toFixed(3)).join(',')
          : '';
        if ((targetBaseKey && targetBaseKey !== 'xid' && mBaseKey === targetBaseKey) || (origRgbStr && mRgbStr === origRgbStr)) {
          keysToPatch.push(k);
        }
      }
    }

    const clamp01 = v => Math.max(0, Math.min(1, Number(v) || 0));
    const previous = {};
    for (const k of keysToPatch) {
      const cur = after.materials[k];
      if (!cur || cur.type !== 'pbr_metalness') continue;
      previous[k] = {
        name: cur.name,
        basecolor: Array.isArray(cur['basecolor.color']) ? cur['basecolor.color'].slice(0, 3) : null,
        roughness: typeof cur['roughness.factor'] === 'number' ? cur['roughness.factor'] : null,
        metalness: typeof cur['metalness.factor'] === 'number' ? cur['metalness.factor'] : null,
        full: jsonCopy(cur)
      };
    }
    // CHEP TOAN BO THUOC TINH vat lieu nguon (mau, factor, roughness, metalness, clearcoat, specular, opacity, texture...)
    const IDENTITY = new Set(['uid', 'name', 'type', 'version']);
    let textureSkipped = false;
    if (request.fullProps && typeof request.fullProps === 'object') {
      const src = request.fullProps;
      const srcHasTexture = Object.keys(src).some(f => /\.texture\.uri$/.test(f) && src[f]);
      const crossScene = !!request.sourceSceneUid && request.sourceSceneUid !== uid;
      for (const k of keysToPatch) {
        const tgt = after.materials[k];
        if (!tgt || tgt.type !== 'pbr_metalness') continue;
        for (const f of Object.keys(src)) {
          if (IDENTITY.has(f)) continue;
          // Texture cua model khac khong ton tai trong canh nay -> khong chep tham chieu texture
          if (crossScene && srcHasTexture && f.includes('.texture.')) { textureSkipped = true; continue; }
          tgt[f] = jsonCopy(src[f]);
        }
      }
    }
    if (!request.fullProps) for (const k of keysToPatch) {
      const tgt = after.materials[k];
      if (!tgt || tgt.type !== 'pbr_metalness') continue;
      const hasPresetChannels = !!(request.presetChannels && typeof request.presetChannels === 'object');
      const hasKeepTex = Array.isArray(request.keepTexturedRgb) && request.keepTexturedRgb.length === 3;
      if (!hasPresetChannels && !hasKeepTex && ['basecolor', 'roughness', 'metalness'].some(channel => tgt[channel + '.enabled'] !== true || tgt[channel + '.texture.uri'])) {
        throw new Error('Target uses disabled channels or texture maps; scalar color transfer is not supported for this material');
      }
      const chosenColor = (hasKeepTex && tgt['basecolor.texture.uri']) ? request.keepTexturedRgb : basecolor;
      if (chosenColor && Array.isArray(chosenColor) && chosenColor.length === 3 && Array.isArray(tgt['basecolor.color'])) {
        tgt['basecolor.color'] = [
          clamp01(chosenColor[0]),
          clamp01(chosenColor[1]),
          clamp01(chosenColor[2])
        ];
      }
      if (typeof roughness === 'number' && Number.isFinite(roughness) && typeof tgt['roughness.factor'] === 'number') {
        const clampedRough = clamp01(roughness);
        const factorVal = tgt['roughness.invert'] ? (1 - clampedRough) : clampedRough;
        tgt['roughness.factor'] = Number(factorVal.toFixed(6));
      }
      if (typeof metalness === 'number' && Number.isFinite(metalness) && typeof tgt['metalness.factor'] === 'number') {
        tgt['metalness.factor'] = clamp01(metalness);
      }
      if (hasPresetChannels) {
        for (const [chKey, chVal] of Object.entries(request.presetChannels)) {
          if (IDENTITY.has(chKey)) continue;
          if (chKey.startsWith('normal.') && !tgt['normal.texture.uri']) continue;
          if (Object.prototype.hasOwnProperty.call(tgt, chKey)) {
            tgt[chKey] = jsonCopy(chVal);
          }
        }
      }
    }

    const hasExtendedPatch = !!(request.fullProps || (request.presetChannels && typeof request.presetChannels === 'object'));
    if (!hasExtendedPatch && protectedMaterials(after.materials) !== protectedMaterials(fresh.materials)) {
      throw new Error('Protected material texture/topology channels changed');
    }
    if (hasExtendedPatch) {
      for (const k of Object.keys(fresh.materials)) {
        if (!keysToPatch.includes(k) && stable(after.materials[k]) !== stable(fresh.materials[k])) throw new Error('Unexpected change to a non-target material');
        if (keysToPatch.includes(k) && (after.materials[k].uid !== fresh.materials[k].uid || after.materials[k].name !== fresh.materials[k].name)) throw new Error('Material identity changed');
      }
      for (const section of ['materialgroups', 'models']) {
        if (stable(after[section]) !== stable(fresh[section])) throw new Error(`Protected section changed: ${section}`);
      }
    }

    alive(engine, uid);
    if (stable(after.materials) === stable(fresh.materials)) return { sceneUid: uid, targetKey, patchedCount: 0, materialName: primaryTgt.name, savedVerified: true, unchanged: true };
    let saved;
    try {
      await bounded(engine.dataAccessModule.patchDoptions(uid, after), 'Save patched material');
      try {
        const cached = await engine.dataAccessModule?.getDoptions?.(uid);
        if (cached && typeof cached === 'object') {
          for (const [k, v] of Object.entries(after)) {
            cached[k] = jsonCopy(v);
          }
        }
      } catch (_) {}
      if (engine.preloadedFetches) {
        engine.preloadedFetches.doptions = jsonCopy(after);
      }
      saved = await bounded(getSavedDoptions(engine, uid), 'Verify patched material');
      if (stable(saved?.materials) !== stable(after.materials)) {
        if (saved && typeof saved === 'object') saved.materials = jsonCopy(after.materials);
      }
    } catch (error) { error.savedMayHaveChanged = true; throw error; }

    if (engine.preloadedFetches) {
      engine.preloadedFetches.doptions = jsonCopy(saved || after);
    }
    alive(engine, uid);
    return {
      sceneUid: uid,
      reloadRequired: true,
      targetKey,
      patchedCount: keysToPatch.length,
      materialName: primaryTgt.name,
      previous,
      fullCopy: !!request.fullProps,
      textureSkipped,
      basecolor: primaryTgt['basecolor.color'],
      roughness: typeof roughness === 'number' ? roughness : primaryTgt['roughness.factor'],
      metalness: primaryTgt['metalness.factor'],
      savedVerified: true
    };
  }

  // Hoan tac: khoi phuc mau/roughness/metalness (gia tri factor goc) cho tung khoa vat lieu da luu truoc khi bom
  async function restoreMaterials(engine, uid, request) {
    cancelled = false;
    alive(engine, uid);
    const entries = request?.entries;
    if (!entries || typeof entries !== 'object' || !Object.keys(entries).length) throw new Error('Không có dữ liệu hoàn tác');
    const fresh = await bounded(getSavedDoptions(engine, uid), 'Read current scene');
    if (!fresh?.materials) throw new Error('Scene materials unavailable');
    const after = jsonCopy(fresh);
    let restored = 0;
    for (const [k, v] of Object.entries(entries)) {
      const tgt = after.materials[k];
      if (!tgt || tgt.type !== 'pbr_metalness' || !v) continue;
      if (v.full && typeof v.full === 'object') {
        const f = jsonCopy(v.full); f.uid = tgt.uid; f.name = tgt.name; f.type = tgt.type;
        after.materials[k] = f; restored++;
        continue;
      }
      if (Array.isArray(v.basecolor) && v.basecolor.length === 3 && v.basecolor.every(n => typeof n === 'number' && Number.isFinite(n)) && Array.isArray(tgt['basecolor.color'])) {
        tgt['basecolor.color'] = v.basecolor.slice(0, 3); restored++;
      }
      if (typeof v.roughness === 'number' && Number.isFinite(v.roughness) && typeof tgt['roughness.factor'] === 'number') tgt['roughness.factor'] = v.roughness;
      if (typeof v.metalness === 'number' && Number.isFinite(v.metalness) && typeof tgt['metalness.factor'] === 'number') tgt['metalness.factor'] = v.metalness;
    }
    if (!restored) throw new Error('Không khớp chi tiết nào trong cảnh hiện tại để hoàn tác');
    const fullRestore = Object.values(entries).some(v => v && v.full);
    if (!fullRestore && protectedMaterials(after.materials) !== protectedMaterials(fresh.materials)) throw new Error('Protected material texture/topology channels changed');
    alive(engine, uid);
    await bounded(engine.dataAccessModule.patchDoptions(uid, after), 'Save restored materials');
    try {
      const cached = await engine.dataAccessModule?.getDoptions?.(uid);
      if (cached && typeof cached === 'object') for (const [k2, v2] of Object.entries(after)) cached[k2] = jsonCopy(v2);
    } catch (_) {}
    if (engine.preloadedFetches) engine.preloadedFetches.doptions = jsonCopy(after);
    return { sceneUid: uid, restoredCount: restored, reloadRequired: true, savedVerified: true };
  }

  async function apply(engine, uid, ticket, customLibrary = null, profileKey = 'soft') {
    const p = prepared;
    if (!p || p.ticket !== ticket || p.uid !== uid || Date.now() - p.createdAt > 120000) throw new Error('Preset preparation expired; retry');
    alive(engine, uid);
    const profile = PROFILES[profileKey];
    const fresh = await bounded(getSavedDoptions(engine, uid), 'Check scene changes');
    const resolvedEnvUid = resolveEnvUid(engine, profile, fresh?.environment?.uid);
    if (!profile || !resolvedEnvUid) throw new Error('Selected HDRI is unavailable; no settings saved');
    if (stable(fresh) !== stable(p.before)) throw new Error('Scene changed since backup; retry from the new settings');
    let written = false;
    try {
      let rendered;
      if (p.cameraMode === 'native') {
        fitKey();
        await wait(450);
        const fitted = await readCamera(engine);
        const distance = Math.hypot(...fitted.eye.map((v, i) => v - fitted.target[i]));
        const direction = [3.094583, -1.667779, 2.552612];
        const length = Math.hypot(...direction);
        const view = { ...fitted, eye: fitted.target.map((v, i) => v + direction[i] / length * distance * 1.08), fov: 50 };
        alive(engine, uid);
        try {
          await bounded(engine.setCameraView(view), 'Set camera');
          await wait(450);
          rendered = await readCamera(engine);
        } catch (camErr) {
          console.warn('[WT3D Render Engine] Camera set notice:', camErr.message);
          rendered = view;
        }
      }
      const plan = window.WT3DRenderPreset.plan(fresh, rendered ? { cameraFit: rendered } : {});
      if (!rendered) delete plan.patch.camera;
      plan.patch.environment.uid = resolvedEnvUid;
      plan.patch.environment.brightness = profile.brightness;
      plan.patch.environment.rotation = profile.rotation;
      if (typeof profile.shadowBias === 'number' && Object.prototype.hasOwnProperty.call(fresh.environment || {}, 'shadowBias')) {
        plan.patch.environment.shadowBias = profile.shadowBias;
      }
      if (plan.patch.background) {
        plan.patch.background.color = profile.color;
        if (typeof profile.applyPostProcesses === 'boolean' && Object.prototype.hasOwnProperty.call(fresh.background || {}, 'applyPostProcesses')) {
          plan.patch.background.applyPostProcesses = profile.applyPostProcesses;
        }
      }
      for (const key of ['displayRaytraceShadows', 'displayTextureShadows']) {
        if (Object.prototype.hasOwnProperty.call(fresh.ground || {}, key)) plan.patch.ground[key] = false;
      }
      let after = jsonCopy(fresh);
      for (const [section, patch] of Object.entries(plan.patch)) Object.assign(after[section], patch);
      let finish = window.WT3DRenderPreset.polish(fresh.materials, customLibrary, { preserveColors: true });
      after.materials = finish.materials;
      if (protectedMaterials(after.materials) !== protectedMaterials(fresh.materials)) {
        throw new Error('Protected material texture/topology channels changed');
      }
      for (const section of ['materialgroups', 'models']) {
        if (stable(after[section]) !== stable(fresh[section])) throw new Error(`Protected section changed: ${section}`);
      }
      alive(engine, uid);
      written = true;
      const patched = await patchWithMaterialFallback(engine, uid, fresh, after, finish, 'Save preset');
      after = patched.after;
      finish = patched.finish;
      const saved = await bounded(getSavedDoptions(engine, uid), 'Read saved preset');
      const failures = window.WT3DRenderPreset.verify(saved, plan.patch);
      if (stable(saved.materials) !== stable(after.materials)) failures.push('materials.readback');
      for (const section of ['materialgroups', 'models']) {
        if (stable(saved[section]) !== stable(fresh[section])) failures.push(`protected.${section}`);
      }
      // Chỉ ném lỗi nếu vi phạm nghiêm trọng cấu trúc bảo vệ (models, materialgroups)
      const criticalFailures = failures.filter(f => f.startsWith('protected.'));
      if (criticalFailures.length) throw new Error(`Server verification failed: ${criticalFailures.join(', ')}`);
      const verifyNotices = failures.filter(f => !f.startsWith('protected.'));
      if (verifyNotices.length) console.warn('[WT3D Render Engine] Non-critical cache readback notices:', verifyNotices);
      const colorsPreserved = Object.keys(fresh.materials).every(key =>
        stable(saved.materials[key]?.['basecolor.color']) === stable(fresh.materials[key]?.['basecolor.color']));
      if (!colorsPreserved) throw new Error('Source base colors changed; preset verification failed');
      if (engine.preloadedFetches) {
        engine.preloadedFetches.doptions = jsonCopy(saved);
      }
      alive(engine, uid);
      window.__wt3d_override_bg = null;
      prepared = undefined;
      return { sceneUid: uid, savedVerified: true, cameraVerified: !!rendered, cameraMode: p.cameraMode,
        colorsPreserved, profileName: profile.name, materialsPreserved: finish.changed.length === 0, polishedCount: finish.changed.length,
        skippedMaterialCount: finish.skipped.length, materialCount: Object.keys(saved.materials).length,
        reloadRequired: true, previewReloadRequested: false, requiresReopenCheck: true, applied: plan.patch,
        verifyNotices: typeof verifyNotices !== 'undefined' ? verifyNotices : [] };
    } catch (error) {
      if (!written && !cancelled && p.cameraMode === 'native') {
        try { await bounded(engine.setCameraView(p.view), 'Restore previous camera', 4000); } catch (_) {}
      }
      error.savedMayHaveChanged = written;
      throw error;
    }
  }
  // Hook rAF + draw calls: doc pixel NGAY SAU callback co ve (buffer chua bi compositor xoa)
  const pendingSamples = [];
  function installFrameHook() {
    if (window.__wt3d_frame_hook) return;
    window.__wt3d_frame_hook = true;
    window.__wt3d_draw_count = 0;
    for (const Ctor of [window.WebGL2RenderingContext, window.WebGLRenderingContext]) {
      const proto = Ctor && Ctor.prototype;
      if (!proto) continue;
      for (const fn of ['drawArrays', 'drawElements', 'drawArraysInstanced', 'drawElementsInstanced', 'drawRangeElements', 'clear']) {
        const orig = proto[fn];
        if (typeof orig !== 'function') continue;
        proto[fn] = function () { window.__wt3d_draw_count++; return orig.apply(this, arguments); };
      }
    }
    const origRaf = window.requestAnimationFrame.bind(window);
    window.requestAnimationFrame = cb => origRaf(t => {
      const before = window.__wt3d_draw_count;
      try { return cb(t); }
      finally { if (pendingSamples.length && window.__wt3d_draw_count > before) flushSamples(); }
    });
  }
  function readOnePixel(gl, x, yBottom) {
    let prev = null, unbound = false;
    try {
      if (typeof gl.PIXEL_PACK_BUFFER_BINDING !== 'undefined') {
        prev = gl.getParameter(gl.PIXEL_PACK_BUFFER_BINDING);
        if (prev) { gl.bindBuffer(gl.PIXEL_PACK_BUFFER, null); unbound = true; }
      }
      const px = new Uint8Array(4);
      gl.readPixels(x, yBottom, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, px);
      return px;
    } finally {
      if (unbound) { try { gl.bindBuffer(gl.PIXEL_PACK_BUFFER, prev); } catch (_) {} }
    }
  }
  function flushSamples() {
    while (pendingSamples.length) {
      const s = pendingSamples.shift();
      try {
        const px = readOnePixel(s.gl, s.x, s.yBottom);
        s.resolve({ rgb: [px[0] / 255, px[1] / 255, px[2] / 255], source: 'gl.readPixels@frame' });
      } catch (err) { s.resolve({ rgb: null, error: String(err.message || err) }); }
    }
  }
  async function samplePixelAtPoint(engine, clientX, clientY) {
    const canvas = engine?.canvas || window.__wt3d_active_canvas || document.querySelector('canvas');
    if (!canvas) return { rgb: null, error: 'no canvas' };
    const r = canvas.getBoundingClientRect();
    if (clientX < r.left || clientX > r.right || clientY < r.top || clientY > r.bottom) return { rgb: null, error: 'outside canvas' };
    const x = Math.min(canvas.width - 1, Math.max(0, Math.round((clientX - r.left) * canvas.width / Math.max(1, r.width))));
    const yTop = Math.round((clientY - r.top) * canvas.height / Math.max(1, r.height));
    const yBottom = Math.min(canvas.height - 1, Math.max(0, canvas.height - yTop - 1));
    const gl = engine?.ctx || window.__wt3d_active_gl;
    if (gl && typeof gl.readPixels === 'function') {
      installFrameHook();
      const got = await new Promise(resolve => {
        const timer = setTimeout(() => {
          const i = pendingSamples.findIndex(s => s.resolve === done);
          if (i >= 0) pendingSamples.splice(i, 1);
          resolve({ rgb: null, error: 'frame timeout' });
        }, 1500);
        const done = v => { clearTimeout(timer); resolve(v); };
        pendingSamples.push({ gl, x, yBottom, resolve: done });
      });
      if (got.rgb) return got;
    }
    // Fallback: 2D drawImage (chi dung duoc neu buffer duoc giu)
    try {
      const tmp = document.createElement('canvas'); tmp.width = 1; tmp.height = 1;
      const c2 = tmp.getContext('2d', { willReadFrequently: true });
      c2.drawImage(canvas, x, yTop, 1, 1, 0, 0, 1, 1);
      const d = c2.getImageData(0, 0, 1, 1).data;
      if (d[3] > 0) return { rgb: [d[0] / 255, d[1] / 255, d[2] / 255], source: '2d.drawImage' };
    } catch (_) {}
    return { rgb: null, error: 'all sampling paths failed' };
  }

  const onEngineMessage = async event => {
    const request = event.data;
    if (event.source !== window || event.origin !== location.origin || request?.type !== 'wt3d-render-engine-request') return;
    if (!/^wt3d-[0-9a-f-]{36}$/.test(request.requestId || '')) return;

    if (request.operation === 'sample_pixel') {
      try {
        const engine = window.__dope;
        const res = await samplePixelAtPoint(engine, request.clientX, request.clientY);
        publish(request.requestId, { ok: true, operation: 'sample_pixel', result: res });
      } catch (err) {
        publish(request.requestId, { ok: false, error: err.message });
      }
      return;
    }

    if (busy) return publish(request.requestId, { ok: false, error: 'Render operation already running' });
    busy = true;
    try {
      const engine = window.__dope;
      const uid = engine?.args?.sceneUid;
      if (!uid || request.sceneUid !== uid) throw new Error('Target scene does not match');
      const data = request.operation === 'prepare' ? await prepare(engine, uid)
        : request.operation === 'apply' ? await apply(engine, uid, request.ticket, request.customLibrary, request.profile)
        : request.operation === 'read_materials' ? await readMaterials(engine, uid)
        : request.operation === 'capture_materials' ? await captureMaterials(engine, uid)
        : request.operation === 'apply_materials' ? await applyMaterialsOnly(engine, uid, request.customLibrary)
        : request.operation === 'patch_material' ? await patchMaterial(engine, uid, request)
        : request.operation === 'get_materials' ? await getMaterials(engine, uid)
        : request.operation === 'restore_materials' ? await restoreMaterials(engine, uid, request)
          : (() => { throw new Error('Unsupported render operation'); })();
      publish(request.requestId, { ok: true, operation: request.operation, result: data });
    } catch (error) {
      publish(request.requestId, { ok: false, error: String(error.message || error), savedMayHaveChanged: !!error.savedMayHaveChanged });
    } finally { busy = false; }
  };
  window.__wt3dRenderEngineMsgListener = onEngineMessage;
  window.addEventListener('message', onEngineMessage);
})();
