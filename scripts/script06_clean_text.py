import json
import cv2
import numpy as np
from pathlib import Path

# ---- CONFIG ----
WORKSPACE_DIR = Path("workspace")

INPAINT_RADIUS = 3   # dimensione maschera text removal


def clean_page(volume_dir: Path, ocr_file: Path):
    pages_dir = volume_dir / "pages"
    edited_dir = volume_dir / "edited"
    edited_dir.mkdir(exist_ok=True)

    page_name = ocr_file.stem + Path(ocr_file).suffix.replace(".json", "")
    with open(ocr_file, "r", encoding="utf-8") as f:
        ocr_data = json.load(f)

    page_image_path = pages_dir / ocr_data.get("page")
    img = cv2.imread(str(page_image_path))
    if img is None:
        print(f"⚠️ Cannot read image: {page_image_path}")
        return

    mask = np.zeros(img.shape[:2], dtype=np.uint8)

    for block in ocr_data.get("blocks", []):
        bbox = block.get("bbox")
        if not bbox:
            continue

        pts = np.array(bbox, dtype=np.int32)
        cv2.fillPoly(mask, [pts], 255)

    # inpainting
    cleaned = cv2.inpaint(img, mask, INPAINT_RADIUS, cv2.INPAINT_TELEA)

    output_path = edited_dir / page_image_path.name
    cv2.imwrite(str(output_path), cleaned)


def process_volume(volume_dir: Path):
    ocr_dir = volume_dir / "ocr"
    print(f"🖌️  Cleaning text in volume: {volume_dir.name}")

    for ocr_file in sorted(ocr_dir.glob("*.json")):
        clean_page(volume_dir, ocr_file)


def main():
    print("🧹 Script06 – Clean Text / Inpainting")

    if not WORKSPACE_DIR.exists():
        raise FileNotFoundError("Workspace not found. Run previous scripts first.")

    for volume_dir in WORKSPACE_DIR.iterdir():
        if volume_dir.is_dir():
            process_volume(volume_dir)

    print("✅ Script06 completed successfully.")


if __name__ == "__main__":
    main()