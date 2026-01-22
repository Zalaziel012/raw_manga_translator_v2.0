import cv2
import numpy as np
from pathlib import Path

# ---- CONFIG ----
WORKSPACE_DIR = Path("workspace")
MAX_WIDTH = 2000        # px massimi
DENOISE_STRENGTH = 10   # più alto = più aggressivo


def preprocess_image(image_path: Path):
    img = cv2.imread(str(image_path))

    if img is None:
        print(f"⚠️ Cannot read image: {image_path}")
        return

    # 1. Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. Denoising (ottimo per screentone)
    denoised = cv2.fastNlMeansDenoising(
        gray,
        h=DENOISE_STRENGTH,
        templateWindowSize=7,
        searchWindowSize=21
    )

    # 3. Adaptive threshold
    thresh = cv2.adaptiveThreshold(
        denoised,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        2
    )

    # 4. Resize opzionale
    h, w = thresh.shape
    if w > MAX_WIDTH:
        scale = MAX_WIDTH / w
        new_size = (int(w * scale), int(h * scale))
        thresh = cv2.resize(thresh, new_size, interpolation=cv2.INTER_AREA)

    # Sovrascrive l'immagine originale
    cv2.imwrite(str(image_path), thresh)


def process_volume(volume_dir: Path):
    pages_dir = volume_dir / "pages"

    if not pages_dir.exists():
        return

    images = sorted(pages_dir.glob("*"))

    print(f"🖼️  Preprocessing {len(images)} page(s) in {volume_dir.name}")

    for img_path in images:
        if img_path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            continue

        preprocess_image(img_path)


def main():
    print("🧪 Script03 – Preprocessing images")

    if not WORKSPACE_DIR.exists():
        raise FileNotFoundError("Workspace not found. Run Script02 first.")

    for volume_dir in WORKSPACE_DIR.iterdir():
        if volume_dir.is_dir():
            process_volume(volume_dir)

    print("✅ Script03 completed successfully.")


if __name__ == "__main__":
    main()