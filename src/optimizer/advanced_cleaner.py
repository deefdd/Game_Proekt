import os
import shutil
from pathlib import Path
from src.utils.logger import log
from src.config import settings


# Paths
PREFETCH_PATH = Path("C:/Windows/Prefetch")
WINDOWS_UPDATE_CACHE = Path("C:/Windows/SoftwareDistribution/Download")

LOCAL_APPDATA = os.getenv("LOCALAPPDATA", "")
NVIDIA_DXCACHE = Path(LOCAL_APPDATA) / "NVIDIA" / "DXCache"
NVIDIA_GLCACHE = Path(LOCAL_APPDATA) / "NVIDIA" / "GLCache"
AMD_SHADER_CACHE = Path(LOCAL_APPDATA) / "AMD" / "DxCache"


def can_access_dir(path: Path) -> bool:
    try:
        if not path.exists() or not path.is_dir():
            return False
        next(path.iterdir(), None)
        return True
    except PermissionError:
        return False
    except Exception:
        return False


def safe_delete(path: Path, dry_run: bool = False) -> int:
    if not can_access_dir(path):
        return 0

    try:
        items = list(path.iterdir())
    except Exception:
        return 0

    if dry_run:
        return len(items)

    removed = 0
    for item in items:
        try:
            if item.is_file():
                item.unlink()
                removed += 1
            elif item.is_dir():
                shutil.rmtree(item, ignore_errors=True)
                removed += 1
        except Exception:
            continue

    return removed


def advanced_cleaner() -> dict:
    dry_run = bool(settings.get("ux", {}).get("dry_run", False))

    removed_prefetch = 0
    removed_shader_cache = 0
    removed_update_cache = 0

    adv_cfg = settings.get("advanced_cleaner", {})

    if adv_cfg.get("remove_prefetch", False):
        removed_prefetch = safe_delete(PREFETCH_PATH, dry_run=dry_run)

    if adv_cfg.get("remove_shader_cache", False):
        removed_shader_cache += safe_delete(NVIDIA_DXCACHE, dry_run=dry_run)
        removed_shader_cache += safe_delete(NVIDIA_GLCACHE, dry_run=dry_run)
        removed_shader_cache += safe_delete(AMD_SHADER_CACHE, dry_run=dry_run)

    if adv_cfg.get("remove_windows_update_cache", False):
        removed_update_cache = safe_delete(WINDOWS_UPDATE_CACHE, dry_run=dry_run)

    prefix = "[DRY-RUN] " if dry_run else ""
    log("advanced_cleaner", f"{prefix}Prefetch removed: {removed_prefetch}")
    log("advanced_cleaner", f"{prefix}Shader cache removed: {removed_shader_cache}")
    log("advanced_cleaner", f"{prefix}Windows Update cache removed: {removed_update_cache}")

    return {
        "prefetch_removed": removed_prefetch,
        "shader_cache_removed": removed_shader_cache,
        "update_cache_removed": removed_update_cache,
        "dry_run": dry_run,
    }
