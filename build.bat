@echo off
REM ============================================================
REM  Compila KNAVE.exe (Windows). Ejecutar dentro del proyecto.
REM  Resultado: dist\KNAVE\KNAVE.exe  (carpeta autocontenida)
REM ============================================================
cd /d "%~dp0"
if not exist .venv ( python -m venv .venv )
call .venv\Scripts\activate.bat
pip install -q -r requirements.txt pyinstaller

pyinstaller --noconfirm --clean --onedir --windowed --name KNAVE ^
  --icon knave.ico ^
  --add-data "static;static" ^
  --collect-all yt_dlp ^
  --collect-all spotdl ^
  --collect-all uvicorn ^
  --collect-all pdf2docx ^
  --collect-all fitz ^
  --collect-all pystray ^
  --collect-all PIL ^
  --collect-all img2pdf ^
  desktop.py

echo.
echo  Listo: dist\KNAVE\KNAVE.exe
echo  Consejo: copia ffmpeg.exe dentro de dist\KNAVE\ para que
echo  la app no dependa del ffmpeg del sistema.
pause
