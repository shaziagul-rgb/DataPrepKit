import hashlib
from collections import defaultdict


def file_hash(path, chunk_size=1024 * 1024):
    """Hash a file in chunks so large files do not need to fit in memory."""
    digest = hashlib.sha256()
    with open(path, "rb") as file:
        while chunk := file.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def find_duplicates(paths):
    """Group files that have identical SHA-256 hashes."""
    groups = defaultdict(list)
    for path in paths:
        groups[file_hash(path)].append(path)
    return {digest: items for digest, items in groups.items() if len(items) > 1}
