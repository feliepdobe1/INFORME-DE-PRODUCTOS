"""
Informe diario de productos ganadores.
Llama a la API de Claude (con búsqueda web activada) usando el prompt del agente,
envía el resultado a un chat de Telegram y guarda una copia con fecha en /informes.

Variables de entorno necesarias (se configuran como Secrets en GitHub Actions):
- ANTHROPIC_API_KEY   -> API key de https://console.anthropic.com
- TELEGRAM_BOT_TOKEN  -> token que te da @BotFather en Telegram
- TELEGRAM_CHAT_ID    -> tu chat_id (instrucciones más abajo en el README)
"""

import os
import sys
import datetime
import requests

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"].strip()
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"].strip()
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"].strip()

MODEL = "claude-sonnet-5"
MAX_TELEGRAM_LEN = 4000  # Telegram corta mensajes muy largos, dejamos margen


def cargar_prompt_agente() -> str:
    ruta = os.path.join(os.path.dirname(__file__), "agente_prompt.txt")
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()


def generar_informe() -> str:
    hoy = datetime.date.today().strftime("%Y-%m-%d")
    system_prompt = cargar_prompt_agente()

    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": MODEL,
            "max_tokens": 2000,
            "system": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": f"Genera el informe diario de productos ganadores. Fecha de hoy: {hoy}.",
                }
            ],
            "tools": [{"type": "web_search_20250305", "name": "web_search"}],
        },
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()

    partes_texto = [
        bloque["text"] for bloque in data.get("content", []) if bloque.get("type") == "text"
    ]
    texto = "\n".join(partes_texto).strip()

    if not texto:
        texto = "⚠️ El agente no devolvió texto. Revisa la respuesta cruda en los logs de la Action."

    return f"🎯 Informe de productos ganadores — {hoy}\n\n{texto}"


def enviar_a_telegram(texto: str) -> None:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    # Telegram tiene un límite de caracteres por mensaje; partimos si hace falta
    for i in range(0, len(texto), MAX_TELEGRAM_LEN):
        trozo = texto[i : i + MAX_TELEGRAM_LEN]
        r = requests.post(
            url,
            json={"chat_id": TELEGRAM_CHAT_ID, "text": trozo},
            timeout=30,
        )
        if not r.ok:
            print(f"Error enviando a Telegram: {r.status_code} {r.text}", file=sys.stderr)
            r.raise_for_status()


def guardar_historial(texto: str) -> None:
    hoy = datetime.date.today().strftime("%Y-%m-%d")
    carpeta = os.path.join(os.path.dirname(__file__), "informes")
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, f"informe-{hoy}.md")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(texto)
    print(f"Informe guardado en {ruta}")


def main() -> None:
    informe = generar_informe()
    print(informe)
    guardar_historial(informe)
    enviar_a_telegram(informe)


if __name__ == "__main__":
    main()
