import shutil
from pathlib import Path


def quarantine(paths, root, category, dry_run=False):
    """Move selected files into a quarantine folder instead of deleting them."""
    root = Path(root)
    destination = root / "quarantine" / category
    moved = []

    for path in paths:
        path = Path(path)
        relative = path.relative_to(root)
        target = destination / relative
        moved.append((path, target))

        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(path), str(target))

    return moved
