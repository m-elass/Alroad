#!/bin/bash
# ============================================================
#  KNAVE en casa — modo compartido con código de acceso
#  Cambia el código de abajo por el tuyo antes de usarlo.
# ============================================================

export KNAVE_SERVER=1
export KNAVE_CODE=cambiame
export KNAVE_TTL_HOURS=720

if [ "$KNAVE_CODE" = "cambiame" ]; then
  echo
  echo "  [!] Edita casa.sh y cambia KNAVE_CODE por el código que"
  echo "      quieras compartir con tu gente."
  echo
  read -p "  Pulsa Enter para continuar de todas formas..."
fi

echo
echo "  KNAVE arrancando en modo compartido…"
echo "  Local:  http://127.0.0.1:8666"
echo
echo "  Para publicarlo en tu red Tailscale, en otra terminal:"
echo "     tailscale serve --bg 8666"
echo

python3 desktop.py
