from playwright.sync_api import sync_playwright
import os
import requests

tc_clips = [
    {"x": 346, "y": 501, "width": 474 - 346, "height": 1073 - 501},
    {"x": 756, "y": 499, "width": 884 - 756, "height": 1071 - 499},
    {"x": 1170, "y": 498, "width": 1298 - 1170, "height": 1070 - 498},
]

def ocr_image(path, apikey):
    with open(path, "rb") as f:
        r = requests.post(
            "https://api.ocr.space/parse/image",
            files={"file": f},
            data={"apikey": apikey, "language": "spa"}
        )
    return r.json()

def limpiar_tc(texto):
    for l in texto.split("\n"):
        l = l.strip().replace("A ", "").replace("v ", "").replace("u ", "")
        try:
            val = float(l)
            if 3.2 <= val <= 3.8:
                return val
        except:
            pass
    return None

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1366, "height": 2500})

    page.goto("https://cuantoestaeldolar.pe/")
    page.wait_for_timeout(15000)

    apikey = os.environ["OCR_API_KEY"]

    resultado = []

    for i, clip in enumerate(tc_clips):
        path = f"tc_{i}.png"
        page.screenshot(path=path, clip=clip)

        data = ocr_image(path, apikey)
        raw = data["ParsedResults"][0]["ParsedText"]

        compra = limpiar_tc(raw)
        venta = limpiar_tc(raw)  # mismo OCR, solo primer valor útil

        resultado.append({
            "compra": compra,
            "venta": venta
        })

    print(resultado)

    browser.close()
