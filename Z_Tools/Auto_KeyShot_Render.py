# -*- coding: utf-8 -*-
# ==============================================================================
# 🚀 NIGHT-CRAWLER KEYSHOT BATCH RENDER ENGINE v3.2 — MASTER EDITION
# Tác giả  : TANPHAN STUDIO x ANTIGRAVITY AI
# Dành cho : Hệ thống lọc nước RO & Thiết bị lọc công nghiệp
#
# Changelog v3.3 (so với v3.2):
# [BUG-1]  setup_environment() — setBackgroundColor float 0..1 thay int 0..255
# [BUG-2]  smart_render() — tách renderImage() ra khỏi _preserve_camera() context
# [BUG-3]  setup_camera() — _CAMERA_DEF_MAP dict 1 lần ngoài function, không dict() mỗi call
# [WARN-1] setup_environment() — HDRI rotation theo camera azimuth (rim light 135° sau cam)
# [WARN-2] _SHADER_MAP — bổ sung "Plastic Fitting Dark Gray", "Polished Stainless Steel"
# [WARN-3] DRAFT_PRECHECK — chia 4 thay chia 6 (960x540 thay 640x360)
# [WARN-5] Xóa _detect_transparent_housing() không dùng
# ==============================================================================

import lux
import os
import re
import math
import datetime
import glob
import json
import time
import traceback
import ctypes
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

# ==============================================================================
# ▶ GLOBAL CONFIG
# ==============================================================================
OUTPUT_DIR        = r"d:\WT3D_Project\Preview_Image"
AUTO_RENDER_MODE  = "OFF"       # "OFF" | "HERO" | "ALL_CAMERAS"
OUTPUT_MODE       = "WEBSITE"   # "WEBSITE" | "CATALOG" | "DATASHEET" | "AR"
RENDER_QUALITY    = "PREVIEW"   # "DRAFT" | "PREVIEW" | "FINAL" | "ULTRA"
EXPORT_WEB_AR     = False
RENDER_WIDTH      = 3840
RENDER_HEIGHT     = 2160
TIMESTAMP_FOLDER  = True
RESUME_RENDER     = True
DRAFT_PRECHECK    = True
SNAPSHOT_MODE     = "OFF"       # "OFF" | "SAVE" | "LOAD"
SNAPSHOT_FILE     = r"d:\WT3D_Project\Z_Tools\night_crawler_snapshot.json"

# ───────────────────────────────────────────────────────────────
# ▶ DEBUG: ĐẶT True để dump toàn bộ lux API ra Console rồi TắT lại
# ───────────────────────────────────────────────────────────────
DEBUG_LUX_API     = False

# ==============================================================================
# ▶ VALIDATION
# ==============================================================================
_VALID = {
    "AUTO_RENDER_MODE": {"OFF", "HERO", "ALL_CAMERAS"},
    "OUTPUT_MODE":      {"WEBSITE", "CATALOG", "DATASHEET", "AR"},
    "RENDER_QUALITY":   {"DRAFT", "PREVIEW", "FINAL", "ULTRA"},
    "SNAPSHOT_MODE":    {"OFF", "SAVE", "LOAD"},
}

def _validate_config() -> None:
    errors = [
        f"{k}='{v}' không hợp lệ. Dùng: {_VALID[k]}"
        for k, v in [
            ("AUTO_RENDER_MODE", AUTO_RENDER_MODE),
            ("OUTPUT_MODE",      OUTPUT_MODE),
            ("RENDER_QUALITY",   RENDER_QUALITY),
            ("SNAPSHOT_MODE",    SNAPSHOT_MODE),
        ]
        if v not in _VALID[k]
    ]
    if errors:
        for e in errors:
            print(f"[CONFIG ERROR] ❌ {e}")
        raise ValueError(f"Config không hợp lệ — fix {len(errors)} lỗi trên trước khi chạy.")

# ==============================================================================
# ▶ LOGGER
# ==============================================================================
_LOG_PREFIX = {
    "INFO":  "  ·", "OK":   " ✅", "WARN": " ⚠️ ", "ERR":  " ❌",
    "HEAD":  "🚀",  "CAM":  "📸", "LIGHT":"💡",   "MAT":  "🎨",
    "REND":  "⚙️ ", "FILM": "🎥", "SNAP": "💾",   "PROG": "▶️ ",
}

def log(level: str, msg: str) -> None:
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {_LOG_PREFIX.get(level, '  ')} {msg}")

# ==============================================================================
# ▶ UTILS
# ==============================================================================
def safe(fn, *args, **kwargs) -> Any:
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        log("WARN", f"safe: {e}")
        return None

def lux_safe(fn_name: str, *args, **kwargs) -> Any:
    """Gọi lux API bằng string name — tránh Early Evaluation crash."""
    try:
        fn = getattr(lux, fn_name)
        return fn(*args, **kwargs)
    except AttributeError:
        log("WARN", f"lux_safe: lux.{fn_name} không tồn tại (Bỏ qua)")
        return None
    except Exception as e:
        log("WARN", f"lux_safe({fn_name}): {e}")
        return None

def normalize(v: Tuple) -> Tuple:
    x, y, z = v
    length = math.sqrt(x*x + y*y + z*z)
    return (x/length, y/length, z/length) if length > 1e-9 else (0.0, 0.0, 1.0)

# ==============================================================================
# ▶ OUTPUT DIR — locked on first call
# ==============================================================================
_OUTPUT_DIR_LOCK: Optional[str] = None

def get_output_dir() -> str:
    global _OUTPUT_DIR_LOCK
    if not _OUTPUT_DIR_LOCK:
        suffix = datetime.datetime.now().strftime("%Y%m%d_%H%M") if TIMESTAMP_FOLDER else ""
        path = os.path.join(OUTPUT_DIR, suffix) if suffix else OUTPUT_DIR
        os.makedirs(path, exist_ok=True)
        _OUTPUT_DIR_LOCK = path
    return _OUTPUT_DIR_LOCK

# ==============================================================================
# ▶ RENDER CONTEXT
# ==============================================================================
QUALITY_PRESETS = {
    "DRAFT":   {"samples":   80, "bounces":  8, "denoise": True,  "denoise_blend": 0.85},
    "PREVIEW": {"samples":  300, "bounces": 16, "denoise": True,  "denoise_blend": 0.95},
    "FINAL":   {"samples":  600, "bounces": 32, "denoise": True,  "denoise_blend": 1.00},
    "ULTRA":   {"samples": 1200, "bounces": 48, "denoise": True,  "denoise_blend": 1.00},
}

@dataclass
class RenderContext:
    """Immutable render configuration — không mutate global state."""
    quality: str
    width:   int
    height:  int

    # [FIX-10] validate ngay khi tạo object, bắt lỗi trước pipeline
    def __post_init__(self):
        if self.quality not in QUALITY_PRESETS:
            raise ValueError(f"RenderContext: quality='{self.quality}' không hợp lệ")
        if self.width <= 0 or self.height <= 0:
            raise ValueError(f"RenderContext: resolution {self.width}x{self.height} không hợp lệ")

    @classmethod
    def from_mode(cls, mode_cfg: Dict) -> "RenderContext":
        return cls(
            quality=mode_cfg["quality"],
            width=mode_cfg["width"],
            height=mode_cfg["height"],
        )

    @classmethod
    def from_globals(cls) -> "RenderContext":
        return cls(quality=RENDER_QUALITY, width=RENDER_WIDTH, height=RENDER_HEIGHT)

    def preset(self) -> Dict:
        return QUALITY_PRESETS[self.quality]

    def __repr__(self) -> str:
        return f"RenderContext(quality={self.quality}, {self.width}x{self.height})"

