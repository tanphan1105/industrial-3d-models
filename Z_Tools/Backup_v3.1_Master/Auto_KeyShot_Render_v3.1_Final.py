# -*- coding: utf-8 -*-
# ==============================================================================
# 🚀 NIGHT-CRAWLER KEYSHOT BATCH RENDER ENGINE v3.1 — MASTER EDITION
# Tác giả  : TANPHAN STUDIO x ANTIGRAVITY AI
# Dành cho : Hệ thống lọc nước RO & Thiết bị lọc công nghiệp
#
# Changelog v3.1 (so với v3.0):
# [OPT-A] main() tách thành _run_setup() / _run_batch() / _run_ar_export()
# [OPT-B] RenderContext mang đủ width/height — loại bỏ ternary logic trong main
# [OPT-C] Regex pattern dùng (?:^|[^a-z0-9]) thay vì lookbehind — match đầu string
# [OPT-D] force_ar tách khỏi COMMERCIAL_MODES data, vào AR_FORCE_MODES set
# [OPT-E] setup_environment cache light handles — không removeAllLights mỗi cam
# [OPT-F] OUTPUT_MODE source-of-truth duy nhất qua get_mode_config() cache
# [OPT-G] SnapshotManager class gom save/load + tái dùng scene-tree cache
# [OPT-H] _collect_scene_nodes() cache — tái dùng giữa apply_materials & snapshot
# ==============================================================================

import lux
import os
import re
import math
import datetime
import glob
import json
import traceback
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
DEBUG_LUX_API     = False       # ĐẶT True nếu cần dump API lần nữa

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
    "DRAFT":   {"samples":   80, "bounces":  8, "denoise": True, "denoise_blend": 0.85},
    "PREVIEW": {"samples":  300, "bounces": 16, "denoise": True, "denoise_blend": 0.95},
    "FINAL":   {"samples":  600, "bounces": 32, "denoise": True, "denoise_blend": 1.00},
    "ULTRA":   {"samples": 1200, "bounces": 48, "denoise": True, "denoise_blend": 1.00},
}

@dataclass
class RenderContext:
    """Immutable render configuration — không mutate global state."""
    quality: str
    width:   int
    height:  int

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
# [OPT-D] force_ar tách riêng khỏi data dict
# ==============================================================================
COMMERCIAL_MODES: Dict[str, Dict] = {
    "WEBSITE": {
        "cameras": ["B2B_01_hero_45deg", "B2B_05_macro_detail"],
        "quality": "FINAL", "width": 3840, "height": 2160,
        "passes":  ["Beauty", "Depth"],
        "note":    "Hero + macro. Max impact per frame — web hero banner.",
    },
    "CATALOG": {
        "cameras": ["B2B_01_hero_45deg", "B2B_03_front_elevation",
                    "B2B_04_side_elevation", "B2B_05_macro_detail"],
        "quality": "FINAL", "width": 4800, "height": 3200,
        "passes":  ["Beauty", "Depth", "MaterialID", "Normal"],
        "note":    "4 góc chuẩn B2B catalogue kỹ thuật. High-res cho in ấn.",
    },
    "DATASHEET": {
        "cameras": ["B2B_03_front_elevation", "B2B_04_side_elevation", "B2B_02_top_down"],
        "quality": "PREVIEW", "width": 2480, "height": 3508,
        "passes":  ["Beauty"],
        "note":    "Tỷ lệ A4. 3 góc kỹ thuật. Đủ cho P&ID / datasheet.",
    },
    "AR": {
        "cameras": ["B2B_01_hero_45deg"],
        "quality": "DRAFT", "width": 1920, "height": 1080,
        "passes":  ["Beauty"],
        "note":    "Thumbnail cho AR viewer. Export GLB/USDZ bắt buộc.",
    },
}

# [OPT-D] Tách logic AR export ra khỏi data
AR_FORCE_MODES = {"AR"}

_mode_cfg_cache: Optional[Dict] = None

def get_mode_config() -> Dict:
    """Source-of-truth duy nhất cho mode config. Cache sau lần đầu."""
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
                
            # Áp dụng Transform Matrix để chuyển từ Local sang Global Coordinates
            try:
                transform = node.getTransform()
                if transform:
                    # KeyShot luxmath.Vector * luxmath.Matrix4
                    p0 = p0 * transform
                    p1 = p1 * transform
            except:
                pass
                
            min_x = min(min_x, min(p0.x, p1.x))
            max_x = max(max_x, max(p0.x, p1.x))
            min_y = min(min_y, min(p0.y, p1.y))
            max_y = max(max_y, max(p0.y, p1.y))
            min_z = min(min_z, min(p0.z, p1.z))
            max_z = max(max_z, max(p0.z, p1.z))
            has_box = True
        except:
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
# ▶ SCENE NODE CACHE — [OPT-H] tái dùng giữa materials + snapshot
# ==============================================================================
_SCENE_NODES_CACHE: Optional[List] = None

