import os
import json
from pathlib import Path

# ---- CONFIG ----
INPUT_DIR = Path("input/manga_to_be_translated")
WORKSPACE_DIR = Path("workspace")
OUTPUT_JSON = WORKSPACE_DIR / "archives.json"
SUPPORTED_EXTENSIONS = {".zip", ".cbz"}


def detect_archives(input_dir: Path):
    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")

    archives = []

    for file in input_dir.iterdir():
        if file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS:
            archives.append(file.name)

    return sorted(archives)


def main():
    print("📦 Script01 – Detecting ZIP / CBZ archives")

    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)

    archives = detect_archives(INPUT_DIR)

    data = {
        "input_directory": str(INPUT_DIR),
        "archives_found": len(archives),
        "archives": archives
    }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"✅ Found {len(archives)} archive(s)")
    print(f"📝 Saved list to: {OUTPUT_JSON}")

    if not archives:
        print("⚠️ No ZIP or CBZ files detected.")


if __name__ == "__main__":
    main()