# ==============================================================================
# ▶ COMMERCIAL MODES
# ==============================================================================
COMMERCIAL_MODES: Dict[str, Dict] = {
    "WEBSITE": {
        "cameras": ["B2B_01_Top_FrontRight", "B2B_05_Low_FrontRight"],
        "quality": "FINAL", "width": 3840, "height": 2160,
        "passes":  ["Beauty", "Depth"],
        "note":    "Hero + macro. Max impact per frame — web hero banner.",
    },
    "CATALOG": {
        "cameras": ["B2B_01_Top_FrontRight", "B2B_09_Ortho_Front",
                    "B2B_11_Ortho_Left", "B2B_05_Low_FrontRight"],
        "quality": "FINAL", "width": 4800, "height": 3200,
        "passes":  ["Beauty", "Depth", "MaterialID", "Normal"],
        "note":    "4 góc chuẩn B2B catalogue kỹ thuật. High-res cho in ấn.",
    },
    "DATASHEET": {
        "cameras": ["B2B_09_Ortho_Front", "B2B_11_Ortho_Left", "B2B_13_Ortho_Top"],
        "quality": "PREVIEW", "width": 2480, "height": 3508,
        "passes":  ["Beauty"],
        "note":    "Tỷ lệ A4. 3 góc kỹ thuật. Đủ cho P&ID / datasheet.",
    },
    "AR": {
        "cameras": ["B2B_01_Top_FrontRight"],
        "quality": "DRAFT", "width": 1920, "height": 1080,
        "passes":  ["Beauty"],
        "note":    "Thumbnail cho AR viewer. Export GLB/USDZ bắt buộc.",
    },
}

AR_FORCE_MODES = {"AR"}

_mode_cfg_cache: Optional[Dict] = None

def get_mode_config() -> Dict:
    global _mode_cfg_cache
    if _mode_cfg_cache is None:
        cfg = COMMERCIAL_MODES.get(OUTPUT_MODE)
        if cfg is None:
            log("WARN", f"OUTPUT_MODE '{OUTPUT_MODE}' không hợp lệ — fallback WEBSITE")
            cfg = COMMERCIAL_MODES["WEBSITE"]
        else:
            log("INFO", f"OUTPUT MODE: {OUTPUT_MODE} — {cfg['note']}")
        _mode_cfg_cache = cfg
    return _mode_cfg_cache

# ==============================================================================
# ▶ SCENE GEOMETRY — cached
# ==============================================================================
_SCENE_BOUNDS_CACHE: Optional[Tuple] = None

def get_scene_bounds() -> Tuple:
    global _SCENE_BOUNDS_CACHE
    if _SCENE_BOUNDS_CACHE is not None:
        return _SCENE_BOUNDS_CACHE

    min_x = min_y = min_z =  float("inf")
    max_x = max_y = max_z = -float("inf")
    has_box = False

    for node in _collect_scene_nodes():
        try:
            bbox = node.getBoundingBox()
            if not bbox or len(bbox) < 2:
                continue
            p0, p1 = bbox[0], bbox[1]
            if not hasattr(p0, "x"):
                continue

            # [FIX-5] Transform multiply bọc riêng — không để crash toàn bbox loop
            try:
                transform = node.getTransform()
                if transform:
                    p0 = p0 * transform
                    p1 = p1 * transform
            except Exception:
                pass  # giữ nguyên p0, p1 local space nếu transform fail

            min_x = min(min_x, min(p0.x, p1.x))
            max_x = max(max_x, max(p0.x, p1.x))
            min_y = min(min_y, min(p0.y, p1.y))
            max_y = max(max_y, max(p0.y, p1.y))
            min_z = min(min_z, min(p0.z, p1.z))
            max_z = max(max_z, max(p0.z, p1.z))
            has_box = True
        except Exception:
            pass

    if not has_box:
        log("WARN", "Không tìm thấy bounding box — dùng fallback (1m cube)")
        _SCENE_BOUNDS_CACHE = (0.0, 0.0, 0.0), 1.0, (1.0, 1.0, 1.0)
    else:
        cx = (min_x + max_x) / 2
        cy = (min_y + max_y) / 2
        cz = (min_z + max_z) / 2
        sx, sy, sz = max_x - min_x, max_y - min_y, max_z - min_z
        _SCENE_BOUNDS_CACHE = (cx, cy, cz), max(sx, sy, sz), (sx, sy, sz)

    log("INFO", f"Scene bounds: center={_SCENE_BOUNDS_CACHE[0]}, max_dim={_SCENE_BOUNDS_CACHE[1]:.3f}")
    return _SCENE_BOUNDS_CACHE

# ==============================================================================
# ▶ SCENE NODE CACHE
# ==============================================================================
_SCENE_NODES_CACHE: Optional[List] = None

def _collect_scene_nodes() -> List:
    global _SCENE_NODES_CACHE
    if _SCENE_NODES_CACHE is None:
        try:
            _SCENE_NODES_CACHE = list(lux.getSceneTree().find())
        except Exception as e:
            log("WARN", f"_collect_scene_nodes: {e}")
            _SCENE_NODES_CACHE = []
    return _SCENE_NODES_CACHE

# ==============================================================================
# ▶ CAMERA SYSTEM
# ==============================================================================
CAMERA_DEFS = [
    # 4 Góc nhìn xuống (Top-down 3/4) - Elevation 35
    ("B2B_01_Top_FrontRight", (  45.0,  35.0)),
    ("B2B_02_Top_FrontLeft",  ( -45.0,  35.0)),
    ("B2B_03_Top_BackLeft",   (-135.0,  35.0)),
    ("B2B_04_Top_BackRight",  ( 135.0,  35.0)),
    # 4 Góc nhìn chếch lên (Low-angle 3/4) - Elevation -8
    ("B2B_05_Low_FrontRight", (  45.0, -8.0)),
    ("B2B_06_Low_FrontLeft",  ( -45.0, -8.0)),
    ("B2B_07_Low_BackLeft",   (-135.0, -8.0)),
    ("B2B_08_Low_BackRight",  ( 135.0, -8.0)),
    # 5 Góc Orthographic (Trực giao) - Standard Views
    ("B2B_09_Ortho_Front", (0.0, 0.0)),
    ("B2B_10_Ortho_Back",  (0.0, 0.0)),
    ("B2B_11_Ortho_Left",  (0.0, 0.0)),
    ("B2B_12_Ortho_Right", (0.0, 0.0)),
    ("B2B_13_Ortho_Top",   (0.0, 0.0)),
]
CAMERA_FOCAL_MM = {name: 50.0 for name, _ in CAMERA_DEFS}
CAMERA_ZOOM_OUT = 1.15
CAMERA_SAMPLE_MULTIPLIER = {name: 1.0 for name, _ in CAMERA_DEFS}

_CAMERA_DEF_MAP: Dict[str, Tuple] = dict(CAMERA_DEFS)

@contextmanager
def _preserve_camera():
    """Context manager: khôi phục camera active sau khi xong."""
    active = None
    try:
        cam = lux.getActiveCamera()
        active = cam.getName() if cam else None
    except Exception:
        pass
    try:
        yield
    finally:
        if active:
            lux_safe("setCamera", active)

