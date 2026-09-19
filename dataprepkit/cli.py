import argparse
import json
import random
from pathlib import Path

from .cleaner import quarantine
from .duplicates import find_duplicates
from .exporter import export_file_list
from .scanner import scan_images
from .statistics import dataset_statistics
from .validator import validate_image


def cmd_scan(args):
    paths = scan_images(args.folder)
    print(f"Images found: {len(paths)}")
    for path in paths:
        print(path.name)


def cmd_validate(args):
    paths = scan_images(args.folder)
    invalid = []
    for path in paths:
        ok, error = validate_image(path)
        if not ok:
            invalid.append((path, error))

    print(f"Checked: {len(paths)}")
    print(f"Valid: {len(paths) - len(invalid)}")
    print(f"Invalid: {len(invalid)}")
    for path, error in invalid:
        print(f"  {path}: {error}")


def cmd_duplicates(args):
    groups = find_duplicates(scan_images(args.folder))
    print(f"Duplicate groups: {len(groups)}")
    for digest, paths in groups.items():
        print(f"\nHash: {digest[:16]}...")
        for path in paths:
            print(f"  {path}")


def cmd_report(args):
    stats = dataset_statistics(scan_images(args.folder))
    text = json.dumps(stats, indent=2)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
        print(f"Report written to {args.output}")
    else:
        print(text)


def cmd_export(args):
    paths = scan_images(args.folder)
    export_file_list(paths, args.output, args.folder if args.relative else None)
    print(f"Wrote {len(paths)} filenames to {args.output}")


def cmd_split(args):
    paths = scan_images(args.folder)
    total = args.train + args.val + args.test
    if abs(total - 1.0) > 1e-9:
        raise SystemExit("train + val + test must equal 1.0")

    rng = random.Random(args.seed)
    rng.shuffle(paths)

    n = len(paths)
    train_end = int(n * args.train)
    val_end = train_end + int(n * args.val)

    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    export_file_list(paths[:train_end], output / "train.txt")
    export_file_list(paths[train_end:val_end], output / "validation.txt")
    export_file_list(paths[val_end:], output / "test.txt")
    print(f"Split {n} images into train/validation/test.")


def cmd_clean(args):
    paths = scan_images(args.folder)
    invalid = [path for path in paths if not validate_image(path)[0]]
    duplicate_groups = find_duplicates(paths)
    duplicates = [path for group in duplicate_groups.values() for path in group[1:]]

    targets = []
    if args.remove_corrupted:
        targets.extend(invalid)
    if args.remove_duplicates:
        targets.extend(duplicates)

    print(f"Files selected: {len(targets)}")
    if not targets:
        return

    if args.dry_run:
        print("DRY RUN: nothing was changed.")
        for path in targets:
            print(f"  {path}")
        return

    if not args.yes:
        answer = input("Move selected files to quarantine? [y/N] ")
        if answer.lower() != "y":
            print("Cancelled.")
            return

    moved = quarantine(targets, Path(args.folder), "cleanup")
    print(f"Quarantined: {len(moved)}")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="dataprep",
        description="Prepare, validate, inspect, and safely clean datasets.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("scan", help="List supported images in a folder")
    p.add_argument("folder")
    p.set_defaults(func=cmd_scan)

    p = sub.add_parser("validate", help="Check image files for read errors")
    p.add_argument("folder")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("duplicates", help="Find exact duplicate images")
    p.add_argument("folder")
    p.set_defaults(func=cmd_duplicates)

    p = sub.add_parser("report", help="Create dataset statistics")
    p.add_argument("folder")
    p.add_argument("--output")
    p.set_defaults(func=cmd_report)

    p = sub.add_parser("export", help="Write image filenames to a text file")
    p.add_argument("folder")
    p.add_argument("--output", default="train.txt")
    p.add_argument("--relative", action="store_true")
    p.set_defaults(func=cmd_export)

    p = sub.add_parser("split", help="Create train, validation, and test lists")
    p.add_argument("folder")
    p.add_argument("--output", default="dataset_lists")
    p.add_argument("--train", type=float, default=0.8)
    p.add_argument("--val", type=float, default=0.1)
    p.add_argument("--test", type=float, default=0.1)
    p.add_argument("--seed", type=int, default=42)
    p.set_defaults(func=cmd_split)

    p = sub.add_parser("clean", help="Quarantine corrupted or duplicate images")
    p.add_argument("folder")
    p.add_argument("--remove-corrupted", action="store_true")
    p.add_argument("--remove-duplicates", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--yes", action="store_true")
    p.set_defaults(func=cmd_clean)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
