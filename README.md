# raw_manga_translator

Manga Translator Pipeline

Automated manga translation: RAW ZIP/CBZ → ITA → Final CBZ

This pipeline uses Python and open-source modules to:

- Extract pages from ZIP/CBZ files
- Preprocess images
- Japanese/English OCR → JSON text
- Translate into Italian
- Clean up the original text
- Insert the translation into the balloons
- Generate final CBZ ready to read

Instructions:
1. Enter raw_manga_translator: `cd raw_manga_translator`
2. Install dependencies: `pip install -r requirements.txt`
3. Double-click on `run_pipeline.bat` or (in cmd) `python run_all_pipeline.py`

#######################################################################################

Italiano: Manga Translator Pipeline

Automated manga translation: RAW ZIP/CBZ → ITA → CBZ finale

Questa pipeline usa Python e moduli open-source per:

- Estrarre le pagine dai file ZIP/CBZ
- Preprocessare le immagini
- OCR giapponese/inglese → testo JSON
- Tradurre in italiano
- Pulire il testo originale
- Inserire la traduzione nelle balloon
- Generare CBZ finale pronto da leggere

Istruzioni:
1. Entra in raw_manga_translator: `cd raw_manga_translator`
2. Installa le dipendenze: `pip install -r requirements.txt`
3. Doppio click su `run_pipeline.bat` o (nel cmd) `python run_all_pipeline.py`