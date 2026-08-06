import os
import sys
from pathlib import Path


def _normalize(arr_in: list) -> list:
    """remove empty elements of array"""
    return list(filter(None, arr_in))


def _setNoneIfEmpty(str_in: str) -> str | None:
    # print("_setNoneIfEmpty:", str_in)
    if str_in is None:
        return None
    trimmed = str_in.strip()
    trimmed = " ".join(trimmed.split())
    return trimmed if trimmed != "" else None


def logo_fn() -> str:
    return os.path.join(
        os.getenv("APPDATA"), "excel2zugferd", "logo.jpg"  # type: ignore
    )


def resource_path(*parts: str) -> Path:
    if getattr(sys, "frozen", False):
        resource_root = Path(sys._MEIPASS)  # type: ignore[attr-defined]
    else:
        resource_root = Path(__file__).resolve().parent.parent / "_internal"
    return resource_root.joinpath(*parts)
