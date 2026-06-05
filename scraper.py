from playwright.sync_api import sync_playwright
import os
import requests

tc_clip = {"x": 346, "y": 501, "width": 474 - 346, "height": 1073 - 501}

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

    resultado = {
        "compra": compra,
        "venta": venta
    }

    print(resultado)

    browser.close()
