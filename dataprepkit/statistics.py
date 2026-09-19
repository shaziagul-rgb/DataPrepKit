from collections import Counter

from .validator import image_info, validate_image


def dataset_statistics(paths):
    """Build a small JSON-friendly summary of an image dataset."""
    formats = Counter()
    dimensions = Counter()
    valid = 0
    invalid = []

    for path in paths:
        ok, error = validate_image(path)
        if not ok:
            invalid.append({"file": str(path), "error": error})
            continue

        valid += 1
        info = image_info(path)
        formats[info["format"]] += 1
        dimensions[f"{info['width']}x{info['height']}"] += 1

    return {
        "total": len(paths),
        "valid": valid,
        "invalid": len(invalid),
        "invalid_files": invalid,
        "formats": dict(formats),
        "dimensions": dict(dimensions),
    }