def _collect_scene_nodes() -> List:
    """Duyệt scene tree một lần duy nhất, cache cho toàn pipeline."""
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
    
    # 4 Góc nhìn chếch lên (Low-angle 3/4) - Elevation -10
    ("B2B_05_Low_FrontRight", (  45.0, -10.0)),
    ("B2B_06_Low_FrontLeft",  ( -45.0, -10.0)),
    ("B2B_07_Low_BackLeft",   (-135.0, -10.0)),
    ("B2B_08_Low_BackRight",  ( 135.0, -10.0)),
]
CAMERA_FOCAL_MM = {
    name: 50.0 for name, _ in CAMERA_DEFS
}
# Giảm Focal Length của các góc Low-Angle để tạo hiệu ứng hùng vĩ (Heroic scale)
for name, _ in CAMERA_DEFS:
    if "Low" in name:
        CAMERA_FOCAL_MM[name] = 35.0

# Hệ số zoom-out sau setStandardView (>1.0 = xa thêm, tự động theo kích thước model)
CAMERA_ZOOM_OUT = 1.65  
CAMERA_SAMPLE_MULTIPLIER = {
    name: 1.0 for name, _ in CAMERA_DEFS
}

# Xóa _CAM_DIR_MAP cũ vì dùng Spherical Coordinates

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

def _get_scene_center_via_bbox() -> List:
    # Bị lỗi tâm trên KeyShot 2025.1. Chuyển sang dùng hàm get_scene_bounds()
    pass

def setup_camera() -> None:
    """Setup cameras — KeyShot 2025.1 API safe."""
    log("CAM", "Setup Camera System v3.1 (KS2025.1 safe)…")

    existing = set()
    try:
        for cam in lux.getCameras():
            try:
                existing.add(cam.getName())
            except:
                pass
    except:
        pass

    (cx, cy, cz), max_dim, _ = get_scene_bounds()

    # Map mỗi camera B2B → VIEW constant chuẩn KeyShot
    _VIEW_MAP = {
        "B2B_01_hero_45deg":        getattr(lux, "VIEW_ISOMETRIC", None),
        "B2B_02_hero_left_45deg":   None, # Dùng Vector Direction, không dùng Standard View
        "B2B_03_hero_low_angle":    None,
        "B2B_04_top_down":          getattr(lux, "VIEW_TOP",        None),
        "B2B_05_macro_detail":      getattr(lux, "VIEW_ISOMETRIC",  None),
    }

    for name, _ in CAMERA_DEFS:
        if name in existing:
            log("INFO", f"Camera Guard (skip): {name}")
            continue
        try:
            lux_safe("newCamera", name)
            lux_safe("setCamera",  name)
            
            # 1. Để KeyShot tự động Fit to View toàn bộ mô hình (Chống trật tâm)
            lux_safe("setStandardView", getattr(lux, "VIEW_ISOMETRIC", 6))
            
            # 2. Rút xuất tọa độ LookAt và Distance chuẩn do KeyShot vừa tính
            auto_dist = lux_safe("getCameraDistance")
            if not auto_dist or auto_dist <= 0: auto_dist = max_dim * 1.5
            final_dist = auto_dist * CAMERA_ZOOM_OUT
            
            # 3. Sử dụng SphericalCamera (API chuẩn KeyShot 2025.1)
            azimuth, elevation = dict(CAMERA_DEFS).get(name, (45.0, 35.0))
            
            try:
                lux.setSphericalCamera(azimuth, elevation, 0.0)
                lux.setCameraDistance(final_dist)
                log("CAM", f"  Spherical Setup {name}: Az={azimuth}, El={elevation}, Dist={final_dist:.1f}")
            except Exception as e:
                log("WARN", f"Spherical Camera Fallback failed: {e}")
            # ✅ Step 3: focal length phù hợp góc nhìn
            lux_safe("setCameraFocalLength", CAMERA_FOCAL_MM.get(name, 50.0))
            lux_safe("saveCamera", name)
            log("CAM", f"  Created: {name}")
        except Exception as e:
            log("WARN", f"Camera {name}: {e}")

    lux_safe("setCamera",      "B2B_01_Top_FrontRight")
    log("CAM", "Camera System READY")

# ==============================================================================
# ▶ ENVIRONMENT & LIGHTING
# [OPT-E] Cache light handles — tránh removeAllLights mỗi camera
# ==============================================================================
_HDRI_SEARCH_PATHS = [
    r"C:\Users\Public\Documents\KeyShot*\Environments\Studio\3 Panels Straight*.hdz",
    r"C:\Users\Public\Documents\KeyShot*\Environments\Studio\Studio Soft Box*.hdz",
    r"C:\Users\Public\Documents\KeyShot*\Environments\Studio\Product Light*.hdz",
    r"C:\Users\Public\Documents\KeyShot*\Environments\Interior\White Room*.hdz",
]
_HDRI_PATH_CACHE: Optional[str] = None
_LIGHT_HANDLES: Dict[str, Any] = {}  # [OPT-E] name → light handle

def _load_best_hdri() -> bool:
    global _HDRI_PATH_CACHE
    if _HDRI_PATH_CACHE:
        lux_safe("setEnvironmentImage", _HDRI_PATH_CACHE)
        return True
    for pattern in _HDRI_SEARCH_PATHS:
        files = glob.glob(pattern)
        if files:
            _HDRI_PATH_CACHE = files[-1]
            log("LIGHT", f"HDRI: {os.path.basename(_HDRI_PATH_CACHE)}")
            lux_safe("setEnvironmentImage", _HDRI_PATH_CACHE)
            return True
    log("WARN", "Không tìm được HDRI — dùng default KeyShot")
    return False

