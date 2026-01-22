import json
from pathlib import Path
from PIL import Image
import pytesseract
from itertools import islice

# ---- CONFIG ----
WORKSPACE_DIR = Path("workspace")
LANGUAGE = "eng"       # "ita" per italiano, "jpn" per giapponese
MIN_CONFIDENCE = 30    # ignora i blocchi con confidenza inferiore a 30%
MAX_WIDTH = 1000       # ridimensiona immagini troppo grandi
CHUNK_SIZE = 5         # numero di immagini per "flusso" / chunk

# ---------- FUNZIONI ----------

def run_ocr_on_image(image_path: Path):
    # Apri immagine con PIL
    image = Image.open(image_path)

    # Resize se troppo larga
    w, h = image.size
    if w > MAX_WIDTH:
        scale = MAX_WIDTH / w
        new_size = (int(w * scale), int(h * scale))
        image = image.resize(new_size, Image.ANTIALIAS)

    # OCR con bounding box
    data = pytesseract.image_to_data(
        image,
        lang=LANGUAGE,
        output_type=pytesseract.Output.DICT
    )

    blocks = []
    n_boxes = len(data['level'])
    for i in range(n_boxes):
        text = data['text'][i].strip()
        conf = float(data['conf'][i])
        if text and conf >= MIN_CONFIDENCE:
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            bbox_list = [
                [x, y],
                [x + w, y],
                [x + w, y + h],
                [x, y + h]
            ]
            blocks.append({
                "bbox": bbox_list,
                "text": text,
                "confidence": round(conf, 2)
            })

    return blocks


def chunks(iterable, size):
    """Generator per dividere iterable in chunk di dimensione fissa."""
    it = iter(iterable)
    while True:
        chunk = list(islice(it, size))
        if not chunk:
            break
        yield chunk


def process_volume(volume_dir: Path):
    pages_dir = volume_dir / "pages"
    ocr_dir = volume_dir / "ocr"
    ocr_dir.mkdir(exist_ok=True)

    images = sorted([img for img in pages_dir.glob("*")
                     if img.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}])

    print(f"🔍 OCR on volume: {volume_dir.name} ({len(images)} pages)")

    # Dividi immagini in chunk
    for chunk_idx, image_chunk in enumerate(chunks(images, CHUNK_SIZE), 1):
        print(f"   ⚡ Processing chunk {chunk_idx} ({len(image_chunk)} images)")

        for img_path in image_chunk:
            print(f"      📄 Processing {img_path.name}")
            blocks = run_ocr_on_image(img_path)

            output = {
                "page": img_path.name,
                "blocks": blocks
            }

            json_path = ocr_dir / f"{img_path.stem}.json"
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(output, f, indent=4, ensure_ascii=False)


def main():
    print("🧠 Script OCR con Tesseract – Chunked")

    if not WORKSPACE_DIR.exists():
        raise FileNotFoundError("Workspace not found. Run previous scripts first.")

    for volume_dir in WORKSPACE_DIR.iterdir():
        if volume_dir.is_dir():
            process_volume(volume_dir)

    print("✅ OCR completato con successo.")


if __name__ == "__main__":
    main()