# Informe diario de productos ganadores → Telegram

Este proyecto corre solo, todos los días, busca productos ganadores en TikTok
que no estén saturados en Colombia, te lo manda a Telegram y guarda una copia
con fecha en la carpeta `informes/`.

## Qué necesitas (una sola vez)

### 1. Cuenta de GitHub (gratis)
Crea una cuenta en https://github.com si no tienes, y crea un repositorio
nuevo (puede ser privado). Sube esta carpeta completa a ese repositorio.

### 2. API key de Anthropic
- Entra a https://console.anthropic.com
- Crea una API key (esto es distinto a tu suscripción de Claude.ai — se cobra
  por uso, pero para 1 informe diario el costo es muy bajo, unos pocos
  centavos de dólar al mes).

### 3. Bot de Telegram (gratis, 2 minutos)
1. Abre Telegram y busca **@BotFather**.
2. Envíale `/newbot`, ponle un nombre y un usuario (debe terminar en "bot").
3. BotFather te da un **token** — ese es tu `TELEGRAM_BOT_TOKEN`.
4. Abre una conversación con tu bot recién creado y mándale cualquier mensaje
   (ej. "hola").
5. Entra en tu navegador a:
   `https://api.telegram.org/bot<TU_TOKEN>/getUpdates`
   (reemplaza `<TU_TOKEN>` por el token real).
6. Busca en la respuesta el campo `"chat":{"id": ...}` — ese número es tu
   `TELEGRAM_CHAT_ID`.

### 4. Configurar los "Secrets" en GitHub
En tu repositorio: **Settings → Secrets and variables → Actions → New repository secret**.
Crea estos tres:
- `ANTHROPIC_API_KEY`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

### 5. Listo
El workflow (`.github/workflows/informe-diario.yml`) ya está programado para
correr todos los días a las 8:00 AM hora Colombia. También puedes ir a la
pestaña **Actions** de tu repo y darle "Run workflow" para probarlo ahora
mismo sin esperar a mañana.

## Dónde queda el historial
Cada informe se guarda como `informes/informe-YYYY-MM-DD.md` dentro del
repositorio, así que con el tiempo vas a tener un historial completo de qué
productos se detectaron cada día.

## Sobre FastMoss
El agente ahora prioriza contenido de FastMoss (plataforma de analítica de
TikTok Shop) dentro de sus búsquedas web — esto usa lo que FastMoss tiene
público/indexado, no su base de datos en vivo.

Si más adelante quieres datos en vivo directo de FastMoss (rankings exactos,
histórico de ventas), FastMoss tiene una API oficial (FastMoss OpenAPI), pero
requiere:
1. Crear cuenta en https://developers.fastmoss.com
2. Sacar tu `client_id` y `client_secret` desde su consola
3. Revisar la documentación de sus endpoints exactos (varía según tu plan/quota)

Con esos tres datos se puede escribir el cliente real que llama a su API
directamente en lugar de depender de búsqueda web.

## Ajustar la hora o los criterios
- Para cambiar la hora: edita la línea `cron` en el workflow (está en UTC).
- Para cambiar qué busca el agente o cómo decide: edita `agente_prompt.txt` —
  no necesitas tocar el script de Python.
