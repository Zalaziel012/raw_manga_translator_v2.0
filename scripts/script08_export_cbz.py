from pathlib import Path
import zipfile
import shutil
import yaml

# ---- CONFIG ----
CONFIG_PATH = Path("config.yaml")
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

WORKSPACE_DIR = Path(config["paths"]["workspace_dir"])
OUTPUT_DIR = Path(config["paths"]["output_dir"])
OUTPUT_DIR.mkdir(exist_ok=True)

FINAL_DIR_NAME = "final"
EDITED_DIR_NAME = "edited"

def create_cbz(volume_dir: Path):
    final_dir = volume_dir / EDITED_DIR_NAME / FINAL_DIR_NAME
    if not final_dir.exists():
        print(f"⚠️ Final images not found for {volume_dir.name}")
        return

    cbz_name = OUTPUT_DIR / f"{volume_dir.name}.cbz"
    with zipfile.ZipFile(cbz_name, 'w') as cbz:
        # aggiunge le immagini ordinate
        for img_path in sorted(final_dir.iterdir()):
            cbz.write(img_path, arcname=img_path.name)

    print(f"✅ Created CBZ: {cbz_name.name}")

def main():
    print("📦 Script08 – Export CBZ")
    for volume_dir in WORKSPACE_DIR.iterdir():
        if not volume_dir.is_dir():
            continue
        create_cbz(volume_dir)

    print("🎉 All CBZ files created successfully!")

if __name__ == "__main__":
    main()