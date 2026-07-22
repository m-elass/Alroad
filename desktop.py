"""
KNAVE — lanzador de escritorio.

Ejecuta el servidor en segundo plano y vive en la bandeja del sistema:
  · doble clic / "Abrir KNAVE"  → abre la interfaz en el navegador
  · "Iniciar con Windows"       → alterna el autoarranque (registro de Windows)
  · "Salir"                     → apaga el servidor

Uso:  python desktop.py            (abre el navegador al arrancar)
      python desktop.py --hidden   (arranca en silencio; lo usa el autoarranque)

Si no hay entorno gráfico para la bandeja, sigue funcionando como
servidor normal en http://127.0.0.1:8666.
"""

from __future__ import annotations

import socket
import sys
import threading
import time
import webbrowser
from pathlib import Path

HOST, PORT = "127.0.0.1", 8666
URL = f"http://{HOST}:{PORT}"
APP_NAME = "KNAVE"
HIDDEN = "--hidden" in sys.argv


# ----------------------------------------------------------------------------
# Instancia única: si ya hay una KNAVE viva, solo abre el navegador y termina
# ----------------------------------------------------------------------------
def _port_in_use() -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((HOST, PORT)) == 0


if _port_in_use():
    if not HIDDEN:
        webbrowser.open(URL)
    sys.exit(0)


# ----------------------------------------------------------------------------
# Servidor en un hilo demonio
# ----------------------------------------------------------------------------
def _run_server() -> None:
    import uvicorn

    from main import app  # importa la app FastAPI del backend

    uvicorn.run(app, host=HOST, port=PORT, log_level="warning")


threading.Thread(target=_run_server, daemon=True).start()

# espera activa a que el servidor responda (máx. 20 s)
for _ in range(200):
    if _port_in_use():
        break
    time.sleep(0.1)

if not HIDDEN:
    webbrowser.open(URL)


# ----------------------------------------------------------------------------
# Autoarranque con Windows (registro HKCU\...\Run)
# ----------------------------------------------------------------------------
_RUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"


def _launch_command() -> str:
    if getattr(sys, "frozen", False):                       # app empaquetada (.exe)
        return f'"{sys.executable}" --hidden'
    script = Path(__file__).resolve()
    pythonw = Path(sys.executable).with_name("pythonw.exe") # sin consola si existe
    py = pythonw if pythonw.exists() else Path(sys.executable)
    return f'"{py}" "{script}" --hidden'


def autostart_enabled() -> bool:
    if sys.platform != "win32":
        return False
    import winreg
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, _RUN_KEY) as key:
            winreg.QueryValueEx(key, APP_NAME)
        return True
    except OSError:
        return False


def toggle_autostart(icon=None, item=None) -> None:
    if sys.platform != "win32":
        return
    import winreg
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, _RUN_KEY, 0,
                        winreg.KEY_SET_VALUE) as key:
        if autostart_enabled():
            try:
                winreg.DeleteValue(key, APP_NAME)
            except OSError:
                pass
        else:
            winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, _launch_command())


# ----------------------------------------------------------------------------
# Icono de bandeja: el sigilo ✕ dibujado con PIL (sin archivos externos)
# ----------------------------------------------------------------------------
def _sigil_image(size: int = 64):
    from PIL import Image, ImageDraw
    from pathlib import Path as _P

    icon = _P(__file__).parent / "static" / "icon-512.png"
    try:
        return Image.open(icon).convert("RGBA").resize((size, size))
    except Exception:  # noqa: BLE001 — sin icono empaquetado → dibujo de respaldo
        pass

    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    s, c, w = size, size / 2, size * 0.16          # lado, centro, medio grosor
    m = size * 0.06                                 # margen
    blood, ember, ash = (224, 23, 61, 255), (255, 116, 51, 255), (239, 233, 227, 255)
    # cuatro hojas afiladas que forman la ✕
    d.polygon([(m + w, m), (c, c - w), (c, c), (c - w, c), (m, m + w)], fill=ember)
    d.polygon([(s - m - w, m), (s - m, m + w), (c + w, c), (c, c), (c, c - w)], fill=blood)
    d.polygon([(m, s - m - w), (m + w, s - m), (c, c + w), (c, c), (c - w, c)], fill=blood)
    d.polygon([(s - m, s - m - w), (s - m - w, s - m), (c, c + w), (c, c), (c + w, c)], fill=ember)
    # pupila de diamante
    p = size * 0.12
    d.polygon([(c, c - p), (c + p, c), (c, c + p), (c - p, c)], fill=ash)
    p2 = size * 0.06
    d.polygon([(c, c - p2), (c + p2, c), (c, c + p2), (c - p2, c)], fill=blood)
    return img


# ----------------------------------------------------------------------------
# Bandeja del sistema (con retirada elegante si no hay entorno gráfico)
# ----------------------------------------------------------------------------
def _notifier(icon) -> None:
    """Convierte los avisos del backend en notificaciones nativas del sistema."""
    from main import pop_notifications
    while True:
        time.sleep(2)
        for n in pop_notifications():
            try:
                icon.notify(n["message"], n["title"])
            except Exception:  # noqa: BLE001 — un aviso fallido no tumba la bandeja
                pass


def _open_output(icon=None, item=None) -> None:
    from main import _open_in_manager, output_dir
    _open_in_manager(output_dir(), select=False)


def _tray() -> None:
    import pystray

    menu = pystray.Menu(
        pystray.MenuItem("Abrir KNAVE", lambda i, _: webbrowser.open(URL),
                         default=True),
        pystray.MenuItem("Abrir carpeta de salida", _open_output),
        pystray.MenuItem("Iniciar con Windows", toggle_autostart,
                         checked=lambda item: autostart_enabled(),
                         visible=sys.platform == "win32"),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Salir", lambda icon, _: icon.stop()),
    )
    icon = pystray.Icon(APP_NAME, _sigil_image(), f"{APP_NAME} · {URL}", menu)

    def _setup(ic) -> None:
        ic.visible = True
        threading.Thread(target=_notifier, args=(ic,), daemon=True).start()

    icon.run(setup=_setup)


if __name__ == "__main__":
    try:
        _tray()                       # bloquea hasta "Salir"
    except Exception as exc:          # noqa: BLE001 — sin bandeja, modo servidor
        print(f"[{APP_NAME}] Bandeja no disponible ({exc.__class__.__name__}). "
              f"Servidor activo en {URL} — Ctrl+C para salir.")
        try:
            while True:
                time.sleep(3600)
        except KeyboardInterrupt:
            pass
