from pathlib import Path

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}


def scan_images(folder):
    """Return supported image files below a folder, in a stable order."""
    folder = Path(folder)
    return sorted(
        path
        for path in folder.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def scan_files(folder):
    """Return all files below a folder, including non-image files."""
    folder = Path(folder)
    return sorted(path for path in folder.rglob("*") if path.is_file())