_HAS_TRANSPARENT_HOUSING: Optional[bool] = None
_TRANSPARENT_KW = ("ly l", "acrylic", "housing", "vessel", "filter bowl", "ly loc")

def _detect_transparent_housing() -> bool:
    global _HAS_TRANSPARENT_HOUSING
    if _HAS_TRANSPARENT_HOUSING is None:
        try:
            names = [n.getName().lower() for n in _collect_scene_nodes()]
            _HAS_TRANSPARENT_HOUSING = any(
                kw in nm for nm in names for kw in _TRANSPARENT_KW
            )
        except:
            _HAS_TRANSPARENT_HOUSING = False
    return _HAS_TRANSPARENT_HOUSING

_ENV_PRIORITY = [
    "GSGProStudiosMetalVol2",     # Greyscalegorilla Metal Studio Vol2 ← tốt nhất
    "GSGPROSTUDIOSMETAL001",      # Greyscalegorilla Metal Studio 1
    "ModernIndustrial",           # GSG Modern Industrial
    "3 Point Medium",             # Studio 3-point clean
    "3 Point Light",              # Studio 3-point bright
    "Grey Studio Grey Floor",     # Neutral grey studio
    "Startup Balanced",           # KeyShot default balanced
    "Studio Backdrop",            # Basic backdrop
]

def _find_best_env() -> Any:
    """Tìm HDRI tốt nhất trong library theo thứ tự ưu tiên công nghiệp."""
    try:
        envs = list(lux.getLibraryEnvironments() or [])
        for kw in _ENV_PRIORITY:
            kw_l = kw.lower()
            for e in envs:
                if kw_l in str(e).lower():
                    return e
        return envs[0] if envs else None
    except:
        return None

def setup_environment(active_camera: str = "B2B_01_hero_45deg") -> None:
    """Auto-setup môi trường công nghiệp: HDRI + Lighting Preset chuẩn B2B."""
    log("LIGHT", f"Setup Lighting [{active_camera}]…")

    # ✅ Bước 1: Tìm và set HDRI tốt nhất từ Library
    env = _find_best_env()
    if env is not None:
        try:
            lux.setActiveEnvironment(env)
            log("LIGHT", f"  HDRI: {str(env).split('/')[-1]}")
            
            # ✅ Bước 2: Kích hoạt Adaptive Optics (Thuật toán 3 Nguồn sáng thông minh)
            _, max_dim, _ = get_scene_bounds()
            try:
                # KeyShot 2025.1 API: Lấy Object Env hiện tại
                active_env = lux.getActiveEnvironment()
                if active_env:
                    # Xoay HDRI 115 độ tạo Rim Light
                    active_env.setRotation(115.0)
                    
                    if max_dim > 1.0:
                        active_env.setBrightness(2.2)
                        log("LIGHT", f"  [Adaptive Optics] B2B Skid (max_dim={max_dim:.1f}) ➔ B=2.2, Rot=115°")
                    else:
                        active_env.setBrightness(1.8)
                        log("LIGHT", f"  [Adaptive Optics] B2B Component (max_dim={max_dim:.1f}) ➔ B=1.8, Rot=115°")
            except Exception as e:
                log("WARN", f"  Env Optics Sync Fail: {e}")

        except Exception as e:
            log("WARN", f"  setActiveEnvironment: {e}")
    else:
        log("WARN", "  Không tìm được HDRI Library")

    # ✅ Bước 3: Lighting Preset — ưu tiên Product/Studio/3-Point
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

    log("LIGHT", "Lighting READY")

# ==============================================================================
# ▶ MATERIAL LIBRARY
# ==============================================================================