def setup_camera() -> None:
    """Setup cameras — KeyShot 2025.1 API safe."""
    log("CAM", "Setup Camera System v3.2 (KS2025.1 safe)…")

    existing = set()
    try:
        for cam in lux.getCameras():
            try:
                existing.add(cam.getName())
            except Exception:
                pass
    except Exception:
        pass

    (cx, cy, cz), max_dim, _ = get_scene_bounds()

    for name, _ in CAMERA_DEFS:
        if name in existing:
            log("INFO", f"Camera Guard (skip): {name}")
            continue
        try:
            lux_safe("newCamera", name)
            lux_safe("setCamera",  name)

            if "Ortho" in name:
                if   "Front" in name: view_id = getattr(lux, "VIEW_FRONT", 1)
                elif "Back"  in name: view_id = getattr(lux, "VIEW_BACK",  2)
                elif "Left"  in name: view_id = getattr(lux, "VIEW_LEFT",  3)
                elif "Right" in name: view_id = getattr(lux, "VIEW_RIGHT", 4)
                elif "Top"   in name: view_id = getattr(lux, "VIEW_TOP",   5)
                else:                 view_id = getattr(lux, "VIEW_FRONT", 1)

                lux_safe("setStandardView", view_id)

                # [FIX-8] dùng lux_safe thay vì bare call để tránh crash
                lux_safe("setCameraOrthographic")

                auto_dist = lux_safe("getCameraDistance")
                if auto_dist:
                    lux_safe("setCameraDistance", auto_dist * CAMERA_ZOOM_OUT)
                log("CAM", f"  Ortho Setup {name}")
            else:
                lux_safe("setStandardView", getattr(lux, "VIEW_ISOMETRIC", 6))

                auto_dist = lux_safe("getCameraDistance")
                if not auto_dist or auto_dist <= 0:
                    auto_dist = max_dim * 1.5
                final_dist = auto_dist * CAMERA_ZOOM_OUT

                azimuth, elevation = _CAMERA_DEF_MAP.get(name, (45.0, 35.0))

                try:
                    lux.setSphericalCamera(azimuth, elevation, 0.0)
                    lux.setCameraDistance(final_dist)
                    log("CAM", f"  Spherical {name}: Az={azimuth}, El={elevation}, Dist={final_dist:.1f}")
                except Exception as e:
                    log("WARN", f"Spherical Camera Fallback failed: {e}")

                lux_safe("setCameraFocalLength", CAMERA_FOCAL_MM.get(name, 50.0))

            lux_safe("saveCamera", name)
            log("CAM", f"  Created: {name}")
        except Exception as e:
            log("WARN", f"Camera {name}: {e}")

    lux_safe("setCamera", "B2B_01_Top_FrontRight")
    log("CAM", "Camera System READY")

# ==============================================================================
# ▶ ENVIRONMENT & LIGHTING
# [OPT-J] Flag tránh gọi lại setup_environment() nhiều lần không cần thiết
# ==============================================================================
_ENV_SETUP_DONE = False   # [OPT-J]

_ENV_PRIORITY = [
    "GSGProStudiosMetalVol2",
    "GSGPROSTUDIOSMETAL001",
    "ModernIndustrial",
    "3 Point Medium",
    "3 Point Light",
    "Grey Studio Grey Floor",
    "Startup Balanced",
    "Studio Backdrop",
]

def _find_best_env() -> Any:
    try:
        envs = list(lux.getLibraryEnvironments() or [])
        for kw in _ENV_PRIORITY:
            kw_l = kw.lower()
            for e in envs:
                if kw_l in str(e).lower():
                    return e
        return envs[0] if envs else None
    except Exception:
        return None

def setup_environment(active_camera: str = "B2B_01_Top_FrontRight", force: bool = False) -> None:
    """Auto-setup môi trường công nghiệp: HDRI + Lighting Preset chuẩn B2B.
    [OPT-J] Chỉ thực thi lần đầu; dùng force=True để override.
    """
    global _ENV_SETUP_DONE
    if _ENV_SETUP_DONE and not force:
        return
    log("LIGHT", f"Setup Lighting [{active_camera}]…")

    env = _find_best_env()
    if env is not None:
        try:
            lux.setActiveEnvironment(env)
            log("LIGHT", f"  HDRI: {str(env).split('/')[-1]}")

            _, max_dim, _ = get_scene_bounds()
            try:
                active_env = lux.getActiveEnvironment()
                if active_env:
                    cam_az = _CAMERA_DEF_MAP.get(active_camera, (45.0, 35.0))[0]
                    hdri_rotation = (cam_az + 135.0) % 360.0
                    active_env.setRotation(hdri_rotation)
                    brightness = 1.0 if max_dim > 1.0 else 0.9
                    active_env.setBrightness(brightness)
                    log("LIGHT", f"  [Adaptive Optics] B={brightness}, Rot={hdri_rotation:.1f}°, max_dim={max_dim:.1f}")

                    try:
                        active_env.setBackgroundColor([1.0, 1.0, 1.0])
                        active_env.setGroundShadows(True)
                        active_env.setOcclusionGroundShadows(True)
                        active_env.setGroundReflections(True)
                        log("LIGHT", "  [Studio] White BG (1.0) + Shadows + Reflections ON")
                    except Exception as e:
                        log("WARN", f"  Studio Config Fail: {e}")
            except Exception as e:
                log("WARN", f"  Env Optics Sync Fail: {e}")

        except Exception as e:
            log("WARN", f"  setActiveEnvironment: {e}")
    else:
        log("WARN", "  Không tìm được HDRI Library")

    try:
        presets = lux.getLightingPresets()
        studio_preset = next(
            (p for p in presets if any(k in str(p).lower() for k in ["product", "studio", "3 point"])),
            presets[0] if presets else None
        )
        if studio_preset:
            lux.setLightingPreset(studio_preset)
            log("LIGHT", f"  Lighting Preset: {studio_preset}")
    except Exception as e:
        log("WARN", f"setLightingPreset: {e}")

    _ENV_SETUP_DONE = True
    log("LIGHT", "Lighting READY")

# ==============================================================================
# ▶ MATERIAL LIBRARY
# ==============================================================================

_LIBRARY_SEARCH_MAP: Dict[str, List[str]] = {
    "Solid Glass":              ["Glass (Solid) White", "Glass (Solid) Grey", "Glass Basic White"],
    "Brushed Stainless Steel":  ["Stainless Steel Brushed Medium", "Stainless Steel Brushed Heavy", "Steel Brushed"],
    "Polished Stainless Steel": ["Stainless Steel Polished", "Steel Polished"],
    "Cast Iron":                ["Iron Rough", "Iron Brushed", "Steel Rough"],
    "Brass":                    ["Brass Polished", "Brass Brushed"],
    "Plastic Fitting Dark Gray": ["Paint Matte Grey", "Hard Textured Plastic Grey", "Plastic Black"],
    "Plastic Rough Light Gray":  ["Hard Rough Plastic Grey", "Hard Shiny Plastic Grey"],
    "Plastic Pipe Light Gray":   ["Hard Shiny Plastic Grey", "Hard Rough Plastic Grey"],
    "Plastic Rough White":      ["Hard Rough Plastic White", "Hard Shiny Plastic White", "Hard Rough Plastic Grey"],
    "Plastic Textured":         ["Hard Textured Plastic Grey", "Mold-Tech MT-14218"],
    "Paint Matte":              ["Paint Matte Grey", "Matte Grey"],
    "Rubber Hard Black":        ["Rubber", "Tire"],
    "Felt":                     ["Cloth Weave Black 1mm", "Nylon Weave Black 3mm"],
    "Plastic Fine Grain":       ["Mold-Tech MT-11020 Spray Dot", "Hard Textured Plastic Grey"],
    "Fiber":                    ["Nylon Weave Black 3mm", "Carbon Fiber Rough 5mm"],
    "Filter Cartridge White":   ["Cloth Weave White 1mm", "Plastic Stereolithography Rough 3mm", "Hard Rough Plastic White"],
    "Plastic Blue":             ["Hard Shiny Plastic Blue", "Paint Gloss Blue"],
    "Solid Glass Blue":         ["Clear Shiny Plastic Blue", "Glass Heavy Frost Bright Blue"],
    "Plastic Red":              ["Hard Shiny Plastic Red", "Paint Gloss Red"],
    "Solid Glass Red":          ["Clear Shiny Plastic Red", "Glass Heavy Frost Bright Red"],
    "Plastic Black":            ["Hard Rough Plastic Black", "Matte Black"],
    "Plastic Beige":            ["Hard Shiny Plastic White", "Hard Textured Plastic White", "Paint Matte White"],
    "Plastic Orange":           ["Paint Gloss Orange", "Hard Shiny Plastic Orange"],
    "Plastic Yellow":           ["Paint Gloss Yellow", "Hard Shiny Plastic Yellow"],
    "Plastic Green":            ["Paint Gloss Green", "Hard Shiny Plastic Green"],
    "Plastic Purple":           ["Paint Gloss Purple", "Hard Shiny Plastic Purple"],
    "Metal Blue":               ["Anodized Aluminum Brushed Blue", "Paint Metallic Blue"],
    "Metal Red":                ["Anodized Aluminum Brushed Red", "Paint Metallic Red"],
    "Metal Orange":             ["Anodized Aluminum Brushed Orange", "Paint Metallic Orange peel Orange"],
    "Metal Yellow":             ["Anodized Aluminum Brushed Yellow", "Paint Metallic Yellow"],
    "Metal Green":              ["Paint Metallic Lime Green", "Paint Metallic Green"],
    "Metal Purple":             ["Anodized Aluminum Brushed Purple", "Paint Metallic Purple"],
    "Metal Black":              ["Anodized Aluminum Brushed Black", "Paint Metallic Black"],
    "Metal White":              ["Paint Metallic White", "Automotive White"],
}

