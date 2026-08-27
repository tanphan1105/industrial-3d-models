# -*- coding: utf-8 -*-
# ==============================================================================
# 🚀 KEYSHOT MAX SCENE EXPORTER v2.1 (B2B MASTER EDITION)
# Tác giả  : TANPHAN STUDIO x ANTIGRAVITY AI
# Mục tiêu : Trích xuất 100% Data từ Scene thành JSON (Dùng cho ML / Pipeline)
# ==============================================================================

import lux
import json
import os
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

# =========================
# CONFIG
# =========================
EXPORT_DIR = r"d:\WT3D_Project\Z_Tools\Exported_Data"


# =========================
# DATA TYPES
# =========================
@dataclass
class ExportResult:
    name: str
    success: bool
    path: Optional[str] = None
    error: Optional[str] = None


# =========================
# CORE UTILS
# =========================
def _serialize(obj: Any) -> Any:
    """Convert lux Vector / tuple / list → JSON-safe types."""
    if hasattr(obj, 'x') and hasattr(obj, 'y') and hasattr(obj, 'z'):
        return [obj.x, obj.y, obj.z]
    if isinstance(obj, (tuple, list)):
        return [_serialize(i) for i in obj]
    return obj


def safe_get(fn_name: str, *args, **kwargs) -> Any:
    """Gọi KeyShot API an toàn qua chuỗi tên hàm — không quăng lỗi nếu API không tồn tại."""
    try:
        fn = getattr(lux, fn_name)
        return _serialize(fn(*args, **kwargs))
    except Exception:
        return None


def _get_mat_name(mat: Any) -> Optional[str]:
    """Trích tên material từ cả str lẫn lux.Material object."""
    if isinstance(mat, str):
        return mat or None
    if mat and hasattr(mat, "getName"):
        return mat.getName()
    return None


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
            try:
                lux.setCamera(active)
            except Exception:
                pass


# =========================
# EXPORTER CLASS
# =========================
class SceneExporter:
    def __init__(self, base_dir: str):
        # Tạo subfolder theo timestamp để không bị ghi đè khi chạy nhiều mô hình
        session_id = time.strftime("%Y%m%d_%H%M%S")
        self.export_dir = os.path.join(base_dir, f"Scene_{session_id}")
        os.makedirs(self.export_dir, exist_ok=True)
        self.results: List[ExportResult] = []

    # ── File I/O ──────────────────────────────────────────────
    def _save(self, filename: str, data: Any) -> ExportResult:
        path = os.path.join(self.export_dir, filename)
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"  ✅ {filename}")
            return ExportResult(name=filename, success=True, path=path)
        except Exception as e:
            print(f"  ❌ {filename}: {e}")
            return ExportResult(name=filename, success=False, error=str(e))

    # ── 1. Cameras ────────────────────────────────────────────
    def export_cameras(self) -> None:
        data: Dict[str, Any] = {}
        cameras = []
        try:
            for c in lux.getCameras():
                try: cameras.append(c.getName() if hasattr(c, "getName") else str(c))
                except Exception: pass
        except Exception:
            pass

        with _preserve_camera():
            for cam in cameras:
                try:
                    lux.setCamera(cam)
                    data[cam] = {
                        "focal_length":   safe_get("getCameraFocalLength"),
                        "fov":            safe_get("getCameraFOV"),
                        "position":       safe_get("getCameraPosition"),
                        "direction":      safe_get("getCameraDirection"),
                        "up_vector":      safe_get("getCameraUpVector"),
                        "dof_enabled":    safe_get("getCameraDepthOfField"),
                        "focus_distance": safe_get("getCameraFocusDistance"),
                    }
                except Exception:
                    data[cam] = None

        self.results.append(self._save("cameras.json", data))

    # ── 2. Environment ────────────────────────────────────────
    def export_environment(self) -> None:
        data = {
            "environment_image": safe_get("getEnvironmentImage"),
            "brightness":        safe_get("getEnvironmentBrightness"),
            "contrast":          safe_get("getEnvironmentContrast"),
            "rotation":          safe_get("getEnvironmentRotation"),
            "background_type":   safe_get("getBackgroundType"),
            "ground_shadow":     safe_get("getGroundShadows"),
        }
        self.results.append(self._save("environment.json", data))

    # ── 3. Materials ──────────────────────────────────────────
    def _collect_node_data(self):
        """Duyệt scene tree một lần duy nhất, trả về (usage_list, mat_set)."""
        usage: List[Dict] = []
        mat_names: set = set()

        try:
            nodes = lux.getSceneTree().find()
        except Exception:
            return usage, mat_names

        for node in nodes:
            try:
                mat_name = _get_mat_name(node.getMaterial())
                usage.append({"part_name": node.getName(), "material": mat_name})
                if mat_name:
                    mat_names.add(mat_name)
            except Exception:
                pass

        return usage, mat_names

    def export_materials(self) -> None:
        usage, mat_names = self._collect_node_data()
        self.results.append(self._save("material_usage.json", usage))
        self.results.append(self._save("materials_list.json", sorted(mat_names)))

    # ── 4. Scene Meta ─────────────────────────────────────────
    def export_scene_meta(self) -> None:
        data = {
            "export_time":      time.strftime("%Y-%m-%d %H:%M:%S"),
            "keyshot_version":  safe_get("getVersion") or "2025.1",
            "unit_system":      safe_get("getUnitSystem"),
            "scene_bbox":       safe_get("getSceneBoundingBox"),
        }
        self.results.append(self._save("scene_meta.json", data))

    # ── Summary ───────────────────────────────────────────────
    def _print_summary(self) -> None:
        ok  = [r for r in self.results if r.success]
        err = [r for r in self.results if not r.success]
        print(f"\n{'─'*50}")
        print(f"  ✅ {len(ok)} files exported  |  ❌ {len(err)} errors")
        if err:
            for r in err:
                print(f"     • {r.name}: {r.error}")
        print(f"  📁 {self.export_dir}")
        print(f"{'─'*50}")

    # ── Entry Point ───────────────────────────────────────────
    def run(self) -> None:
        print("🚀 KEYSHOT MAX EXPORTER v2.1 – START\n")
        self.export_cameras()
        self.export_environment()
        self.export_materials()
        self.export_scene_meta()
        self._print_summary()
        print("🎯 DONE")


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    SceneExporter(EXPORT_DIR).run()
