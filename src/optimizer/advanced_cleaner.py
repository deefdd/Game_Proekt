import os
import shutil
from pathlib import Path
from src.utils.logger import log
from src.config import settings

# Paths for advanced cleaning
PREFETCH_PATH = Path("C:/Windows/Prefetch")
WINDOWS_UPDATE_CACHE = Path("C:/Windows/SoftwareDistribution/Download")

LOCAL_APPDATA = os.getenv("LOCALAPPDATA") or ""
NVIDIA_DXCACHE = Path(LOCAL_APPDATA) / "NVIDIA" / "DXCache"
NVIDIA_GLCACHE = Path(LOCAL_APPDATA) / "NVIDIA" / "GLCache"
AMD_SHADER_CACHE = Path(LOCAL_APPDATA) / "AMD" / "DxCache"


def safe_delete(path: Path) -> int:
    """
    Deletes all files and folders inside a directory.
    Returns number of removed items.
    """
    if not path.exists() or not path.is_dir():
        return 0

    removed = 0

    try:
        items = list(path.iterdir())
    except PermissionError:
        return 0

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
    """
    Cleans: Prefetch, Shader Cache (NVIDIA/AMD), Windows Update Cache.
    Behavior is controlled by settings.json -> advanced_cleaner section.
    """
    removed_prefetch = 0
    removed_update_cache = 0
    removed_shader_cache = 0

    if settings["advanced_cleaner"]["remove_prefetch"]:
        removed_prefetch = safe_delete(PREFETCH_PATH)

    if settings["advanced_cleaner"]["remove_shader_cache"]:
        removed_shader_cache = (
            safe_delete(NVIDIA_DXCACHE)
            + safe_delete(NVIDIA_GLCACHE)
            + safe_delete(AMD_SHADER_CACHE)
        )

    if settings["advanced_cleaner"]["remove_windows_update_cache"]:
        removed_update_cache = safe_delete(WINDOWS_UPDATE_CACHE)

    log("advanced_cleaner", f"Prefetch removed: {removed_prefetch}")
    log("advanced_cleaner", f"Shader cache removed: {removed_shader_cache}")
    log("advanced_cleaner", f"Windows Update cache removed: {removed_update_cache}")

    return {
        "prefetch_removed": removed_prefetch,
        "shader_cache_removed": removed_shader_cache,
        "update_cache_removed": removed_update_cache,
    }
