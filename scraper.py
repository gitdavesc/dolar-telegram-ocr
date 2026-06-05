from playwright.sync_api import sync_playwright
import os
import requests

clips = [
    {"x": 64, "y": 457, "width": 411, "height": 615},
    {"x": 482, "y": 460, "width": 411, "height": 615},
    {"x": 892, "y": 461, "width": 411, "height": 615},
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1366, "height": 2500})

    page.goto("https://cuantoestaeldolar.pe/")
    page.wait_for_timeout(15000)

    apikey = os.environ["OCR_API_KEY"]

    for i, clip in enumerate(clips):
        path = f"captura_{i}.png"
        page.screenshot(path=path, clip=clip)

        with open(path, "rb") as f:
            r = requests.post(
                "https://api.ocr.space/parse/image",
                files={"file": f},
                data={"apikey": apikey, "language": "spa"}
            )

        print(r.text)

    browser.close()