_SHADER_MAP: Dict[str, Any] = {
    "Solid Glass":              getattr(lux, "SHADER_TYPE_GLASS_SOLID",  None),
    "Brushed Stainless Steel":  getattr(lux, "SHADER_TYPE_BRUSHED",      None),
    "Polished Stainless Steel": getattr(lux, "SHADER_TYPE_BRUSHED",      None),
    "Cast Iron":                getattr(lux, "SHADER_TYPE_METAL",        None),
    "Brass":                    getattr(lux, "SHADER_TYPE_METAL",        None),
    "Plastic Fitting Dark Gray": getattr(lux, "SHADER_TYPE_PLASTIC",      None),
    "Plastic Rough Light Gray": getattr(lux, "SHADER_TYPE_PLASTIC",      None),
    "Plastic Rough White":      getattr(lux, "SHADER_TYPE_PLASTIC",      None),
    "Plastic Textured":         getattr(lux, "SHADER_TYPE_PLASTIC",      None),
    "Paint Matte":              getattr(lux, "SHADER_TYPE_PAINT",        None),
    "Rubber Hard Black":        getattr(lux, "SHADER_TYPE_PLASTIC",      None),
    "Felt":                     getattr(lux, "SHADER_TYPE_TRANSLUCENT",  None),
    "Plastic Fine Grain":       getattr(lux, "SHADER_TYPE_PLASTIC",      None),
    "Fiber":                    getattr(lux, "SHADER_TYPE_PLASTIC",      None),
    "Plastic Blue":             getattr(lux, "SHADER_TYPE_PLASTIC",      None),
    "Plastic Red":              getattr(lux, "SHADER_TYPE_PLASTIC",      None),
    "Solid Glass Red":          getattr(lux, "SHADER_TYPE_GLASS_SOLID",  None),
    "Plastic Black":            getattr(lux, "SHADER_TYPE_PLASTIC",      None),
    "Plastic Beige":            getattr(lux, "SHADER_TYPE_PLASTIC",      None),
    "Plastic Orange":           getattr(lux, "SHADER_TYPE_PAINT",        None),
    "Plastic Yellow":           getattr(lux, "SHADER_TYPE_PAINT",        None),
    "Plastic Green":            getattr(lux, "SHADER_TYPE_PAINT",        None),
    "Plastic Purple":           getattr(lux, "SHADER_TYPE_PAINT",        None),
    "Metal Blue":               getattr(lux, "SHADER_TYPE_METAL",        None),
    "Metal Red":                getattr(lux, "SHADER_TYPE_METAL",        None),
    "Metal Orange":             getattr(lux, "SHADER_TYPE_METAL",        None),
    "Metal Yellow":             getattr(lux, "SHADER_TYPE_METAL",        None),
    "Metal Green":              getattr(lux, "SHADER_TYPE_METAL",        None),
    "Metal Purple":             getattr(lux, "SHADER_TYPE_METAL",        None),
    "Metal Black":              getattr(lux, "SHADER_TYPE_METAL",        None),
    "Metal White":              getattr(lux, "SHADER_TYPE_METAL",        None),
}
_SHADER_FALLBACK = getattr(lux, "SHADER_TYPE_PLASTIC", None)

_LIB_MATERIALS_CACHE: Optional[List] = None

def _get_lib_materials() -> List:
    global _LIB_MATERIALS_CACHE
    if _LIB_MATERIALS_CACHE is None:
        try:
            _LIB_MATERIALS_CACHE = list(lux.getLibraryMaterials()) or []
            log("MAT", f"  Library: {len(_LIB_MATERIALS_CACHE)} materials available")
            log("MAT", f"  Sample: {[str(m) for m in _LIB_MATERIALS_CACHE[:3]]}")
        except Exception as e:
            log("WARN", f"getLibraryMaterials: {e}")
            _LIB_MATERIALS_CACHE = []
    return _LIB_MATERIALS_CACHE

def _find_library_material(mat_type: str) -> Any:
    keywords = _LIBRARY_SEARCH_MAP.get(mat_type, [mat_type])
    lib_mats = _get_lib_materials()
    if not lib_mats:
        return None
    for kw in keywords:
        kw_l = kw.lower()
        for m in lib_mats:
            try:
                if kw_l in str(m).lower():
                    return m
            except Exception:
                continue
    return None

def _apply_lib_mat(node: Any, lib_mat: Any) -> bool:
    """Áp dụng library material chuẩn cho KeyShot 2025.1"""
    mat_name = str(lib_mat)

    node_id = None
    if   hasattr(node, "getID"): node_id = node.getID()
    elif hasattr(node, "id"):    node_id = node.id
    elif hasattr(node, "ID"):    node_id = node.ID
    else:                        node_id = node

    try:
        lux.applyMaterialMapping({node_id: mat_name})
        log("MAT", f"  ✅ Applied: {mat_name}")
        return True
    except Exception as e:
        log("MAT", f"  ❌ applyMaterialMapping fail: {e}")
        return False

# [FIX-1] Thêm tham số node vào signature — loại bỏ NameError node_name
def _apply_material_profile(node: Any, profile: Dict) -> None:
    mat_type = profile.get("type")
    if not mat_type:
        return

    # Ưu tiên 1: Library material
    lib_mat = _find_library_material(mat_type)
    if lib_mat is not None:
        if _apply_lib_mat(node, lib_mat):
            return

    # Ưu tiên 2: createSceneMaterial fallback
    try:
        shader = _SHADER_MAP.get(mat_type) or _SHADER_FALLBACK
        if shader:
            mat = lux.createSceneMaterial(shader)
            if mat is not None:
                # Lấy tên node an toàn để gọi setObjectMaterial
                node_name = node.getName() if hasattr(node, "getName") else str(node)
                lux.setObjectMaterial(node_name, mat)
    except Exception as e:
        log("WARN", f"_apply_material_profile({mat_type}): {e}")