# Từ khóa EXACT từ KeyShot Material Library dump (953 materials)
_LIBRARY_SEARCH_MAP: Dict[str, List[str]] = {
    # Vật liệu kính — dùng cho housing, boảng mạch, vỏ trong suốt
    "Solid Glass":              ["Glass (Solid) White", "Glass (Solid) Grey", "Glass Basic White"],
    # Thép không gỉ — dùng cho pipe, fitting, valve, flange
    "Brushed Stainless Steel":  ["Stainless Steel Brushed Medium", "Stainless Steel Brushed Heavy", "Steel Brushed"],
    # Gang — dùng cho pump body, heavy bracket
    "Cast Iron":                ["Iron Rough", "Iron Brushed", "Steel Rough"],
    # Đồng thẩu — dùng cho connector, coupling, brass fitting
    "Brass":                    ["Brass Polished", "Brass Brushed"],
    # Nhựa xám nhạt — dùng cho filter housing, enclosure
    "Plastic Rough Light Gray": ["Hard Rough Plastic Grey", "Hard Rough Plastic White"],
    # Nhựa trắng — dùng cho RO membrane housing, tank
    "Plastic Rough White":      ["Hard Rough Plastic White", "Hard Rough Plastic Grey"],
    # Nhựa có vân — dùng cho panel, cover
    "Plastic Textured":         ["Hard Textured Plastic Grey", "Mold-Tech MT-14218"],
    # Sơn mờ — dùng cho frame, stand, base plate
    "Paint Matte":              ["Paint Matte Grey", "Matte Grey"],
    # Cao su cứng — dùng cho gasket, seal, o-ring
    "Rubber Hard Black":        ["Rubber", "Tire"],
    # Vải lọ/ felt — dùng cho filter media, pre-filter
    "Felt":                     ["Cloth Weave Black 1mm", "Nylon Weave Black 3mm"],
    # Nhựa hạt mịn — dùng cho sensor body, small component
    "Plastic Fine Grain":       ["Mold-Tech MT-11020 Spray Dot", "Hard Textured Plastic Grey"],
    # Sợi carbon / fiber — dùng cho filter cartridge, membrane wrap
    "Fiber":                    ["Nylon Weave Black 3mm", "Carbon Fiber Rough 5mm"],
    
    # ===== COLOR-BASED SMART MAPPING =====
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
    
    # --- Colored Metals ---
    "Metal Blue":               ["Anodized Aluminum Brushed Blue", "Paint Metallic Blue"],
    "Metal Red":                ["Anodized Aluminum Brushed Red", "Paint Metallic Red"],
    "Metal Orange":             ["Anodized Aluminum Brushed Orange", "Paint Metallic Orange peel Orange"],
    "Metal Yellow":             ["Anodized Aluminum Brushed Yellow", "Paint Metallic Yellow"],
    "Metal Green":              ["Paint Metallic Lime Green", "Paint Metallic Green"],
    "Metal Purple":             ["Anodized Aluminum Brushed Purple", "Paint Metallic Purple"],
    "Metal Black":              ["Anodized Aluminum Brushed Black", "Paint Metallic Black"],
    "Metal White":              ["Paint Metallic White", "Automotive White"],
}
# Fallback SHADER_TYPE khi không tìm được trong Library
_SHADER_MAP: Dict[str, Any] = {
    "Solid Glass":              getattr(lux, "SHADER_TYPE_GLASS_SOLID",  None),
    "Brushed Stainless Steel":  getattr(lux, "SHADER_TYPE_BRUSHED",      None),
    "Cast Iron":                getattr(lux, "SHADER_TYPE_METAL",        None),
    "Brass":                    getattr(lux, "SHADER_TYPE_METAL",        None),
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

# Cache Library materials — chỉ gọi getLibraryMaterials() 1 lần
_LIB_MATERIALS_CACHE: Optional[List] = None

def _guess_profile_from_color(name_to_check: str) -> Optional[str]:
    """Phân tích chuỗi color:R:G:B từ Inventor để chọn profile tốt nhất."""
    match = re.search(r'color:(\d+):(\d+):(\d+)', name_to_check)
    if not match:
        return None
        
    r, g, b = int(match.group(1)), int(match.group(2)), int(match.group(3))
    
    if r < 50 and g < 50 and b < 50:
        return "Rubber Hard Black" if "seal" in name_to_check or "o" in name_to_check else "Plastic Black"
    if r > 200 and g < 80 and b < 80:
        return "Plastic Red"
    if b > 180 and r < 100:
        if "than" in name_to_check or "housing" in name_to_check or "ly" in name_to_check:
            return "Solid Glass Blue"
        return "Plastic Blue"
    if r > 220 and g > 220 and b > 220:
        if "loi" in name_to_check or "cartridge" in name_to_check:
            return "Filter Cartridge White"
        return "Plastic Rough White"
    if r > 240 and g > 210 and b > 150:
        return "Plastic Beige"
    if r > 200 and g > 180 and b < 100:
        return "Brass"
    
    return "Plastic Rough Light Gray"

def _get_lib_materials() -> List:
    global _LIB_MATERIALS_CACHE
    if _LIB_MATERIALS_CACHE is None:
        try:
            _LIB_MATERIALS_CACHE = list(lux.getLibraryMaterials()) or []
            n = len(_LIB_MATERIALS_CACHE)
            log("MAT", f"  Library: {n} materials available")
            sample = [str(m) for m in _LIB_MATERIALS_CACHE[:3]]
            log("MAT", f"  Sample str(mat): {sample}")
        except Exception as e:
            log("WARN", f"getLibraryMaterials: {e}")
            _LIB_MATERIALS_CACHE = []
    return _LIB_MATERIALS_CACHE

def _find_library_material(mat_type: str) -> Any:
    """Tìm material cao cấp trong KeyShot Library theo keywords ưu tiên."""
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
            except:
                continue
    return None

def _apply_lib_mat(node: Any, lib_mat: Any) -> bool:
    """Áp dụng library material chuẩn cho KeyShot 2025.1"""
    mat_name = str(lib_mat)
    
    # Trích xuất node ID
    node_id = None
    if hasattr(node, "getID"): node_id = node.getID()
    elif hasattr(node, "id"): node_id = node.id
    elif hasattr(node, "ID"): node_id = node.ID
    else: node_id = node

    try:
        # KeyShot 2025.1 yêu cầu dict {node_id: material_name_string}
        lux.applyMaterialMapping({node_id: mat_name})
        log("MAT", f"  ✅ Đã áp dụng: {mat_name}")
        return True
    except Exception as e:
        log("MAT", f"  ❌ applyMaterialMapping fail: {e}")
        return False

def _apply_material_profile(node: Any, profile: Dict) -> None:
    mat_type = profile.get("type")
    if not mat_type:
        return
    
    # ✅ Ưu tiên 1: Tìm chính xác tên trong KeyShot Library
    lib_mat = _find_library_material(mat_type)
    if lib_mat is not None:
        if _apply_lib_mat(node, lib_mat):
            return
    # ✅ Ưu tiên 2: createSceneMaterial (SHADER_TYPE_*)
    try:
        shader = _SHADER_MAP.get(mat_type) or _SHADER_FALLBACK
        if shader:
            mat = lux.createSceneMaterial(shader)
            if mat is not None:
                lux.setObjectMaterial(node_name, mat)
    except Exception as e:
        log("WARN", f"_apply_material_profile({mat_type}): {e}")

def _guess_profile_from_inventor_material(node_name: str, mat_name: str) -> Optional[str]:
    """Phân tích TÊN VẬT LIỆU (Tính chất vật lý) và MÀU SẮC (Hiển thị) từ Inventor."""
    node_name = (node_name or "").lower().strip()
    mat_name = (mat_name or "").lower().strip()
    full_str = f"{node_name} | {mat_name}"
    
    r = g = b = -1
    has_color = False
    match = re.search(r'color:(\d+):(\d+):(\d+)', full_str)
    if match:
        r, g, b = int(match.group(1)), int(match.group(2)), int(match.group(3))
        has_color = True

    # --- Hàm con: Phân loại màu thành tên Vật Liệu ---
    def _get_color_variant(base_type: str):
        if not has_color: return None
        
        # Đen / Xám đậm
        if r < 100 and g < 100 and b < 100: 
            return f"{base_type} Black" if base_type != "Glass" else "Solid Glass"
            
        # Các màu cơ bản
        if r > 150 and g > 150 and b < 100: return f"{base_type} Yellow" if base_type != "Glass" else "Solid Glass"
        if r > 150 and g > 70 and g < 150 and b < 80: return f"{base_type} Orange" if base_type != "Glass" else "Solid Glass Red"
        if r > 150 and g < 80 and b < 80: return "Solid Glass Red" if base_type == "Glass" else f"{base_type} Red"
        if g > 120 and r < 100 and b < 100: return f"{base_type} Green" if base_type != "Glass" else "Solid Glass"
        if r > 120 and b > 120 and g < 80: return f"{base_type} Purple" if base_type != "Glass" else "Solid Glass"
        if b > 150 and r < 150: return "Solid Glass Blue" if base_type == "Glass" else f"{base_type} Blue"
        
        # Nhóm màu sáng
        if r > 200 and g > 200 and b > 200: 
            if base_type == "Plastic": return "Filter Cartridge White"
            if base_type == "Metal": return "Metal White"
            return "Solid Glass"
            
        if r > 200 and g > 150 and b < 180: return "Plastic Beige" # Cho các nắp ly lọc màu vàng nhạt/Beige
        return None

    # --- 1. NHẬN DIỆN KIM LOẠI / CAO SU (Ưu tiên thuộc tính vật lý, sau đó áp màu) ---
    if "rubber" in mat_name or "epdm" in mat_name or "viton" in mat_name or "silicone" in mat_name:
        return "Rubber Hard Black" # Cao su mặc định là đen
        
    is_metal = False
    if "stainless" in mat_name or "inox" in mat_name: return "Brushed Stainless Steel" # Inox giữ nguyên bản
    if "brass" in mat_name or "copper" in mat_name or "bronze" in mat_name or "dong" in mat_name: return "Brass"
    if "steel" in mat_name or "iron" in mat_name or "cast" in mat_name or "metal" in mat_name or "thep" in mat_name or "gang" in mat_name or "nhom" in mat_name or "aluminum" in mat_name: is_metal = True
    
    if is_metal:
        color_mat = _get_color_variant("Metal")
        if color_mat: return color_mat
        return "Cast Iron"

    # --- 2. NHẬN DIỆN KÍNH / TRONG SUỐT ---
    if "glass" in mat_name or "clear" in mat_name or "acrylic" in mat_name or "polycarbonate" in mat_name:
        color_mat = _get_color_variant("Glass")
        if color_mat: return color_mat
        if "blue" in mat_name: return "Solid Glass Blue"
        if "red" in mat_name: return "Solid Glass Red"
        return "Solid Glass"

    # --- 3. NHẬN DIỆN NHỰA CÔNG NGHIỆP ---
    if "pvc" in mat_name or "hdpe" in mat_name or "plastic" in mat_name or "nylon" in mat_name or "pp" in mat_name or "nhua" in mat_name or "upvc" in mat_name:
        color_mat = _get_color_variant("Plastic")
        if color_mat: return color_mat
        return "Plastic Rough Light Gray"

    # --- 4. FALLBACK KHÔNG RÕ VẬT LIỆU: ĐOÁN DỰA TRÊN MÀU RGB ---
    if has_color:
        if r < 100 and g < 100 and b < 100:
            if "rubber" in full_str or "seal" in full_str or "o-ring" in full_str or "gasket" in full_str:
                return "Rubber Hard Black"
            return "Plastic Black"
            
        if r > 150 and g > 150 and b < 100: return "Plastic Yellow"
        if r > 150 and g > 70 and g < 150 and b < 80: return "Plastic Orange"
        if r > 150 and g < 80 and b < 80: return "Plastic Red"
        if g > 120 and r < 100 and b < 100: return "Plastic Green"
        if r > 120 and b > 120 and g < 80: return "Plastic Purple"
        if b > 150 and r < 150: return "Solid Glass Blue"  
        if r > 200 and g > 200 and b > 200: return "Filter Cartridge White"
        if r > 200 and g > 150 and b < 180: return "Plastic Beige"
        if r > 200 and g > 180 and b < 100: return "Brass"
            
    return None

def apply_materials() -> None:
    log("MAT", "Apply Industrial Materials v3.1…")
    assigned = fallback = skipped = 0

    # Lấy danh sách toàn bộ vật liệu KeyShot hợp lệ để tránh ghi đè khi chạy lại
    valid_ks_mats = set(m.lower() for mats in _LIBRARY_SEARCH_MAP.values() for m in mats)

    for node in _collect_scene_nodes():
        try:
            node_name = node.getName().lower()
            if "__lock" in node_name:
                skipped += 1
                continue

            # Lấy tên vật liệu gốc từ node (Do Inventor gán)
            mat_name = ""
            if hasattr(node, "getMaterial"):
                try:
                    mat_obj = node.getMaterial()
                    mat_name = (mat_obj.getName() if hasattr(mat_obj, "getName") else str(mat_obj)).lower()
                except:
                    pass
            
            # TRÁNH GHI ĐÈ: Nếu vật liệu hiện tại đã là vật liệu KeyShot xịn, bỏ qua!
            if mat_name in valid_ks_mats:
                assigned += 1
                continue
                
            # --- TÌM MÀU TRONG NODE_NAME VÀ MAT_NAME ---
            profile_type = _guess_profile_from_inventor_material(node_name, mat_name)
            
            if profile_type:
                log("MAT", f"  [{node_name[:20]}] InventorMat({mat_name[:25]}) ➔ {profile_type}")
                _apply_material_profile(node, {"type": profile_type})
                assigned += 1
            else:
                # Nếu không xác định được vật liệu/màu, gán mặc định
                fb_shader = _SHADER_FALLBACK
                if fb_shader:
                    try:
                        mat = lux.createSceneMaterial(fb_shader)
                        if mat: lux.setObjectMaterial(node.getName(), mat)
                    except:
                        pass
                fallback += 1

        except Exception as e:
            log("WARN", f"Node processing fail: {e}")

    log("MAT", f"Materials READY — assigned={assigned}, fallback={fallback}, skipped={skipped}")

# ==============================================================================
# ▶ RENDER ENGINE
# ==============================================================================
def setup_render_engine(ctx: RenderContext) -> None:
    preset = ctx.preset()
    log("REND", f"Quality: {ctx.quality} (samples={preset['samples']}, bounces={preset['bounces']})")

    # ✅ GPU luôn ưu tiên — RENDER_ENGINE_PRODUCT_GPU (KS2025.1)
    gpu_engine = (
        getattr(lux, "RENDER_ENGINE_PRODUCT_GPU",  None) or  # ✅ KS2025.1
        getattr(lux, "RENDER_ENGINE_INTERIOR_GPU", None) or  # fallback GPU
        getattr(lux, "RENDER_ENGINE_GPU",          None) or  # legacy
        getattr(lux, "RENDER_ENGINE_PRODUCT",      None)      # CPU fallback
    )
    if gpu_engine is not None:
        lux.setRenderEngine(gpu_engine)
        log("REND", f"Render Engine: GPU ({gpu_engine})")
    else:
        log("WARN", "Không tìm được GPU engine — dùng default")
    lux_safe("setGPURender", True)  # bỏ qua nếu KS2025.1 không có

def _make_render_opts(ctx: RenderContext, cam_name: str) -> Any:
    preset   = ctx.preset()
    adjusted = int(preset["samples"] * CAMERA_SAMPLE_MULTIPLIER.get(cam_name, 1.0))

    opts = lux.getRenderOptions()
    opts.setMaxSamples(adjusted)
    opts.setRayBounces(preset["bounces"])
    opts.setGlobalIllumination(True)
    opts.setIncludeAlpha(True)

    if ctx.quality in ("FINAL", "ULTRA") and hasattr(opts, "setClampSamples"):
        safe(opts.setClampSamples, 150)

    try:
        opts.setOutputPasses(["Beauty", "Depth", "MaterialID", "Normal", "Diffuse"])
    except:
        pass

    if preset["denoise"]:
        if hasattr(opts, "setDenoise"): safe(opts.setDenoise, True)
        if hasattr(opts, "setDenoiseBlend"): safe(opts.setDenoiseBlend, preset["denoise_blend"])

    log("REND", f"  Opts: {adjusted} samples (×{CAMERA_SAMPLE_MULTIPLIER.get(cam_name, 1.0)}) / {preset['bounces']} bounces")
    return opts

# ==============================================================================
# ▶ SMART RENDER
# ==============================================================================
def smart_render(cam_name: str, out_path: str, ctx: RenderContext) -> bool:
    if RESUME_RENDER and os.path.exists(out_path):
        log("INFO", f"SKIP (đã có): {os.path.basename(out_path)}")
        return False

    w, h = ctx.width, ctx.height
    draft_path = None

    if DRAFT_PRECHECK and ctx.quality in ("FINAL", "ULTRA"):
        draft_path = out_path.replace(".png", "_precheck.png")
        draft_ctx  = RenderContext(quality="DRAFT", width=w // 6, height=h // 6)
        lux.renderImage(draft_path, w // 6, h // 6, _make_render_opts(draft_ctx, cam_name))
        log("REND", f"  Draft → {os.path.basename(draft_path)}")

    lux.renderImage(out_path, w, h, _make_render_opts(ctx, cam_name))
    log("OK", f"Saved: {os.path.basename(out_path)}")
    MetadataScrubber.scrub(out_path)

    if draft_path and os.path.exists(draft_path):
        try:
            os.remove(draft_path)
        except:
            pass

    return True

# ==============================================================================
# ▶ METADATA SCRUBBER (Education / B2B Compliance)
# ==============================================================================
class MetadataScrubber:
    @staticmethod
    def scrub_png(filepath: str) -> None:
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
            signature = b'\x89PNG\r\n\x1a\n'
            if not data.startswith(signature): return
            
            out_data = bytearray(signature)
            idx = 8
            # Các chunks tEXt, iTXt, zTXt, eXIf chứa metadata/KeyShot info
            unsafe_chunks = {b'tEXt', b'iTXt', b'zTXt', b'eXIf'}
            scrubbed = 0
            
            while idx < len(data):
                if idx + 8 > len(data): break
                length = int.from_bytes(data[idx:idx+4], 'big')
                chunk_type = data[idx+4:idx+8]
                
                if chunk_type not in unsafe_chunks:
                    out_data.extend(data[idx:idx+12+length])
                else:
                    scrubbed += 1
                idx += 12 + length
                
            if scrubbed > 0:
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
            if not data.startswith(b'glTF'): return
            
            version = int.from_bytes(data[4:8], 'little')
            json_chunk_len = int.from_bytes(data[12:16], 'little')
            json_chunk_type = data[16:20]
            if json_chunk_type != b'JSON': return
            
            json_data = data[20:20+json_chunk_len]
            bin_start = 20 + json_chunk_len
            
            js = json.loads(json_data.decode('utf-8'))
            modified = False
            
            if "asset" in js:
                if "generator" in js["asset"]:
                    js["asset"]["generator"] = "Tanphan OS v3.1"
                    modified = True
                for k in ["copyright", "extras"]:
                    if k in js["asset"]:
                        del js["asset"][k]
                        modified = True
                        
            if not modified: return
            
            new_json_str = json.dumps(js, separators=(',', ':'))
            padding = (4 - (len(new_json_str) % 4)) % 4
            new_json_str += " " * padding
            new_json_bytes = new_json_str.encode('utf-8')
            new_json_len = len(new_json_bytes)
            new_total_len = 12 + 8 + new_json_len + (len(data) - bin_start)
            
            out_data = bytearray()
            out_data.extend(b'glTF')
            out_data.extend(version.to_bytes(4, 'little'))
            out_data.extend(new_total_len.to_bytes(4, 'little'))
            out_data.extend(new_json_len.to_bytes(4, 'little'))
            out_data.extend(b'JSON')
            out_data.extend(new_json_bytes)
            out_data.extend(data[bin_start:])
            
            with open(filepath, 'wb') as f:
                f.write(out_data)
            log("INFO", f"  Scrubbed GLB metadata (Generator: Tanphan OS)")
        except Exception as e:
            log("WARN", f"Scrub GLB failed: {e}")

    @classmethod
    def scrub(cls, filepath: str) -> None:
        if not os.path.exists(filepath): return
        ext = filepath.lower().split('.')[-1]
        if ext == 'png':
            cls.scrub_png(filepath)
        elif ext == 'glb':
            cls.scrub_glb(filepath)

# ==============================================================================
# ▶ SNAPSHOT MANAGER — [OPT-G] gom save/load, tái dùng node cache
# ==============================================================================
class SnapshotManager:
    VERSION = "3.1"

    def __init__(self, path: str):
        self.path = path

    def save(self) -> None:
        log("SNAP", f"SAVE → {self.path}")
        snap: Dict = {
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
            log("OK",   f"Snapshot saved: {self.path}")
            log("INFO", f"  {len(snap['cameras'])} cameras, {len(snap['materials'])} material overrides")
        except Exception as e:
            log("ERR", f"Không ghi được snapshot: {e}")

    def load(self) -> None:
        if not os.path.exists(self.path):
            log("WARN", f"Snapshot không tồn tại: {self.path}")
            return
        log("SNAP", f"LOAD ← {self.path}")
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                snap = json.load(f)
        except Exception as e:
            log("ERR", f"Không đọc được snapshot: {e}")
            return

        log("INFO", f"  v{snap.get('version','?')} từ: {snap.get('saved_at','?')}")
        self._apply_environment(snap.get("environment", {}))
        self._apply_materials(snap.get("materials", {}))

    # ── Private ──────────────────────────────────────────────────────────
    def _read_environment(self) -> Dict:
        return {
            "brightness": lux_safe("getEnvironmentBrightness"),
            "contrast":   lux_safe("getEnvironmentContrast"),
            "rotation":   lux_safe("getEnvironmentRotation"),
            "hdri_file":  _HDRI_PATH_CACHE or "",
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
                    except:
                        pass
        except:
            pass
        return result

    def _read_materials(self) -> Dict:
        result: Dict = {}
        for node in _collect_scene_nodes():  # [OPT-G] tái dùng cache
            try:
                mat = node.getMaterial()
                if mat:
                    name = mat.getName() if hasattr(mat, "getName") else str(mat)
                    if name:
                        result[node.getName()] = name
            except:
                pass
        return result

    def _apply_environment(self, env: Dict) -> None:
        hdri = env.get("hdri_file", "")
        if hdri and os.path.exists(hdri):
            lux_safe("setEnvironmentImage", hdri)
        for key, fn in [
            ("brightness", lux.setEnvironmentBrightness),
            ("contrast",   lux.setEnvironmentContrast),
            ("rotation",   lux.setEnvironmentRotation),
        ]:
            if env.get(key) is not None:
                safe(fn, env[key])
        log("LIGHT", "Environment restored")

    def _apply_materials(self, mat_map: Dict) -> None:
        restored = sum(
            1 for node in _collect_scene_nodes()
            if node.getName() in mat_map
            and safe(node.setMaterial, mat_map[node.getName()]) is not None
        )
        log("MAT", f"Materials restored: {restored}/{len(mat_map)}")

# ==============================================================================
# ▶ MAIN PIPELINE — [OPT-A] tách thành 3 sub-functions
# ==============================================================================
_snapshot = SnapshotManager(SNAPSHOT_FILE)

def _run_setup(ctx: RenderContext) -> None:
    """Phase 1: Materials, cameras, render engine."""
    if SNAPSHOT_MODE == "LOAD":
        _snapshot.load()
    else:
        apply_materials()

    setup_camera()
    setup_render_engine(ctx)

    if SNAPSHOT_MODE == "SAVE":
        _snapshot.save()

    log("OK", "SETUP COMPLETE")

def _run_batch(ctx: RenderContext, mode_cfg: Dict) -> None:
    """Phase 2: Batch render tất cả cameras theo mode."""
    out_dir = get_output_dir()

    cams = ["B2B_01_hero_45deg"] if AUTO_RENDER_MODE == "HERO" else mode_cfg["cameras"]
    total = len(cams)
    done = skipped = 0
    errors: List[Tuple[str, str]] = []

    log("FILM", f"BATCH [{ctx.width}×{ctx.height}] | Mode={OUTPUT_MODE} → {out_dir}")

    for idx, cam in enumerate(cams, 1):
        bar = "█" * idx + "░" * (total - idx)
        log("PROG", f"[{bar}] {idx}/{total} — {cam}")
        try:
            lux_safe("setCamera", cam)
            setup_environment(active_camera=cam)
            out_path = os.path.join(out_dir, f"{cam}_{OUTPUT_MODE}_{ctx.quality}.png")
            done += smart_render(cam, out_path, ctx)
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
    except:
        pass

def _run_ar_export(out_dir: str) -> None:
    """Phase 3: AR asset export (GLB + USDZ)."""
    glb_path = os.path.join(out_dir, "B2B_RO_System_AR.glb")
    usdz_path = os.path.join(out_dir, "B2B_RO_System_AR.usdz")
    lux_safe("exportFile", glb_path)
    lux_safe("exportFile", usdz_path)
    MetadataScrubber.scrub(glb_path)
    MetadataScrubber.scrub(usdz_path)
    log("OK", f"AR assets exported & scrubbed → {out_dir}")

def main() -> None:
    _validate_config()
    log("HEAD", "NIGHT-CRAWLER v3.1 — COMMERCIAL RENDER OS BOOTING")

    mode_cfg = get_mode_config()

    # [OPT-B] RenderContext quyết định đầy đủ — không cần ternary ngoài
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
        # [OPT-D] Dùng AR_FORCE_MODES thay vì truy cập COMMERCIAL_MODES dict
        if EXPORT_WEB_AR or OUTPUT_MODE in AR_FORCE_MODES:
            _run_ar_export(get_output_dir())
    else:
        setup_environment(active_camera="B2B_01_hero_45deg")
        log("INFO", "Interactive mode — đổi AUTO_RENDER_MODE='HERO'/'ALL_CAMERAS' để render")

    print("─" * 60)
    log("HEAD", "NIGHT-CRAWLER v3.1 — SESSION END")

# ==============================================================================
# ▶ ENTRY POINT
# ==============================================================================
if DEBUG_LUX_API:
    attrs = sorted(dir(lux))
    print("="*60)
    print(f"⭐ LUX API DUMP — KeyShot {len(attrs)} attributes")
    print("="*60)
    cam_attrs = [a for a in attrs if "amera" in a or "cam" in a.lower()]
    env_attrs = [a for a in attrs if "nviron" in a or "hdri" in a.lower() or "lighting" in a.lower()]
    mat_attrs = [a for a in attrs if "aterial" in a or "mat" in a.lower()]
    lgt_attrs = [a for a in attrs if "ight" in a.lower() and "lightning" not in a.lower()]
    rnd_attrs = [a for a in attrs if "ender" in a.lower() or "RENDER" in a]
    print(f"\n[📸 CAMERA ({len(cam_attrs)})]:", ", ".join(cam_attrs))
    print(f"\n[💡 ENVIRONMENT ({len(env_attrs)})]:", ", ".join(env_attrs))
    print(f"\n[🎨 MATERIAL ({len(mat_attrs)})]:", ", ".join(mat_attrs))
    print(f"\n[💡 LIGHT ({len(lgt_attrs)})]:", ", ".join(lgt_attrs))
    print(f"\n[⚙️  RENDER ({len(rnd_attrs)})]:", ", ".join(rnd_attrs))
    print("="*60)
    print(f"→ FULL LIST ({len(attrs)} attrs):", ", ".join(attrs))
    print("="*60)
    print("[✅] DEBUG DONE — Đổi DEBUG_LUX_API=False rồi chạy lại")
else:
    main()