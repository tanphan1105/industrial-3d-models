// color-bridge.js - MAIN WORLD: Dope Engine + WebGL Context Controller (Zero-Lag & Low-RAM)
// WT3D Fab Extension v3.9.54
(function() {
    'use strict';

    if (window.__wt3d_color_bridge_loaded) return;
    window.__wt3d_color_bridge_loaded = true;

    // Biến toàn cục lưu màu ghi đè: null hoặc Float32Array([r, g, b, 1.0])
    window.__wt3d_override_bg = null;

    // =========================================================================
    // 🛡️ TẦNG 1: HOOK WEBGL PROTOTYPES (CHỈ CAN THIỆP KHI CÓ OVERRIDE_BG)
    // =========================================================================
    function installWebGLHooks() {
        if (window.__wt3d_webgl_hooks_installed) return;
        window.__wt3d_webgl_hooks_installed = true;

        const hookClearColor = (proto) => {
            if (!proto || !proto.clearColor) return;
            const original = proto.clearColor;
            proto.clearColor = function(r, g, b, a) {
                const bg = window.__wt3d_override_bg;
                if (bg) {
                    try {
                        if (this.getParameter(this.FRAMEBUFFER_BINDING) === null) {
                            return original.call(this, bg[0], bg[1], bg[2], bg[3]);
                        }
                    } catch(_) {}
                }
                return original.call(this, r, g, b, a);
            };
        };

        const hookClear = (proto) => {
            if (!proto || !proto.clear) return;
            const originalClear = proto.clear;
            const originalClearColor = proto.clearColor;
            proto.clear = function(mask) {
                const bg = window.__wt3d_override_bg;
                if (bg && (mask & this.COLOR_BUFFER_BIT)) {
                    try {
                        if (this.getParameter(this.FRAMEBUFFER_BINDING) === null) {
                            originalClearColor.call(this, bg[0], bg[1], bg[2], bg[3]);
                        }
                    } catch(_) {}
                }
                return originalClear.call(this, mask);
            };
        };

        if (typeof WebGLRenderingContext !== 'undefined') {
            hookClearColor(WebGLRenderingContext.prototype);
            hookClear(WebGLRenderingContext.prototype);
        }
        if (typeof WebGL2RenderingContext !== 'undefined') {
            hookClearColor(WebGL2RenderingContext.prototype);
            hookClear(WebGL2RenderingContext.prototype);

            const origClearBufferfv = WebGL2RenderingContext.prototype.clearBufferfv;
            if (origClearBufferfv) {
                WebGL2RenderingContext.prototype.clearBufferfv = function(buffer, drawbuffer, values, srcOffset) {
                    const bg = window.__wt3d_override_bg;
                    if (bg && buffer === this.COLOR && drawbuffer === 0) {
                        try {
                            if (this.getParameter(this.FRAMEBUFFER_BINDING) === null) {
                                return origClearBufferfv.call(this, buffer, drawbuffer, bg, 0);
                            }
                        } catch(_) {}
                    }
                    return origClearBufferfv.apply(this, arguments);
                };
            }
        }

        // Lưu tham chiếu WebGL context nhẹ nhàng, KHÔNG ép preserveDrawingBuffer:true để tránh ngốn VRAM/RAM ở 60FPS
        if (typeof HTMLCanvasElement !== 'undefined' && !HTMLCanvasElement.prototype.__wt3d_hooked) {
            HTMLCanvasElement.prototype.__wt3d_hooked = true;
            const origGetContext = HTMLCanvasElement.prototype.getContext;
            HTMLCanvasElement.prototype.getContext = function(type, attributes) {
                const ctx = origGetContext.call(this, type, attributes);
                if (ctx && typeof type === 'string' && type.toLowerCase().includes('webgl')) {
                    window.__wt3d_active_gl = ctx;
                    window.__wt3d_active_canvas = this;
                }
                return ctx;
            };
        }
    }

    installWebGLHooks();

    // =========================================================================
    // 🎨 TẦNG 2: ĐIỀU KHIỂN TRỰC TIẾP DOPE ENGINE (MEMORY + PATCH)
    // =========================================================================
    async function applyEngineBackground(targetHex) {
        const raw = String(targetHex || '#FFFFFF').replace('#', '').toUpperCase();
        const r = parseInt(raw.substr(0, 2), 16) / 255;
        const g = parseInt(raw.substr(2, 2), 16) / 255;
        const b = parseInt(raw.substr(4, 2), 16) / 255;

        window.__wt3d_override_bg = new Float32Array([r, g, b, 1.0]);

        try {
            const dope = window.__dope;
            const ctx = dope?.ctx || window.__wt3d_active_gl;
            if (ctx) {
                ctx.clearColor(r, g, b, 1.0);
                ctx.clear(ctx.COLOR_BUFFER_BIT);
            }
        } catch(_) {}

        const dope = window.__dope;
        if (!dope) return true;

        try {
            if (dope.preloadedFetches?.doptions?.background) {
                dope.preloadedFetches.doptions.background.type = 'COLOR';
                dope.preloadedFetches.doptions.background.color = [r, g, b];
                dope.preloadedFetches.doptions.background.enabled = true;
            }
        } catch(_) {}

        try {
            const uid = dope.args?.sceneUid;
            if (uid && dope.dataAccessModule?.patchDoptions) {
                let cur = dope.preloadedFetches?.doptions;
                if ((!cur || !cur.materials) && typeof dope.dataAccessModule.getDoptions === 'function') {
                    try { cur = await dope.dataAccessModule.getDoptions(uid); } catch(_) {}
                }
                if (cur && typeof cur === 'object' && cur.background) {
                    const fullBg = Object.assign({}, cur.background, { type: 'COLOR', color: [r, g, b], enabled: true });
                    const fullPayload = JSON.parse(JSON.stringify(Object.assign({}, cur, { background: fullBg })));
                    await dope.dataAccessModule.patchDoptions(uid, fullPayload);
                }
            }
        } catch(_) {}

        return true;
    }

    document.addEventListener('wt3d-inject-color', async function(e) {
        const targetHex = (e.detail || {}).hex || '#FFFFFF';
        if (window === window.top) return;
        await applyEngineBackground(targetHex);
        document.dispatchEvent(new CustomEvent('wt3d-color-result', { detail: { success: true, hex: targetHex } }));
    });

    async function applyEnginePreset(prof) {
        if (!prof || typeof prof !== 'object') return false;
        const dope = window.__dope;
        const bgType = prof.bgType || 'environment';
        if (bgType === 'environment') {
            window.__wt3d_override_bg = null;
        } else {
            let targetHex = '#FFFFFF';
            if (bgType === 'clean_light') targetHex = '#F5F5F7';
            else if (bgType === 'clean_dark') targetHex = '#18181B';
            await applyEngineBackground(targetHex);
        }

        if (!dope || !dope.preloadedFetches?.doptions) return true;
        const dopt = dope.preloadedFetches.doptions;

        try {
            if (dopt.environment) {
                dopt.environment.enabled = true;
                if (typeof prof.brightness === 'number') dopt.environment.brightness = prof.brightness;
                if (typeof prof.orientation === 'number') {
                    dopt.environment.rotation = Number(((prof.orientation * Math.PI) / 180).toFixed(4));
                }
            }
            if (dopt.background) {
                dopt.background.enabled = true;
                dopt.background.type = bgType === 'environment' ? 'ENVIRONMENT' : 'COLOR';
            }
            if (dopt.ground) {
                dopt.ground.enabled = true;
                dopt.ground.displayAO = true;
                if (typeof prof.groundIntensity === 'number') dopt.ground.intensity = prof.groundIntensity;
            }
            if (dopt.camera) {
                dopt.camera.fov = typeof prof.fov === 'number' ? prof.fov : 50;
                dopt.camera.autoExposure = false;
            }
            if (dopt.postprocess) {
                dopt.postprocess.useDOF = false;
                dopt.postprocess.useGrain = false;
                dopt.postprocess.useChroma = false;
                dopt.postprocess.useSSAO = true;
                if (typeof prof.occlusionIntensity === 'number') dopt.postprocess.ssaoIntensity = prof.occlusionIntensity;
                if (typeof prof.occlusionBias === 'number') dopt.postprocess.ssaoBias = prof.occlusionBias;
                dopt.postprocess.useVignette = !!prof.vignette;
                dopt.postprocess.useBloom = (typeof prof.bloomIntensity === 'number' && prof.bloomIntensity > 0);
                if (typeof prof.bloomIntensity === 'number') dopt.postprocess.bloomFactor = prof.bloomIntensity;
                dopt.postprocess.useToneMapping = true;
                dopt.postprocess.useTAA = true;
                dopt.postprocess.useFXAA = true;
            }

            const uid = dope.args?.sceneUid;
            if (uid && typeof dope.dataAccessModule?.patchDoptions === 'function') {
                await dope.dataAccessModule.patchDoptions(uid, Object.assign({}, dopt));
            }
        } catch (_) {}
        return true;
    }

    window.addEventListener('message', function(e) {
        if (e.data?.type === 'wt3d-set-background') {
            applyEngineBackground(e.data.hex || '#FFFFFF');
        } else if (e.data?.type === 'wt3d-set-background-env') {
            window.__wt3d_override_bg = null;
            try {
                const dope = window.__dope;
                if (dope?.preloadedFetches?.doptions?.background) {
                    dope.preloadedFetches.doptions.background.type = 'ENVIRONMENT';
                    dope.preloadedFetches.doptions.background.enabled = true;
                    const uid = dope.args?.sceneUid;
                    if (uid && typeof dope.dataAccessModule?.patchDoptions === 'function') {
                        dope.dataAccessModule.patchDoptions(uid, Object.assign({}, dope.preloadedFetches.doptions));
                    }
                }
            } catch (_) {}
        } else if (e.data?.type === 'wt3d-apply-preset') {
            applyEnginePreset(e.data.profile);
        }
    });
})();