def _guess_profile_from_inventor_material(node_name: str, mat_name: str) -> Optional[str]:
    """Phân tích TÊN VẬT LIỆU (Tính chất vật lý) và MÀU SẮC từ Inventor."""
    node_name = (node_name or "").lower().strip()
    mat_name  = (mat_name  or "").lower().strip()

    # Loại bỏ prefix tên node khỏi mat_name (Inventor export quirk)
    if node_name and mat_name.startswith(node_name):
        mat_name = mat_name[len(node_name):].strip()
    elif node_name and node_name in mat_name:
        mat_name = mat_name.replace(node_name, "").strip()

    # PiPipe — ống uPVC (xám nhạt)
    if node_name.startswith("pipipe") or "pipe" in node_name:
        return "Plastic Pipe Light Gray"

    # Fittings & phụ kiện nhựa uPVC
    _FITTING_KEYWORDS = (
        "co 90", "co 45", "co 60", "co 30", "co goc",
        "elbow", "bend",
        "te giam", "te thang", "te bằng", "te bang",
        "tegiam", "tee", " te ",
        "rac co", "racco",
        "union", "khop noi",
        "noi thang", "noithang", "coupling", "sleeve",
        "noi giam", "reducer straight", "bushing",
        "giam ", "reducer", "reduction",
        "mat bich", "matbich", "flange", "stub flange",
        "loi ", " loi", "socket", "hub",
        "ren ngoai", "renngoai", "male thread", "mnpt",
        "ren trong", "rentrong", "female thread", "fnpt",
        "nap bit", "napbit", "end cap", "cap end", "plug",
        "chu thap", "chuthap", "cross fitting",
        "noi ong", "pipe connector", "nipple",
        "adapter", "adaptor",
        "van nhua", "plastic valve", "ball valve",
        "filter", "housing", "lo loc", "vo loc",
        "cum loc", "cum may", "cum bom",
        "manifold",
    )
    if any(kw in node_name for kw in _FITTING_KEYWORDS):
        return "Plastic Fitting Dark Gray"

    # Frame (Inox bóng)
    if node_name.startswith("frame"):
        return "Polished Stainless Steel"

    # Inox từ tên node
    if "inox" in node_name or "stainless" in node_name:
        return "Brushed Stainless Steel"

    # Fasteners
    _FASTENER_KEYWORDS = ("bolt", "nut", "tacke", "washer", "screw",
                          "iso 8676", "iso 4762", "iso 4161", "iso 7092",
                          "iso 4019", "iso 8673", "din ", "gb/t ")
    if any(kw in node_name for kw in _FASTENER_KEYWORDS):
        return "Brushed Stainless Steel"

    # Parse RGB color từ mat_name (KeyShot có thể truncate)
    r = g = b = -1
    has_color = False

    # [FIX-7] Không extrapolate b=g — chỉ dùng dữ liệu thực tế có
    match_3 = re.search(r'color:(\d+):(\d+):(\d+)', mat_name)
    match_2 = re.search(r'color:(\d+):(\d+):?$', mat_name)
    match_1 = re.search(r'color:(\d+)$', mat_name)

    if match_3:
        r, g, b = int(match_3.group(1)), int(match_3.group(2)), int(match_3.group(3))
        has_color = True
    elif match_2:
        # Chỉ có 2 channels — không đoán b, dùng fallback xám
        r = int(match_2.group(1))
        g = int(match_2.group(2))
        b = -1          # unknown — không extrapolate
        has_color = True
    elif match_1:
        r = int(match_1.group(1))
        g = b = -1      # unknown
        has_color = True

    # Text color keywords (English/CAD only)
    text_color = None
    if   "blue"   in mat_name: text_color = "Blue"
    elif "red"    in mat_name: text_color = "Red"
    elif "yellow" in mat_name: text_color = "Yellow"
    elif "green"  in mat_name: text_color = "Green"
    elif "purple" in mat_name: text_color = "Purple"
    elif "orange" in mat_name: text_color = "Orange"
    elif "black"  in mat_name: text_color = "Black"
    elif "white"  in mat_name: text_color = "White"
    elif "grey" in mat_name or "gray" in mat_name: text_color = "Grey"

    def _get_color_variant(base_type: str) -> Optional[str]:
        if text_color:
            if text_color == "White" and base_type == "Plastic":
                if any(k in mat_name for k in ("loi", "cartridge", "nylon", "cloth")):
                    return "Filter Cartridge White"
                return "Plastic Rough White"
            if text_color == "Grey"  and base_type == "Plastic": return "Plastic Rough Light Gray"
            if text_color == "Black" and base_type == "Plastic": return "Plastic Black"
            if text_color == "Black" and base_type == "Rubber":  return "Rubber Hard Black"
            if base_type == "Glass":
                if text_color in ("Blue", "Red"): return f"Solid Glass {text_color}"
                return "Solid Glass"
            return f"{base_type} {text_color}"

        if not has_color:
            return None

        # Chỉ classify khi đủ 3 channels
        if b < 0:
            # Không đủ thông tin màu — fallback về xám
            return f"{base_type} Rough Light Gray" if base_type == "Plastic" else None

        if r < 100 and g < 100 and b < 100:
            return f"{base_type} Black" if base_type != "Glass" else "Solid Glass"
        if r > 150 and g > 150 and b < 100: return f"{base_type} Yellow" if base_type != "Glass" else "Solid Glass"
        if r > 150 and 70 < g < 150 and b < 80: return f"{base_type} Orange" if base_type != "Glass" else "Solid Glass Red"
        if r > 150 and g < 80 and b < 80:   return "Solid Glass Red" if base_type == "Glass" else f"{base_type} Red"
        if g > 120 and r < 100 and b < 100: return f"{base_type} Green" if base_type != "Glass" else "Solid Glass"
        if r > 120 and b > 120 and g < 80:  return f"{base_type} Purple" if base_type != "Glass" else "Solid Glass"
        if b > 150 and r < 150: return "Solid Glass Blue" if base_type == "Glass" else f"{base_type} Blue"
        if r > 200 and g > 200 and b > 200:
            if base_type == "Plastic":
                if any(k in mat_name for k in ("loi", "cartridge", "nylon", "cloth")):
                    return "Filter Cartridge White"
                return "Plastic Rough White"
            if base_type == "Metal": return "Metal White"
            return "Solid Glass"
        if r > 200 and g > 150 and b < 180: return "Plastic Beige"
        if 100 <= r <= 200 and abs(r-g) < 20 and abs(g-b) < 20:
            return "Cast Iron" if base_type == "Metal" else "Plastic Rough Light Gray"
        return None

    # 1. Cao su / Rubber
    if any(k in mat_name for k in ("rubber", "epdm", "viton", "silicone")):
        return "Rubber Hard Black"

    # 2. Kim loại
    is_metal = False
    if any(k in mat_name for k in ("stainless", "inox", "sus304", "sus")):
        return "Brushed Stainless Steel"
    if any(k in mat_name for k in ("brass", "copper", "bronze", "thau")):
        return "Brass"
    if any(k in mat_name for k in ("steel", "iron", "cast", "metal", "thep",
                                    "gang", "nhom", "aluminum")):
        is_metal = True
    if is_metal:
        color_mat = _get_color_variant("Metal")
        return color_mat if color_mat else "Cast Iron"

    # 3. Kính / Trong suốt
    if any(k in mat_name for k in ("glass", "clear", "acrylic", "polycarbonate", "mica")):
        color_mat = _get_color_variant("Glass")
        if color_mat: return color_mat
        if "blue" in mat_name: return "Solid Glass Blue"
        if "red"  in mat_name: return "Solid Glass Red"
        return "Solid Glass"

    # 4. Nhựa công nghiệp
    if any(k in mat_name for k in ("pvc", "hdpe", "plastic", "nylon", "pp",
                                    "nhua", "upvc", "frp")):
        color_mat = _get_color_variant("Plastic")
        return color_mat if color_mat else "Plastic Rough Light Gray"

    # 5. Fallback text color
    if text_color:
        if text_color == "Black":
            if any(k in mat_name for k in ("rubber", "seal", "o-ring", "gasket")):
                return "Rubber Hard Black"
            return "Plastic Black"
        if text_color == "White":
            if any(k in mat_name for k in ("loi", "cartridge", "nylon", "cloth")):
                return "Filter Cartridge White"
            return "Plastic Rough White"
        if text_color == "Grey": return "Plastic Rough Light Gray"
        return f"Plastic {text_color}"

    # 6. Fallback RGB (chỉ khi đủ 3 channels)
    if has_color and b >= 0:
        if r < 100 and g < 100 and b < 100:
            return "Rubber Hard Black" if any(k in mat_name for k in ("rubber", "seal", "o-ring", "gasket")) else "Plastic Black"
        if r > 150 and g > 150 and b < 100: return "Plastic Yellow"
        if r > 150 and 70 < g < 150 and b < 80: return "Plastic Orange"
        if r > 150 and g < 80 and b < 80: return "Plastic Red"
        if g > 120 and r < 100 and b < 100: return "Plastic Green"
        if r > 120 and b > 120 and g < 80: return "Plastic Purple"
        if b > 150 and r < 150: return "Plastic Blue"
        if r > 200 and g > 200 and b > 200:
            return "Filter Cartridge White" if any(k in mat_name for k in ("loi", "cartridge", "nylon", "cloth")) else "Plastic Rough White"
        if r > 200 and g > 150 and b < 180: return "Plastic Beige"
        if 100 <= r <= 200 and abs(r-g) < 20 and abs(g-b) < 20: return "Plastic Rough Light Gray"
        if r > 200 and g > 180 and b < 100: return "Brass"

    return None

