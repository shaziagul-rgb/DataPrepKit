from pathlib import Path


def export_file_list(paths, output, relative_to=None):
    """Write one file path per line, optionally relative to a dataset root."""
    output = Path(output)
    base = Path(relative_to).resolve() if relative_to else None
    lines = []

    for path in paths:
        path = Path(path)
        value = path.resolve().relative_to(base) if base else path.name
        lines.append(str(value).replace("\\", "/"))

    output.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
