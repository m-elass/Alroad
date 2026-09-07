# KNAVE ✕

Descargas y conversiones de archivos, con estética propia. Corre entero en tu
equipo: nada sale de tu ordenador salvo lo que tú descargas.

## Qué hace

**Descargar** — pega hasta 20 enlaces (uno por línea) de YouTube, Spotify y
cientos de sitios más:
- Vista previa automática del enlace (título, autor, duración, nº de pistas).
- Vídeo MP4 (480p–máxima) o audio en **MP3 · M4A · FLAC · OPUS · WAV**.
- Listas de reproducción completas con numeración de pistas.
- Carátula y metadatos incrustados; subtítulos es/en opcionales.
- Spotify: metadatos de Spotify + audio de su equivalente en YouTube.

**Convertir** — suelta archivos y las operaciones válidas se encienden solas:
| Operación | Entrada |
|---|---|
| A PDF | docx, pptx, xlsx, odt, rtf, txt… (requiere LibreOffice) |
| A Word / A PowerPoint / A imágenes | |
| Separar páginas / Comprimir | un PDF |
| Unir en PDF | hasta 200 imágenes |
| Combinar PDFs | 2–200 PDFs |

**Biblioteca** — todo se guarda en `Descargas/KNAVE` (configurable). Desde la
pestaña puedes abrir la carpeta, mostrar un archivo, descargar una copia o
eliminarlo.

Además: **puerta de acceso con código** para compartirla solo con quien
quieras, cancelación de trabajos en caliente, notificaciones nativas al
terminar, icono en la bandeja con «Iniciar con Windows» y ajustes persistentes.

## Llevarla al móvil, iPad y web

**¿Quieres que las descargas nunca fallen?** Sigue **GUIA_CASA.md**: KNAVE se
ejecuta en tu PC y entras desde el móvil con Tailscale, así YouTube ve tu IP
doméstica y no hay bloqueos. Incluye los lanzadores `casa.bat` / `casa.sh`.

Guía completa en **DESPLIEGUE.md**: Render con Docker, contraseña de acceso,
modo multiusuario con sesiones aisladas, opción privada con Tailscale e
instalación como app en iPhone/iPad/PC.

## Ejecutar desde PyCharm

1. Abre la carpeta como proyecto y crea un intérprete (venv).
2. `pip install -r requirements.txt`
3. Instala [ffmpeg](https://www.gyan.dev/ffmpeg/builds/) (o copia `ffmpeg.exe`
   junto a `main.py`) y [LibreOffice](https://es.libreoffice.org/) si quieres
   convertir documentos a PDF.
4. Ejecuta `desktop.py` (bandeja + navegador) o `main.py` (solo servidor) y
   entra en `http://127.0.0.1:8666`.

## Crear el .exe

Doble clic en **`build.bat`** (Windows) o `./build.sh` (Linux/macOS). El
resultado queda en `dist/KNAVE/KNAVE.exe`; copia `ffmpeg.exe` a esa misma
carpeta y ya puedes moverla o compartirla entera.

- Windows SmartScreen avisará porque el exe no está firmado: «Más información →
  Ejecutar de todas formas».
- La app usa una sola instancia: si ya está abierta, un segundo clic solo abre
  la pestaña.

## Si algo falla

- La app siempre explica el motivo en la propia tarjeta del trabajo.
- «LibreOffice no está instalado» → instálalo y reintenta.
- Sin ffmpeg no hay conversión de audio ni fusión de vídeo: compruébalo en
  `http://127.0.0.1:8666/api/health`.
- yt-dlp envejece rápido: si YouTube cambia algo, `pip install -U yt-dlp` y
  reconstruye.

Uso personal. Descarga solo contenido sobre el que tengas derechos; respeta
los términos de cada plataforma.