def apply_materials() -> None:
    log("MAT", "Apply Industrial Materials v3.3…")

    lib_mats = _get_lib_materials()
    lib_name_cache: Dict[str, Any] = {}

    def _resolve_lib(profile_type: str) -> Any:
        if profile_type not in lib_name_cache:
            lib_name_cache[profile_type] = _find_library_material(profile_type)
        return lib_name_cache[profile_type]

    # PASS 1: Pure Python — xây batch {node_id → mat_name}
    batch: Dict[Any, str] = {}
    node_map: Dict[Any, Any] = {}   # node_id → node object (dùng cho per-node fallback)
    assigned = fallback = skipped = reassigned = 0

    for node in _collect_scene_nodes():
        try:
            # Chỉ áp cho leaf nodes (geometry), không ghi đè group
            children = node.getChildren() if hasattr(node, "getChildren") else []
            if children and len(children) > 0:
                continue

            node_name = node.getName().lower()
            if "__lock" in node_name:
                skipped += 1
                continue

            node_id = None
            if   hasattr(node, "getID"): node_id = node.getID()
            elif hasattr(node, "id"):    node_id = node.id
            elif hasattr(node, "ID"):    node_id = node.ID
            else:                        node_id = node
            if node_id is None:
                continue

            mat_name = ""
            try:
                mat_obj = node.getMaterial()
                mat_name = (mat_obj.getName() if hasattr(mat_obj, "getName") else str(mat_obj)).lower()
            except Exception:
                pass
            mat_clean = re.sub(r'\s*#\d*\s*$', '', mat_name).strip()

            profile_type = _guess_profile_from_inventor_material(node_name, mat_name)
            if not profile_type:
                fallback += 1
                continue

            target_name = ""
            
            # ĐIỀU HƯỚNG LIBRARY THEO PHÂN LOẠI
            if profile_type == "Plastic Pipe Light Gray":
                # Ống -> luôn dùng cấu hình Ống
                lib_mat = _resolve_lib("Plastic Pipe Light Gray")
            elif profile_type in ("Plastic Rough Light Gray", "Plastic Fitting Dark Gray"):
                # Gom chung toàn bộ Phụ Kiện và Nhựa xám mặc định -> Xám Đậm
                lib_mat = _resolve_lib("Plastic Fitting Dark Gray")
            else:
                # Dùng thư viện cho các vật liệu còn lại (Inox, Kính, Tank Xanh...)
                lib_mat = _resolve_lib(profile_type)

            if lib_mat is None:
                fallback += 1
                continue
                
            target_name = str(lib_mat)

            if mat_clean == target_name.lower():
                assigned += 1
                continue

            batch[node_id]   = target_name
            node_map[node_id] = node
            reassigned += 1

        except Exception as e:
            log("WARN", f"Node scan fail: {e}")

    # PASS 2: Batch apply — [FIX-6] per-node fallback nếu batch fail
    if batch:
        try:
            lux.applyMaterialMapping(batch)
            log("MAT", f"  Batch applied: {len(batch)} nodes")
        except Exception as e:
            log("WARN", f"Batch applyMaterialMapping fail ({e}) — switching to per-node fallback")
            per_ok = per_fail = 0
            for nid, mat_name in batch.items():
                try:
                    lux.applyMaterialMapping({nid: mat_name})
                    per_ok += 1
                except Exception as e2:
                    log("WARN", f"  Per-node fail [{nid}]: {e2}")
                    per_fail += 1
            log("MAT", f"  Per-node fallback: ok={per_ok}, fail={per_fail}")

    assigned += reassigned
    log("MAT", f"Materials READY — assigned={assigned}, reassigned={reassigned}, fallback={fallback}, skipped={skipped}")

# ==============================================================================
# ▶ RENDER ENGINE
# ==============================================================================
def setup_render_engine(ctx: RenderContext) -> None:
    preset = ctx.preset()
    log("REND", f"Quality: {ctx.quality} (samples={preset['samples']}, bounces={preset['bounces']})")

    # GPU priority — chống overheat CPU
    gpu_engine = (
        getattr(lux, "RENDER_ENGINE_PRODUCT_GPU",  None) or
        getattr(lux, "RENDER_ENGINE_INTERIOR_GPU", None) or
        getattr(lux, "RENDER_ENGINE_GPU",          None)
    )
    if gpu_engine is not None:
        lux.setRenderEngine(gpu_engine)
        log("REND", f"GPU Engine LOCKED ({gpu_engine})")
    else:
        log("WARN", "CRITICAL: Không tìm được GPU engine, có thể chạy CPU!")

    for func in ("setGPURender", "setUseGPU", "enableGPU"):
        try: getattr(lux, func)(True)
        except Exception: pass

def _make_render_opts(ctx: RenderContext, cam_name: str, mode_passes: Optional[List[str]] = None) -> Any:
    """[FIX-3] passes lấy từ mode_cfg, không hardcode toàn bộ."""
    preset   = ctx.preset()
    adjusted = int(preset["samples"] * CAMERA_SAMPLE_MULTIPLIER.get(cam_name, 1.0))

    opts = lux.getRenderOptions()
    opts.setMaxSamples(adjusted)
    opts.setRayBounces(preset["bounces"])
    opts.setGlobalIllumination(True)
    opts.setIncludeAlpha(True)

    if ctx.quality in ("FINAL", "ULTRA") and hasattr(opts, "setClampSamples"):
        safe(opts.setClampSamples, 150)

    if mode_passes:
        try:
            opts.setOutputPasses(mode_passes)
        except Exception:
            pass  # API không hỗ trợ thì bỏ qua

    if preset["denoise"]:
        if hasattr(opts, "setDenoise"):      safe(opts.setDenoise,      True)
        if hasattr(opts, "setDenoiseBlend"): safe(opts.setDenoiseBlend, preset["denoise_blend"])

    log("REND", f"  Opts: {adjusted} spp × bounce={preset['bounces']}, passes={mode_passes}")
    return opts

