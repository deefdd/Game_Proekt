import os
import shutil
from pathlib import Path
from src.utils.logger import log


# Paths for advanced cleaning
PREFETCH_PATH = Path("C:/Windows/Prefetch")
WINDOWS_UPDATE_CACHE = Path("C:/Windows/SoftwareDistribution/Download")

# Shader cache paths
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
    Logs results to logs/advanced_cleaner.log
    """
    removed_prefetch = safe_delete(PREFETCH_PATH)
    removed_update_cache = safe_delete(WINDOWS_UPDATE_CACHE)

    removed_nvidia_dx = safe_delete(NVIDIA_DXCACHE)
    removed_nvidia_gl = safe_delete(NVIDIA_GLCACHE)
    removed_amd_cache = safe_delete(AMD_SHADER_CACHE)

    shader_removed = removed_nvidia_dx + removed_nvidia_gl + removed_amd_cache

    # logging here – we have access to all counters
    log("advanced_cleaner", f"Prefetch removed: {removed_prefetch}")
    log("advanced_cleaner", f"Shader cache removed: {shader_removed}")
    log("advanced_cleaner", f"Update cache removed: {removed_update_cache}")

    return {
        "prefetch_removed": removed_prefetch,
        "shader_cache_removed": shader_removed,
        "update_cache_removed": removed_update_cache,
    }
