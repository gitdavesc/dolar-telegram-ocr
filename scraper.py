from playwright.sync_api import sync_playwright
import os
import requests

n_clips = [
    {"x": 61, "y": 502, "width": 210 - 61, "height": 1071 - 502},   # n1
    {"x": 472, "y": 503, "width": 621 - 472, "height": 1072 - 503},  # n2
    {"x": 882, "y": 504, "width": 1031 - 882, "height": 1073 - 504}, # n3
]

tc_clips = [
    {"x": 346, "y": 501, "width": 474 - 346, "height": 1073 - 501},   # tc1
    {"x": 756, "y": 499, "width": 884 - 756, "height": 1071 - 499},   # tc2
    {"x": 1170, "y": 498, "width": 1298 - 1170, "height": 1070 - 498} # tc3
]

def ocr_image(path, apikey):
    with open(path, "rb") as f:
        r = requests.post(
            "https://api.ocr.space/parse/image",
            files={"file": f},
            data={"apikey": apikey, "language": "spa"}
        )
    return r.json()

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1366, "height": 2500})

    page.goto("https://cuantoestaeldolar.pe/")
    page.wait_for_timeout(15000)

    apikey = os.environ["OCR_API_KEY"]

    nombres = []
    tipos = []

    for i, clip in enumerate(n_clips):
        path = f"n_{i}.png"
        page.screenshot(path=path, clip=clip)
        data = ocr_image(path, apikey)
        nombres.append(data["ParsedResults"][0]["ParsedText"])

    for i, clip in enumerate(tc_clips):
        path = f"tc_{i}.png"
        page.screenshot(path=path, clip=clip)
        data = ocr_image(path, apikey)
        tipos.append(data["ParsedResults"][0]["ParsedText"])

    resultado = [
        {"n": nombres[i], "tc": tipos[i]}
        for i in range(3)
    ]

    print(resultado)

    browser.close()
