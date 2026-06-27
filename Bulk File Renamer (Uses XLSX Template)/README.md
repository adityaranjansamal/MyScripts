# Batch File Renamer from Excel

Batch rename files in a directory using an Excel (`.xlsx`) file containing old and new filenames.

## Features

* Batch rename files from an Excel mapping
* Skips missing files
* Prevents overwriting existing files
* Displays a summary of renamed, skipped, and failed files

## Requirements

* Python 3.8+
* `openpyxl`

## Setup (Ubuntu)

```bash
# Clone the repository
git clone https://github.com/<your-username>/<repository-name>.git
cd <repository-name>

# Create and activate a virtual environment
sudo apt install python3-venv
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install openpyxl
```

## Usage

```bash
python3 rename_from_xlsx.py <folder> <rename_map.xlsx>
```

Example:

```bash
python3 rename_from_xlsx.py ~/Downloads/Movies rename_map.xlsx
```

## Excel Format

| Old Filename | New Filename |
| ------------ | ------------ |
| old.mp4      | new.mp4      |
| image.jpg    | vacation.jpg |

* Row 1 is the header.
* Column A: Existing filename
* Column B: New filename

## Example Output

```text
[OK] Movie1.mkv
[OK] Movie2.mkv
[SKIP] Missing: Movie3.mkv

==========
Renamed : 2
Skipped : 1
Errors  : 0
```

## Notes

* Does not overwrite existing files.
* Missing files are skipped automatically.
* Only filenames are required in the Excel sheet (no file paths).

## License

MIT License.
