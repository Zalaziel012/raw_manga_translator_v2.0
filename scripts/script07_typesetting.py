import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import yaml

# ---- CONFIG ----
CONFIG_PATH = Path("config.yaml")
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

WORKSPACE_DIR = Path(config["paths"]["workspace_dir"])
FONT_PATH = Path(config["paths"]["fonts_dir"]) / config["font"]["ttf"]
FONT_SIZE = config["font"].get("size", 30)
PADDING = config["font"].get("padding", 5)
EDITED_DIR_NAME = "edited"
FINAL_DIR_NAME = "final"
TRANSLATION_DIR_NAME = "translation"

font = ImageFont.truetype(str(FONT_PATH), FONT_SIZE)

def typeset_volume(volume_dir: Path):
    translation_dir = volume_dir / TRANSLATION_DIR_NAME
    final_dir = volume_dir / EDITED_DIR_NAME / FINAL_DIR_NAME
    final_dir.mkdir(parents=True, exist_ok=True)

    for translation_file in translation_dir.glob("*.json"):
        with open(translation_file, "r", encoding="utf-8") as f:
            blocks = json.load(f)

        for block in blocks:
            img_path = volume_dir / EDITED_DIR_NAME / block["image_name"]
            if not img_path.exists():
                print(f"⚠️ Image not found: {img_path}")
                continue

            img = Image.open(img_path).convert("RGBA")
            draw = ImageDraw.Draw(img)

            # disegna testo tradotto italiano
            text_it = block.get("text_it", "")
            if text_it.strip():
                # posiziona testo centrato nel bounding box
                bbox = block.get("bbox", [0, 0, img.width, img.height])
                x1, y1, x2, y2 = bbox
                max_width = x2 - x1 - 2*PADDING

                # Word wrap semplice
                lines = []
                words = text_it.split()
                line = ""
                for word in words:
                    test_line = f"{line} {word}".strip()
                    w, h = draw.textsize(test_line, font=font)
                    if w <= max_width:
                        line = test_line
                    else:
                        lines.append(line)
                        line = word
                lines.append(line)

                # calcola altezza totale
                line_height = font.getsize("A")[1] + 2
                total_height = line_height * len(lines)
                y_text = y1 + (y2 - y1 - total_height) // 2

                for line in lines:
                    w, h = draw.textsize(line, font=font)
                    x_text = x1 + (max_width - w)//2 + PADDING
                    draw.text((x_text, y_text), line, font=font, fill=(0,0,0))
                    y_text += line_height

            # salva immagine finale
            final_img_path = final_dir / img_path.name
            img.save(final_img_path)

        print(f"✅ Volume {volume_dir.name} typeset completed!")

def main():
    print("🖌️ Script07 – Typesetting translated text")
    for volume_dir in WORKSPACE_DIR.iterdir():
        if not volume_dir.is_dir():
            continue
        typeset_volume(volume_dir)
    print("🎉 All volumes typeset successfully!")

if __name__ == "__main__":
    main()