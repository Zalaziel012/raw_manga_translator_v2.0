import shutil
from pathlib import Path

# ---- CONFIG ----
WORKSPACE_DIR = Path("workspace")
INPUT_DIR = Path("input/manga_to_be_translated")
OUTPUT_DIR = Path("output")

def sanity_check():
    print("🔎 Sanity Check - Project Status\n")

    if not INPUT_DIR.exists():
        print(f"❌ Input folder missing: {INPUT_DIR}")
    else:
        archives = list(INPUT_DIR.glob("*"))
        print(f"📦 Archives in input: {len(archives)}")

    if not WORKSPACE_DIR.exists():
        print(f"⚠️ Workspace not found: {WORKSPACE_DIR}")
    else:
        volumes = [v for v in WORKSPACE_DIR.iterdir() if v.is_dir()]
        print(f"📂 Volumes in workspace: {len(volumes)}")
        for vol in volumes:
            pages = list((vol / "pages").glob("*")) if (vol / "pages").exists() else []
            ocr = list((vol / "ocr").glob("*.json")) if (vol / "ocr").exists() else []
            translation = list((vol / "translation").glob("*.json")) if (vol / "translation").exists() else []
            edited = list((vol / "edited").glob("*")) if (vol / "edited").exists() else []

            print(f"  - {vol.name}: pages={len(pages)}, ocr={len(ocr)}, translation={len(translation)}, edited={len(edited)}")

    if not OUTPUT_DIR.exists():
        print(f"⚠️ Output folder not found: {OUTPUT_DIR}")
    else:
        cbz_files = list(OUTPUT_DIR.glob("*.cbz"))
        print(f"📚 CBZ/ZIP files in output: {len(cbz_files)}")

def reset_workspace():
    confirm = input("⚠️ Do you really want to RESET workspace and output? (y/N): ")
    if confirm.lower() == 'y':
        if WORKSPACE_DIR.exists():
            shutil.rmtree(WORKSPACE_DIR)
            print(f"🧹 Deleted {WORKSPACE_DIR}")
        if OUTPUT_DIR.exists():
            shutil.rmtree(OUTPUT_DIR)
            print(f"🧹 Deleted {OUTPUT_DIR}")
        print("✅ Workspace and output reset complete!")
    else:
        print("❌ Reset cancelled.")

def main():
    print("🛠️  Script00 – Sanity Check / Reset Workspace")
    sanity_check()

    action = input("\nDo you want to RESET workspace/output? (y/N): ")
    if action.lower() == 'y':
        reset_workspace()
    else:
        print("✅ No changes made.")

if __name__ == "__main__":
    main()