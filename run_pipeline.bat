@echo off
REM ----------------------------------------
REM Manga Translator Pipeline - Windows BAT
REM ----------------------------------------

REM Attiva eventuale ambiente virtuale (modifica se usi venv)
REM call venv\Scripts\activate

echo 🚀 Eseguo run_all_pipeline.py ...

python run_all_pipeline.py

if %ERRORLEVEL% neq 0 (
    echo ❌ La pipeline ha riscontrato un errore.
    pause
    exit /b %ERRORLEVEL%
)

echo 🎉 Pipeline completata con successo!
pause