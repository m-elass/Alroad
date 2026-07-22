# Desplegar KNAVE ✕ — móvil, iPad y ordenador

Esta guía cubre todas las vías para usar KNAVE fuera de tu PC, de la más
recomendable a la más avanzada. Antes, lo esencial:

- **Vercel no sirve.** Es una plataforma *serverless*: funciones que viven
  segundos, sin ffmpeg, sin LibreOffice, sin procesos largos ni disco. KNAVE
  necesita un servidor de verdad. **Render sí vale** (con Docker), y hay más
  opciones abajo.
- KNAVE ya incluye un **modo web multiusuario**: nadie ve lo de nadie.

---

## 1 · Cómo funciona el modo web (multiusuario)

Se activa con la variable de entorno `KNAVE_SERVER=1` (el Dockerfile ya la trae):

- Cada visitante recibe una **sesión anónima por cookie**. Su biblioteca, sus
  trabajos en curso y sus ajustes viven en una carpeta propia del servidor:
  **es imposible ver o borrar los archivos de otra persona** (los trabajos
  ajenos responden 404 y las rutas están selladas contra `../`).
- Los resultados se guardan en el servidor y se bajan con el botón
  **Descargar** (en iPhone/iPad van a la app Archivos).
- **Limpieza automática**: los archivos de cada sesión se borran pasadas
  `KNAVE_TTL_HOURS` horas (24 por defecto), para que el disco no se llene.
- Los botones «Abrir carpeta / Mostrar en carpeta» desaparecen solos: no tienen
  sentido en remoto.
- `KNAVE_PASSWORD=loquesea` pone un **candado global**: el navegador pedirá
  usuario (da igual cuál) y esa contraseña.
  **¿Prefieres acceso libre para tu gente?** No pongas la variable — o bórrala
  en Render → Environment → Save (redespliega solo). Sin login, y cada
  visitante sigue completamente aislado en su propia sesión.

| Variable | Efecto | Por defecto |
|---|---|---|
| `KNAVE_SERVER` | `1` = modo web multiusuario | apagado |
| `KNAVE_PASSWORD` | contraseña de acceso al sitio | sin candado |
| `KNAVE_TTL_HOURS` | horas de vida de los archivos | `24` |
| `KNAVE_MAX_MB` | tamaño máx. por archivo subido | `500` |
| `PORT` | puerto de escucha | `8666` |

---

## 2 · Opción A — Render (pública y gratis, la que conoces)

### Paso 1 — Sube el proyecto a GitHub

```bash
cd knave
git init
git add .
git commit -m "KNAVE"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/knave.git
git push -u origin main
```

(El `.gitignore` incluido ya deja fuera `dist/`, `build/` y demás morralla.)

### Paso 2 — Crea el servicio

