@echo off
REM ============================================================
REM  KNAVE en casa - modo compartido con codigo de acceso
REM  Cambia el codigo de abajo por el tuyo antes de usarlo.
REM ============================================================

set KNAVE_SERVER=1
set KNAVE_CODE=cambiame
set KNAVE_TTL_HOURS=720

if "%KNAVE_CODE%"=="cambiame" (
  echo.
  echo  [!] Abre casa.bat con el Bloc de notas y cambia KNAVE_CODE
  echo      por el codigo que quieras compartir con tu gente.
  echo.
  pause
)

echo.
echo  KNAVE arrancando en modo compartido...
echo  Local:  http://127.0.0.1:8666
echo.
echo  Para publicarlo en tu red Tailscale, en otra terminal:
echo     tailscale serve --bg 8666
echo.

python desktop.py
pause
