import json
from pathlib import Path
from transformers import MarianMTModel, MarianTokenizer
from langdetect import detect
import yaml

# ---- CONFIG ----
CONFIG_PATH = Path("config.yaml")
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

WORKSPACE_DIR = Path(config["paths"]["workspace_dir"])
TRANSLATION_DIR_NAME = "translation"
BATCH_SIZE = config["translation"].get("batch_size", 8)

# Modelli MarianMT
MODEL_MAPPING = {
    "ja": "Helsinki-NLP/opus-mt-ja-it",
    "en": "Helsinki-NLP/opus-mt-en-it"
}

# Cache modelli
MODEL_CACHE = {}

def get_model_and_tokenizer(lang_code):
    if lang_code not in MODEL_CACHE:
        model_name = MODEL_MAPPING.get(lang_code)
        if not model_name:
            raise ValueError(f"No translation model for language: {lang_code}")
        print(f"🔹 Loading model {model_name} for {lang_code} ...")
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        MODEL_CACHE[lang_code] = (model, tokenizer)
    return MODEL_CACHE[lang_code]

def translate_block(text_block, lang_code):
    model, tokenizer = get_model_and_tokenizer(lang_code)
    # batching opzionale
    inputs = tokenizer([text_block], return_tensors="pt", padding=True)
    outputs = model.generate(**inputs)
    translated = [tokenizer.decode(t, skip_special_tokens=True) for t in outputs]
    return translated[0]

def main():
    print("📝 Script05 – Translate OCR → ITA")

    for volume_dir in WORKSPACE_DIR.iterdir():
        if not volume_dir.is_dir():
            continue

        ocr_dir = volume_dir / "ocr"
        translation_dir = volume_dir / TRANSLATION_DIR_NAME
        translation_dir.mkdir(exist_ok=True)

        for ocr_file in ocr_dir.glob("*.json"):
            with open(ocr_file, "r", encoding="utf-8") as f:
                ocr_data = json.load(f)

            translated_data = []
            for block in ocr_data:
                text = block.get("text", "")
                if not text.strip():
                    translated_text = ""
                else:
                    # rileva lingua
                    try:
                        lang_code = detect(text)
                        if lang_code not in MODEL_MAPPING:
                            lang_code = "ja"  # fallback
                    except:
                        lang_code = "ja"

                    translated_text = translate_block(text, lang_code)

                # salva il blocco tradotto
                translated_block = block.copy()
                translated_block["text_it"] = translated_text
                translated_data.append(translated_block)

            # salva JSON tradotto
            translation_file = translation_dir / ocr_file.name
            with open(translation_file, "w", encoding="utf-8") as f:
                json.dump(translated_data, f, ensure_ascii=False, indent=4)

            print(f"✅ Translated {ocr_file.name} → {translation_file.name}")

    print("🎉 All volumes translated successfully!")

if __name__ == "__main__":
    main()