# ==============================================================================
# ▶ SMART RENDER
# ==============================================================================
def smart_render(cam_name: str, out_path: str, ctx: RenderContext,
                 mode_passes: Optional[List[str]] = None) -> bool:
    if RESUME_RENDER and os.path.exists(out_path):
        log("INFO", f"SKIP (đã có): {os.path.basename(out_path)}")
        return False

    w, h = ctx.width, ctx.height
    draft_path = None

    lux_safe("setCamera", cam_name)

    if DRAFT_PRECHECK and ctx.quality in ("FINAL", "ULTRA"):
        draft_path = out_path.replace(".png", "_precheck.png")
        draft_ctx  = RenderContext(quality="DRAFT", width=w // 4, height=h // 4)
        lux.renderImage(draft_path, w // 4, h // 4,
                        _make_render_opts(draft_ctx, cam_name, ["Beauty"]))
        log("REND", f"  Draft → {os.path.basename(draft_path)}")

    lux.renderImage(out_path, w, h, _make_render_opts(ctx, cam_name, mode_passes))

    log("OK", f"Saved: {os.path.basename(out_path)}")
    MetadataScrubber.scrub(out_path)

    if draft_path and os.path.exists(draft_path):
        try:
            os.remove(draft_path)
        except Exception:
            pass

    return True

# ==============================================================================
# ▶ METADATA SCRUBBER
# ==============================================================================
class MetadataScrubber:
    @staticmethod
    def scrub_png(filepath: str) -> None:
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
            if not data.startswith(b'\x89PNG\r\n\x1a\n'):
                return
            signature   = b'\x89PNG\r\n\x1a\n'
            out_data    = bytearray(signature)
            idx         = 8
            unsafe_chunks = {b'tEXt', b'iTXt', b'zTXt', b'eXIf'}
            scrubbed    = 0
            while idx < len(data):
                if idx + 8 > len(data): break
                length     = int.from_bytes(data[idx:idx+4], 'big')
                chunk_type = data[idx+4:idx+8]
                if chunk_type not in unsafe_chunks:
                    out_data.extend(data[idx:idx+12+length])
                else:
                    scrubbed += 1
                idx += 12 + length
            if scrubbed:
                with open(filepath, 'wb') as f:
                    f.write(out_data)
                log("INFO", f"  Scrubbed {scrubbed} metadata chunks (PNG)")
        except Exception as e:
            log("WARN", f"Scrub PNG failed: {e}")

    @staticmethod
    def scrub_glb(filepath: str) -> None:
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
            if not data.startswith(b'glTF'):
                return
            version         = int.from_bytes(data[4:8], 'little')
            json_chunk_len  = int.from_bytes(data[12:16], 'little')
            if data[16:20] != b'JSON':
                return
            json_data = data[20:20+json_chunk_len]
            bin_start = 20 + json_chunk_len
            js = json.loads(json_data.decode('utf-8'))
            modified = False
            if "asset" in js:
                if "generator" in js["asset"]:
                    js["asset"]["generator"] = "Tanphan OS v3.2"
                    modified = True
                for k in ("copyright", "extras"):
                    if k in js["asset"]:
                        del js["asset"][k]
                        modified = True
            if not modified:
                return
            new_json = json.dumps(js, separators=(',', ':'))
            padding  = (4 - (len(new_json) % 4)) % 4
            new_json += " " * padding
            new_bytes = new_json.encode('utf-8')
            new_total = 12 + 8 + len(new_bytes) + (len(data) - bin_start)
            out_data  = bytearray()
            out_data.extend(b'glTF')
            out_data.extend(version.to_bytes(4, 'little'))
            out_data.extend(new_total.to_bytes(4, 'little'))
            out_data.extend(len(new_bytes).to_bytes(4, 'little'))
            out_data.extend(b'JSON')
            out_data.extend(new_bytes)
            out_data.extend(data[bin_start:])
            with open(filepath, 'wb') as f:
                f.write(out_data)
            log("INFO", "  Scrubbed GLB metadata (Generator: Tanphan OS)")
        except Exception as e:
            log("WARN", f"Scrub GLB failed: {e}")

    @classmethod
    def scrub(cls, filepath: str) -> None:
        if not os.path.exists(filepath):
            return
        ext = filepath.lower().rsplit('.', 1)[-1]
        if   ext == 'png': cls.scrub_png(filepath)
        elif ext == 'glb': cls.scrub_glb(filepath)

# ==============================================================================
# ▶ SNAPSHOT MANAGER
# ==============================================================================
class SnapshotManager:
    VERSION = "3.2"

    def __init__(self, path: str):
        self.path = path

    def save(self) -> None:
        log("SNAP", f"SAVE → {self.path}")
        snap = {
            "version":     self.VERSION,
            "saved_at":    datetime.datetime.now().isoformat(),
            "environment": self._read_environment(),
            "cameras":     self._read_cameras(),
            "materials":   self._read_materials(),
        }
        try:
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(snap, f, ensure_ascii=False, indent=2)
            log("OK", f"Snapshot saved — {len(snap['cameras'])} cams, {len(snap['materials'])} mats")
        except Exception as e:
            log("ERR", f"Không ghi được snapshot: {e}")

    def load(self) -> bool:
        """Trả về True nếu load thành công."""
        if not os.path.exists(self.path):
            log("WARN", f"Snapshot không tồn tại: {self.path}")
            return False
        log("SNAP", f"LOAD ← {self.path}")
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                snap = json.load(f)
        except Exception as e:
            log("ERR", f"Không đọc được snapshot: {e}")
            return False
        log("INFO", f"  v{snap.get('version','?')} from: {snap.get('saved_at','?')}")
        self._apply_environment(snap.get("environment", {}))
        self._apply_materials(snap.get("materials", {}))
        return True

    def _read_environment(self) -> Dict:
        env_obj = lux_safe("getActiveEnvironment")
        if not env_obj:
            return {}
        bg = env_obj.getBackgroundColor() if hasattr(env_obj, 'getBackgroundColor') else None
        bg_list = None
        if bg is not None:
            try: bg_list = [bg[0], bg[1], bg[2]]
            except Exception: pass
        return {
            "name":                   env_obj.getName()                  if hasattr(env_obj, 'getName')                  else "",
            "brightness":             env_obj.getBrightness()            if hasattr(env_obj, 'getBrightness')            else None,
            "rotation":               env_obj.getRotation()              if hasattr(env_obj, 'getRotation')              else None,
            "backgroundColor":        bg_list,
            "groundShadows":          env_obj.getGroundShadows()         if hasattr(env_obj, 'getGroundShadows')         else None,
            "occlusionGroundShadows": env_obj.getOcclusionGroundShadows() if hasattr(env_obj, 'getOcclusionGroundShadows') else None,
            "groundReflections":      env_obj.getGroundReflections()     if hasattr(env_obj, 'getGroundReflections')     else None,
        }

    def _read_cameras(self) -> Dict:
        result: Dict = {}
        try:
            with _preserve_camera():
                for cam in lux.getCameras():
                    try:
                        name = cam.getName()
                        lux_safe("setCamera", name)
                        result[name] = {
                            "focal_length": lux_safe("getCameraFocalLength"),
                            "fstop":        lux_safe("getCameraFStop"),
                            "focus_dist":   lux_safe("getCameraFocusDistance"),
                            "dof":          lux_safe("getCameraDof"),
                        }
                    except Exception:
                        pass
        except Exception:
            pass
        return result

    def _read_materials(self) -> Dict:
        result: Dict = {}
        for node in _collect_scene_nodes():
            try:
                mat = node.getMaterial()
                if mat:
                    name = mat.getName() if hasattr(mat, "getName") else str(mat)
                    if name:
                        result[node.getName()] = name
            except Exception:
                pass
        return result

    def _apply_environment(self, env_data: Dict) -> None:
        env_obj = lux_safe("getActiveEnvironment")
        if not env_obj or not env_data:
            return
        if env_data.get("brightness")             is not None and hasattr(env_obj, 'setBrightness'):
            safe(env_obj.setBrightness, env_data["brightness"])
        if env_data.get("rotation")               is not None and hasattr(env_obj, 'setRotation'):
            safe(env_obj.setRotation, env_data["rotation"])
        if env_data.get("backgroundColor")        is not None and hasattr(env_obj, 'setBackgroundColor'):
            safe(env_obj.setBackgroundColor, env_data["backgroundColor"])
        if env_data.get("groundShadows")          is not None and hasattr(env_obj, 'setGroundShadows'):
            safe(env_obj.setGroundShadows, env_data["groundShadows"])
        if env_data.get("occlusionGroundShadows") is not None and hasattr(env_obj, 'setOcclusionGroundShadows'):
            safe(env_obj.setOcclusionGroundShadows, env_data["occlusionGroundShadows"])
        if env_data.get("groundReflections")      is not None and hasattr(env_obj, 'setGroundReflections'):
            safe(env_obj.setGroundReflections, env_data["groundReflections"])
        log("LIGHT", f"Environment restored (from snapshot: {env_data.get('name','')})")

    def _apply_materials(self, mat_map: Dict) -> None:
        restored = sum(
            1 for node in _collect_scene_nodes()
            if node.getName() in mat_map
            and safe(node.setMaterial, mat_map[node.getName()]) is not None
        )
        log("MAT", f"Materials restored: {restored}/{len(mat_map)}")

# ==============================================================================
# ▶ MAIN PIPELINE
# ==============================================================================
_snapshot = SnapshotManager(SNAPSHOT_FILE)

def _run_setup(ctx: RenderContext) -> None:
    """Phase 1: Materials, cameras, render engine."""
    # [FIX-9] Nếu snapshot load fail → vẫn apply_materials() đảm bảo pipeline không bị empty
    if SNAPSHOT_MODE == "LOAD":
        loaded = _snapshot.load()
        if not loaded:
            log("WARN", "Snapshot load fail — chạy apply_materials() thay thế")
            apply_materials()
    else:
        apply_materials()

    setup_camera()
    setup_render_engine(ctx)

    if SNAPSHOT_MODE == "SAVE":
        _snapshot.save()

    log("OK", "SETUP COMPLETE")

def _run_batch(ctx: RenderContext, mode_cfg: Dict) -> None:
    """Phase 2: Batch render — [FIX-4] setup_environment() chỉ 1 lần trước loop."""
    out_dir = get_output_dir()
    cams    = ["B2B_01_Top_FrontRight"] if AUTO_RENDER_MODE == "HERO" else mode_cfg["cameras"]
    passes  = mode_cfg.get("passes", ["Beauty"])
    total   = len(cams)
    done = skipped = 0
    errors: List[Tuple[str, str]] = []

    log("FILM", f"BATCH [{ctx.width}×{ctx.height}] | Mode={OUTPUT_MODE} | {total} cameras → {out_dir}")

    # [FIX-4] Gọi setup_environment() 1 lần duy nhất trước vòng lặp
    setup_environment(active_camera=cams[0])

    frame_times: List[float] = []

    for idx, cam in enumerate(cams, 1):
        # Kiểm tra ngắt khẩn cấp ESC
        if ctypes.windll.user32.GetAsyncKeyState(0x1B) & 0x8000:
            log("WARN", "🚨 ESC detected — hủy BATCH RENDER")
            break

        bar = "█" * idx + "░" * (total - idx)

        # ETA estimate — [OPT-I]
        eta_str = ""
        if frame_times:
            avg = sum(frame_times) / len(frame_times)
            remaining = avg * (total - idx + 1)
            eta_str = f" | ETA ~{int(remaining//60)}m{int(remaining%60)}s"

        log("PROG", f"[{bar}] {idx}/{total} — {cam}{eta_str}")
        t0 = time.time()
        try:
            lux_safe("setCamera", cam)
            out_path = os.path.join(out_dir, f"{cam}_{OUTPUT_MODE}_{ctx.quality}.png")
            rendered = smart_render(cam, out_path, ctx, mode_passes=passes)
            if rendered:
                frame_times.append(time.time() - t0)
            done += rendered
        except Exception as e:
            log("ERR", f"[{cam}] FAILED: {e}")
            errors.append((cam, str(e)))
            skipped += 1

    print("─" * 60)
    log("OK", f"BATCH DONE — rendered={done}, skipped={skipped}, errors={len(errors)}")
    if errors:
        log("WARN", "Cameras có lỗi:")
        for cam, err in errors:
            log("ERR", f"  {cam}: {err}")
    try:
        os.startfile(out_dir)
    except Exception:
        pass

def _run_ar_export(out_dir: str) -> None:
    """Phase 3: AR asset export (GLB + USDZ)."""
    glb_path  = os.path.join(out_dir, "B2B_RO_System_AR.glb")
    usdz_path = os.path.join(out_dir, "B2B_RO_System_AR.usdz")
    lux_safe("exportFile", glb_path)
    lux_safe("exportFile", usdz_path)
    MetadataScrubber.scrub(glb_path)
    MetadataScrubber.scrub(usdz_path)
    log("OK", f"AR assets exported & scrubbed → {out_dir}")

def main() -> None:
    _validate_config()
    log("HEAD", "NIGHT-CRAWLER v3.3 — COMMERCIAL RENDER OS BOOTING")

    mode_cfg = get_mode_config()

    ctx = (
        RenderContext.from_mode(mode_cfg)
        if AUTO_RENDER_MODE != "OFF"
        else RenderContext.from_globals()
    )

    log("INFO", f"{ctx} | AutoMode={AUTO_RENDER_MODE}")
    print("─" * 60)

    _run_setup(ctx)
    print("─" * 60)

    if AUTO_RENDER_MODE != "OFF":
        _run_batch(ctx, mode_cfg)
        if EXPORT_WEB_AR or OUTPUT_MODE in AR_FORCE_MODES:
            _run_ar_export(get_output_dir())
    else:
        setup_environment(active_camera="B2B_01_Top_FrontRight")
        log("INFO", "Interactive mode — đổi AUTO_RENDER_MODE='HERO'/'ALL_CAMERAS' để render")

    print("─" * 60)
    log("HEAD", "NIGHT-CRAWLER v3.3 — SESSION END")

# ==============================================================================
# ▶ ENTRY POINT
# ==============================================================================
if DEBUG_LUX_API:
    attrs     = sorted(dir(lux))
    cam_attrs = [a for a in attrs if "amera" in a or "cam" in a.lower()]
    env_attrs = [a for a in attrs if "nviron" in a or "hdri" in a.lower() or "lighting" in a.lower()]
    mat_attrs = [a for a in attrs if "aterial" in a or "mat" in a.lower()]
    lgt_attrs = [a for a in attrs if "ight" in a.lower() and "lightning" not in a.lower()]
    rnd_attrs = [a for a in attrs if "ender" in a.lower() or "RENDER" in a]
    print("=" * 60)
    print(f"⭐ LUX API DUMP — {len(attrs)} attributes")
    print("=" * 60)
    print(f"\n[📸 CAMERA ({len(cam_attrs)})]:",  ", ".join(cam_attrs))
    print(f"\n[💡 ENV    ({len(env_attrs)})]:",  ", ".join(env_attrs))
    print(f"\n[🎨 MAT    ({len(mat_attrs)})]:",  ", ".join(mat_attrs))
    print(f"\n[💡 LIGHT  ({len(lgt_attrs)})]:",  ", ".join(lgt_attrs))
    print(f"\n[⚙️  RENDER ({len(rnd_attrs)})]:", ", ".join(rnd_attrs))
    print("=" * 60)
    print(f"→ FULL LIST ({len(attrs)}):", ", ".join(attrs))
    print("=" * 60)
    print("[✅] DEBUG DONE — Đổi DEBUG_LUX_API=False rồi chạy lại")
else:
    main()
