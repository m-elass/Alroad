#!/usr/bin/env bash
cd "$(dirname "$0")"
python3 -m venv .venv 2>/dev/null; source .venv/bin/activate
pip install -q -r requirements.txt pyinstaller
pyinstaller --noconfirm --clean --onedir --windowed --name KNAVE \
  --add-data "static:static" \
  --collect-all yt_dlp --collect-all spotdl --collect-all uvicorn \
  --collect-all pdf2docx --collect-all fitz --collect-all pystray --collect-all PIL --collect-all img2pdf \
  desktop.py
echo "Listo: dist/KNAVE/KNAVE"
