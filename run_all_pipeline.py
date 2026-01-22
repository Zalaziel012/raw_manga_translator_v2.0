import subprocess
import sys
from pathlib import Path

# ---- CONFIG ----
SCRIPTS_ORDER = [
    "script00_sanity_reset.py",
    "script01_detect_archives.py",
    "script02_extract_archives.py",
    "script03_preprocess_images.py",
    "script04_ocr.py",
    "script05_translate.py",
    "script06_clean_text.py",
    "script07_typesetting.py",
    "script08_export_cbz.py"
]

SCRIPTS_DIR = Path("scripts")  # dove sono tutti gli script

def run_script(script_path: Path):
    print(f"\n▶️ Running {script_path.name} ...")
    result = subprocess.run([sys.executable, str(script_path)])
    if result.returncode != 0:
        print(f"❌ Script failed: {script_path.name}")
        sys.exit(1)  # ferma tutto se uno script fallisce
    print(f"✅ Completed {script_path.name}")

def main():
    print("🚀 Running full Manga Translation Pipeline\n")
    for script_name in SCRIPTS_ORDER:
        script_path = SCRIPTS_DIR / script_name
        if not script_path.exists():
            print(f"❌ Script not found: {script_path}")
            sys.exit(1)
        run_script(script_path)

    print("\n🎉 All scripts completed successfully! Your manga CBZ files are in `output/`")

if __name__ == "__main__":
    main()