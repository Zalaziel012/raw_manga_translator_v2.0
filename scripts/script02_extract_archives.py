import json
import zipfile
from pathlib import Path
import shutil

# ---- CONFIG ----
INPUT_DIR = Path("input/manga_to_be_translated")
WORKSPACE_DIR = Path("workspace")
ARCHIVES_JSON = WORKSPACE_DIR / "archives.json"

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def create_volume_structure(volume_dir: Path):
    subfolders = ["pages", "ocr", "translation", "edited"]
    for folder in subfolders:
        (volume_dir / folder).mkdir(parents=True, exist_ok=True)


def is_image_file(filename: str) -> bool:
    return Path(filename).suffix.lower() in IMAGE_EXTENSIONS


def extract_archive(archive_path: Path, volume_dir: Path):
    pages_dir = volume_dir / "pages"

    with zipfile.ZipFile(archive_path, "r") as zip_ref:
        image_files = [
            f for f in zip_ref.namelist()
            if not f.endswith("/") and is_image_file(f)
        ]

        image_files.sort()

        for index, file in enumerate(image_files, start=1):
            ext = Path(file).suffix.lower()
            new_name = f"{index:03d}{ext}"
            target_path = pages_dir / new_name

            with zip_ref.open(file) as source, open(target_path, "wb") as target:
                shutil.copyfileobj(source, target)


def main():
    print("📂 Script02 – Extracting archives")

    if not ARCHIVES_JSON.exists():
        raise FileNotFoundError("archives.json not found. Run Script01 first.")

    with open(ARCHIVES_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    archives = data.get("archives", [])

    if not archives:
        print("⚠️ No archives to extract.")
        return

    for archive_name in archives:
        archive_path = INPUT_DIR / archive_name
        volume_name = archive_path.stem
        volume_dir = WORKSPACE_DIR / volume_name

        print(f"📦 Processing: {archive_name}")

        create_volume_structure(volume_dir)

        extract_archive(archive_path, volume_dir)

        print(f"✅ Extracted to: {volume_dir / 'pages'}")

    print("🎉 Script02 completed successfully.")


if __name__ == "__main__":
    main()