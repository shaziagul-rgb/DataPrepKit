# DataPrepKit

A small Python command-line toolkit for preparing and checking image datasets before they are used in machine learning or computer vision workflows.

It focuses on the practical jobs that often sit around a training pipeline: finding images, checking whether files can be read, spotting exact duplicates, creating dataset reports, making file lists, and safely quarantining files that need attention.

## What it does

- Recursively scan for supported image files
- Validate images with Pillow
- Find exact duplicate files using SHA-256
- Generate basic dataset statistics in JSON
- Export image file lists
- Create train, validation, and test file lists
- Preview cleanup operations with `--dry-run`
- Move selected files to a quarantine folder instead of deleting them

Supported image formats: JPEG, PNG, BMP, TIFF, and WEBP.

## Installation

Python 3.10 or newer is recommended.

```bash
git clone <your-repository-url>
cd DataPrepKit
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

For development and tests:

```bash
pip install -r requirements-dev.txt
pytest
```

You can also install the command as a script with:

```bash
pip install -e .
```

Then use `dataprep` instead of `python -m dataprepkit`.

## Examples

Scan a dataset:

```bash
python -m dataprepkit scan ./images
```

Validate the images:

```bash
python -m dataprepkit validate ./images
```

Find exact duplicates:

```bash
python -m dataprepkit duplicates ./images
```

Create a JSON report:

```bash
python -m dataprepkit report ./images --output report.json
```

Export filenames, keeping paths relative to the dataset folder:

```bash
python -m dataprepkit export ./images --output files.txt --relative
```

Create train, validation, and test lists:

```bash
python -m dataprepkit split ./images --train 0.8 --val 0.1 --test 0.1
```

Preview cleanup without changing anything:

```bash
python -m dataprepkit clean ./images --remove-corrupted --remove-duplicates --dry-run
```

After checking the dry run, the selected files can be moved to quarantine:

```bash
python -m dataprepkit clean ./images --remove-corrupted --remove-duplicates --yes
```

## Safety

The `clean` command does not permanently delete files. Selected files are moved under `quarantine/cleanup/`, preserving their relative paths where possible.

For anything that changes the dataset, use `--dry-run` first. The quarantine directory is ignored by Git so it is not accidentally committed with the project.

## Project structure

```text
DataPrepKit/
├── dataprepkit/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── cleaner.py
│   ├── duplicates.py
│   ├── exporter.py
│   ├── scanner.py
│   ├── statistics.py
│   └── validator.py
├── tests/
├── .gitignore
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Notes

This project is intentionally lightweight. It is designed as a reusable utility for dataset preparation rather than as a full machine learning framework.

## License

MIT License. See [LICENSE](LICENSE) for details.
# DataPrepKit