1. Entra en [render.com](https://render.com) → **New +** → **Web Service**.
2. Conecta tu repositorio `knave`.
3. Render detecta el `Dockerfile` automáticamente (Language: **Docker**).
   No toques comandos de build/start.
4. **Instance Type: Free**.

### Paso 3 — Variables de entorno

En **Environment** añade:

- `KNAVE_PASSWORD` → tu contraseña (opcional: **omítela y la app queda
  abierta, sin pantalla de login**; el aislamiento por sesiones se mantiene).

`KNAVE_SERVER=1` ya viene en el Dockerfile. Opcional: en Settings →
Health Check Path pon `/healthz`.

### Paso 4 — Deploy

Pulsa **Create Web Service**. El primer build tarda **10–20 minutos**
(LibreOffice pesa). Al acabar tendrás tu URL:
`https://knave-xxxx.onrender.com` — ábrela desde cualquier dispositivo.

Para actualizar la app: `git push` y Render redespliega solo.

### Lo que debes saber del plan Free

- **Se duerme** tras ~15 min sin visitas; la primera carga después tarda
  ~1 minuto (está despertando, no está rota).
- **Disco efímero**: un redeploy o reinicio borra las bibliotecas. Por eso el
  TTL de 24 h y el aviso en la pestaña Biblioteca: descarga lo que quieras
  conservar.
- **512 MB de RAM**: documentos de oficina enormes pueden agotar la memoria al
  convertir a PDF. Si te pasa a menudo: plan Starter (~7 $/mes) o la opción C.
- CPU compartida: las conversiones van más lentas que en tu PC.

---

## 3 · Instálala como app (PWA) en cada dispositivo

KNAVE trae manifest e iconos: se «instala» desde el navegador y se abre a
pantalla completa con su icono ✕.

- **iPhone / iPad (Safari)**: abre tu URL → botón **Compartir** →
  **Añadir a pantalla de inicio**.
- **Android (Chrome)**: menú ⋮ → **Instalar aplicación**.
- **PC/Mac (Chrome/Edge)**: icono de instalar a la derecha de la barra de
  direcciones.

---

## 4 · Opción B — Privada con Tailscale (la mejor para ti y los tuyos)

Si el objetivo real es *tenerla tú* en el móvil, el iPad y el PC, esta vía es
superior: gratis, **nada queda expuesto a internet**, los archivos caen
directamente en tu PC y las descargas de YouTube funcionan mejor (ver avisos).

1. Instala [Tailscale](https://tailscale.com) en tu PC y en el móvil/iPad con
   la misma cuenta (es una VPN privada punto a punto).
2. En el PC arranca KNAVE como siempre (`desktop.py` o el .exe).
3. En una terminal del PC: `tailscale serve --bg 8666`
   → te da una URL `https://TU-PC.tu-red.ts.net` con HTTPS incluido.
4. Ábrela desde el móvil/iPad (con Tailscale activado) y añádela a la pantalla
   de inicio como en la sección 3.

¿Compartes la red Tailscale con familia y quieres aislamiento entre vosotros?
Arranca el servidor así: `KNAVE_SERVER=1 python main.py` (en Windows:
`set KNAVE_SERVER=1` y luego `python main.py`).

---

## 5 · Opción C — Hugging Face Spaces (pública, gratis, 16 GB de RAM)

Ideal si Render Free se te queda corto de memoria para LibreOffice.

1. [huggingface.co](https://huggingface.co) → **New Space** → SDK: **Docker**.
2. Sube todos los archivos del proyecto (o haz `git push` al repo del Space).
3. En el `README.md` **del Space**, dentro de la cabecera YAML, añade:
   `app_port: 8666`.
4. Settings → **Variables and secrets** → añade `KNAVE_PASSWORD` como *Secret*.

Pega: la URL es tipo `*.hf.space` y también tiene arranques fríos.

---

## 6 · Otras rutas con el mismo Dockerfile

- **Railway / Fly.io / Koyeb**: crea el servicio desde el repo; detectan el
  Dockerfile. Planes con crédito gratuito.
- **VPS propio** (Oracle Cloud *Always Free*, Hetzner ~4 €/mes): control total,
  IP fija y **persistencia real** con un volumen:

  ```bash
  docker build -t knave .
  docker run -d --restart unless-stopped -p 80:8666 \
    -e KNAVE_PASSWORD=tu_clave -e KNAVE_TTL_HOURS=168 \
    -v knave-data:/root/.knave knave
  ```

---

## 7 · Avisos importantes (léelos)

- **YouTube contra los datacenters**: YouTube exige a menudo verificación a las
  IPs de servidores en la nube («Sign in to confirm you're not a bot»), así que
  en Render/HF **algunas descargas de vídeo fallarán**; la tarjeta te mostrará
  el motivo. El **conversor de documentos funciona siempre**. KNAVE además
  reintenta cada descarga por **tres vías distintas** antes de rendirse, y en
  Ajustes puedes subir tus **cookies de YouTube** (extensión «Get cookies.txt
  LOCALLY»), que rescatan la mayoría de bloqueos — valen solo para tu sesión.
  Para descargas siempre fiables, la opción B (tu IP doméstica) es la buena. Spotify usa YouTube como
  fuente de audio, así que le afecta igual.
- **Legal y condiciones de uso**: un sitio público de descargas puede incumplir
  los términos de YouTube/Spotify y las normas del hosting, y compartir
  material con derechos no es uso personal. Ponle contraseña, compártela solo
  con tu círculo y descargad únicamente contenido sobre el que tengáis
  derechos.
- **HTTPS**: Render, Hugging Face y Tailscale te lo dan hecho; no publiques la
  app sin cifrar.
- **La versión de escritorio no cambia**: `build.bat` y el .exe siguen
  funcionando exactamente igual; el modo web es un traje más, no un reemplazo.
