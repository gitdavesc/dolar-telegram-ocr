import requests
import os
from datetime import datetime
from playwright.sync_api import sync_playwright

tc_clip = {"x": 346, "y": 501, "width": 474 - 346, "height": 1073 - 501}

GROUP_CHAT_ID = "-1001763327225"

def es_feriado_peru():
    try:
        año = datetime.now().year
        hoy = datetime.now().strftime("%Y-%m-%d")
        url = f"https://date.nager.at/api/v3/PublicHolidays/{año}/PE"
        feriados = requests.get(url, timeout=10).json()
        return any(f["date"] == hoy for f in feriados)
    except:
        return False

def ocr_image(path, apikey):
    with open(path, "rb") as f:
        r = requests.post(
            "https://api.ocr.space/parse/image",
            files={"file": f},
            data={"apikey": apikey, "language": "spa"}
        )
    return r.json()

def extraer_par(texto):
    nums = []
    for l in texto.split("\n"):
        l = l.strip().replace("A ", "").replace("v ", "").replace("u ", "")
        try:
            val = float(l)
            if 3.2 <= val <= 3.8:
                nums.append(val)
        except:
            pass
    return nums[:2] if len(nums) >= 2 else (None, None)

if es_feriado_peru():
    print("Feriado en Perú, no se ejecuta")
    exit()

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1366, "height": 2500})

    page.goto("https://cuantoestaeldolar.pe/")
    page.wait_for_timeout(15000)

    apikey = os.environ["OCR_API_KEY"]

    page.screenshot(path="tc.png", clip=tc_clip)

    data = ocr_image("tc.png", apikey)
    raw = data["ParsedResults"][0]["ParsedText"]

    compra, venta = extraer_par(raw)

    texto_ocr = f"Compra: {compra} | Venta: {venta}"

    token = os.environ.get("TELEGRAM_TOKEN", "")

    if token:
        requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data={
                "chat_id": GROUP_CHAT_ID,
                "text": texto_ocr
            }
        )

    print(texto_ocr)

    browser.close()
