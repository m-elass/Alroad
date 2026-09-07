# KNAVE desde tu casa ✕

Guía completa para que KNAVE se ejecute en **tu ordenador** y las descargas
salgan por **tu IP doméstica** (sin bloqueos de YouTube), pudiendo entrar desde
el móvil, el iPad o cualquier sitio.

---

## Cómo funciona (esto es lo importante)

KNAVE **no** se ejecuta en tu móvil. Se ejecuta en tu PC; el móvil solo enseña
la pantalla y da las órdenes:

```
  Tu iPad (en cualquier parte)
        │
        │  túnel cifrado (Tailscale)
        ▼
  Tu PC de casa  ──── pide el vídeo ────►  YouTube
        │                                  (ve tu IP doméstica ✓)
        │  el archivo vuelve por el túnel
        ▼
  Tu iPad: "Descargar"
```

YouTube nunca ve el móvil ni la red del sitio donde estés: solo ve a tu PC
pidiendo un vídeo desde una conexión doméstica normal. Por eso **no hay
bloqueos**.

**La condición**: el PC debe estar encendido y con KNAVE abierto. Es el precio
a cambio de que las descargas nunca fallen.

---

## PARTE 1 · Preparar el PC

### 1.1 · Python

Si ya usas PyCharm, lo tienes. Si no: [python.org](https://www.python.org/downloads/)
→ al instalar en Windows, **marca "Add Python to PATH"**.

### 1.2 · Las dependencias de KNAVE

Abre una terminal en la carpeta del proyecto y ejecuta:

```bash
pip install -r requirements.txt
```

(En PyCharm: crea el intérprete del proyecto y él te lo ofrece solo.)

### 1.3 · ffmpeg — imprescindible para audio y vídeo

Sin esto no hay MP3 ni fusión de vídeo con audio.

**Windows** (la vía fácil, con winget ya incluido en Windows 10/11):

```powershell
winget install Gyan.FFmpeg
```

Cierra y abre la terminal, y comprueba:

```powershell
ffmpeg -version
```

Si `winget` no te va: descarga de [gyan.dev/ffmpeg/builds](https://www.gyan.dev/ffmpeg/builds/)
(la versión *release essentials*), descomprime y **copia `ffmpeg.exe` a la
misma carpeta que `main.py`**. KNAVE lo busca ahí automáticamente.

**macOS**: `brew install ffmpeg`
**Linux**: `sudo apt install ffmpeg`

### 1.4 · LibreOffice — solo si quieres convertir documentos a PDF

Descárgalo de [es.libreoffice.org](https://es.libreoffice.org/). No hace falta
configurar nada, KNAVE lo encuentra solo. (Si solo vas a descargar vídeos,
puedes saltarte este paso.)

### 1.5 · Comprobación

Arranca KNAVE:

```bash
python desktop.py
```

Abre `http://127.0.0.1:8666` y entra en `http://127.0.0.1:8666/api/health`.
Deberías ver algo así:

```json
{"ok":true,"server":false,"ffmpeg":"C:\\...\\ffmpeg.exe","libreoffice":true,...}
```

Si `ffmpeg` sale `null`, vuelve al paso 1.3. **Prueba una descarga real ahora**,
antes de seguir: debe funcionar sin errores.

---

## PARTE 2 · Elegir el modo

Aquí hay una decisión real que cambia el comportamiento. Elige según quién vaya
a usarla:

### Modo A — Solo para ti (o gente de plena confianza)

No pongas ninguna variable. Arranca y listo.

- Los archivos se guardan **para siempre** en `Descargas/KNAVE`
- Funciona el botón «Mostrar en carpeta»
- **Todos ven la misma biblioteca** (si lo compartes, tus amigos ven tus
  archivos y pueden borrarlos)

### Modo B — Compartido con tu círculo (recomendado si lo van a usar otros)

Activa el modo servidor y el código de acceso:

- Cada persona tiene su **biblioteca privada** — nadie ve lo de nadie
- Se pide un **código** al entrar (pantalla propia de KNAVE con el ojo)
- Los archivos **caducan** pasado un tiempo y hay que descargarlos al
  dispositivo (puedes alargar ese plazo)
- Desaparece «Mostrar en carpeta» (no tiene sentido en remoto)

**En Windows**, crea un archivo `casa.bat` junto a `main.py` con esto:

```bat
@echo off
set KNAVE_SERVER=1
set KNAVE_CODE=elcodigoquetuquieras
set KNAVE_TTL_HOURS=720
python desktop.py
```

Cambia `elcodigoquetuquieras` por tu código real. `720` son 30 días de vida
para los archivos (por defecto serían 24 horas). A partir de ahora arrancas
KNAVE con doble clic en `casa.bat`.

**En macOS/Linux**, un `casa.sh`:

```bash
#!/bin/bash
export KNAVE_SERVER=1
export KNAVE_CODE=elcodigoquetuquieras
export KNAVE_TTL_HOURS=720
python3 desktop.py
```

(Dale permisos con `chmod +x casa.sh`.)

**Desde PyCharm**: Run → Edit Configurations → *Environment variables* → añade
`KNAVE_SERVER=1;KNAVE_CODE=tucodigo;KNAVE_TTL_HOURS=720`.

---

## PARTE 3 · Tailscale (el túnel)

### 3.1 · Instalar en el PC

1. Descarga de [tailscale.com/download](https://tailscale.com/download)
2. Instala y **entra con tu cuenta** (Google, Microsoft, GitHub… la que quieras)
3. En la bandeja del sistema verás el icono de Tailscale conectado

El plan Personal es gratis y permite 6 usuarios con dispositivos ilimitados.

### 3.2 · Activar los certificados HTTPS

Esto es obligatorio para que funcione el paso siguiente:

1. Entra en [login.tailscale.com/admin/dns](https://login.tailscale.com/admin/dns)
2. Busca **HTTPS Certificates** y pulsa **Enable**
3. Anota el nombre de tu red, del estilo `tu-red.ts.net`

### 3.3 · Publicar KNAVE en tu red privada

Con KNAVE ya arrancado, en otra terminal del PC:

```bash
tailscale serve --bg 8666
```

Te responderá con tu dirección, algo como:

```
https://tu-pc.tu-red.ts.net
```

Esa es la URL de tu KNAVE. `--bg` hace que siga activo aunque cierres la
terminal.

Para comprobar el estado o apagarlo:

```bash
tailscale serve status
tailscale serve --https=443 off
```

> En Windows, si `tailscale` no se reconoce como comando, usa la ruta completa:
> `"C:\Program Files\Tailscale\tailscale.exe" serve --bg 8666`

### 3.4 · Entrar desde el móvil y el iPad

1. Instala **Tailscale** desde la App Store / Play Store
2. Entra con **la misma cuenta**
3. Activa el interruptor (aparece un icono de VPN en la barra de estado)
4. Abre `https://tu-pc.tu-red.ts.net` en Safari o Chrome

### 3.5 · Instalarla como app

- **iPhone / iPad**: Safari → botón **Compartir** → **Añadir a pantalla de inicio**
- **Android**: Chrome → menú ⋮ → **Instalar aplicación**
- **PC/Mac**: icono de instalar en la barra de direcciones

Quedará con el icono del ojo de Arlecchino y se abrirá a pantalla completa.

---

## PARTE 4 · Compartirla con tu gente

### Opción 1 — Que instalen Tailscale (lo más privado)

Nada queda expuesto a internet. Dos formas:

**Invitarles a tu red** (comparten tu tailnet):
[login.tailscale.com/admin/users](https://login.tailscale.com/admin/users) →
**Invite users** → les llega un enlace.

**Compartir solo tu PC** (mejor opción: no ven el resto de tus dispositivos):
[login.tailscale.com/admin/machines](https://login.tailscale.com/admin/machines)
→ los tres puntos junto a tu PC → **Share** → copia el enlace y mándaselo.

Luego instalan Tailscale, aceptan, y abren tu URL. **No necesitan código**: ya
están dentro de la red.

### Opción 2 — Tailscale Funnel (sin que instalen nada)

Publica KNAVE en una dirección web pública. Ellos solo abren un enlace.

```bash
tailscale funnel --bg 8666
```

Para apagarlo: `tailscale funnel --https=443 off`

**Si usas Funnel, el código de acceso es obligatorio** (Modo B de la Parte 2):
al quedar accesible desde internet, cualquiera que dé con la dirección podría
usar tu PC para descargar.

---

## PARTE 5 · Que no se apague

Como KNAVE vive en tu PC, si el PC duerme la app deja de responder.

### 5.1 · Evitar la suspensión

**Windows**: Configuración → Sistema → Energía → *Suspensión* → «Nunca»
(al menos con el equipo enchufado). Puedes dejar que la pantalla se apague, eso
no afecta.

**macOS**: Ajustes → Batería → Adaptador de corriente → «Impedir que el Mac se
duerma automáticamente».

### 5.2 · Arranque automático

En la bandeja del sistema, clic derecho en el icono de KNAVE →
**«Iniciar con Windows»**. Así vuelve solo tras un reinicio.

> Ojo: el arranque automático usa la configuración normal, sin las variables
> del `casa.bat`. Si usas el Modo B, mejor pon un acceso directo a `casa.bat`
> en la carpeta de inicio: pulsa `Win+R`, escribe `shell:startup` y pega ahí
> el acceso directo.

`tailscale serve --bg` sobrevive a los reinicios por su cuenta.

---

## PARTE 6 · Comprobación final

Con el PC encendido y KNAVE en marcha, desde el **móvil con datos móviles**
(no wifi de casa, para probar de verdad que funciona desde fuera):

- [ ] Tailscale activado en el móvil
- [ ] `https://tu-pc.tu-red.ts.net` carga y se ve el ojo
- [ ] Si usas Modo B: pide el código y entra al escribirlo
- [ ] Pega un enlace de YouTube → aparece la vista previa con la miniatura
- [ ] Pulsa Descargar → progresa y termina en **COMPLETADO**
- [ ] Botón **Descargar** en la tarjeta → el archivo llega a tu móvil
- [ ] En Modo A, el archivo también está en `Descargas/KNAVE` del PC

Si los seis primeros pasan, ya lo tienes montado.

---

## PARTE 7 · Si algo falla

**«No se puede acceder al sitio» desde el móvil**
→ ¿Tailscale activado en el móvil? ¿El PC encendido y sin dormir?
→ En el PC: `tailscale status` (debe aparecer conectado) y `tailscale serve status`.

**La página carga pero sale error al descargar**
→ Mira `/api/health` en el navegador: si `ffmpeg` es `null`, repite el paso 1.3.

**«Este vídeo es privado / no está disponible»**
→ Es del vídeo, no de KNAVE. Prueba con otro enlace.

**Descargas que fallaban antes y ahora también**
→ Actualiza yt-dlp, que envejece rápido:
```bash
pip install -U yt-dlp
```
Reinicia KNAVE después. Hazlo cada pocas semanas.

**«El puerto ya está en uso»**
→ Ya tienes una instancia abierta. Mira la bandeja del sistema.

**Safari sigue pidiendo la contraseña vieja**
→ Ajustes → Safari → Borrar historial y datos, o usa una pestaña privada.

**Va muy lento al descargar en el móvil**
→ El archivo viaja de tu PC al móvil, así que depende de la **velocidad de
subida** de tu fibra. Para música y vídeos normales no se nota.

---

## PARTE 8 · Mantenimiento y cosas a tener en cuenta

**Cada pocas semanas**: `pip install -U yt-dlp` y reiniciar.

**El disco**: en Modo B los archivos se borran solos según `KNAVE_TTL_HOURS`.
En Modo A no se borra nada nunca: vacía `Descargas/KNAVE` de vez en cuando.

**Todo sale a tu nombre**: las descargas usan tu IP. Si alguien baja algo que
no debe, hacia fuera parece que lo hiciste tú. Comparte el código solo con
gente de confianza. No soy abogado, pero el riesgo lo asumes tú.

**Uso intensivo**: si se descarga mucho y muy seguido, YouTube puede empezar a
mostrarte captchas en tu casa durante un tiempo. Con un uso normal no pasa.

**Si usas cookies** (Ajustes ⚙): que sean de una cuenta de Google secundaria,
nunca la principal.

**Recursos**: el PC encendido, algo de CPU en las conversiones y subida de tu
conexión cuando alguien descarga.

---

## Resumen en cinco líneas

```bash
pip install -r requirements.txt      # una vez
winget install Gyan.FFmpeg           # una vez (Windows)
# instalar Tailscale + activar HTTPS Certificates en el panel web
casa.bat                             # arrancar KNAVE (Modo B)
tailscale serve --bg 8666            # publicar en tu red
```

Y desde el móvil: Tailscale activado → `https://tu-pc.tu-red.ts.net` →
Añadir a pantalla de inicio.
