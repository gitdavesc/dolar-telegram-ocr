from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1366, "height": 2500})

    page.goto("https://cuantoestaeldolar.pe/")

    page.wait_for_timeout(15000)

    page.screenshot(
        path="captura.png",
        clip={
		    "x": 80,
		    "y": 380,
		    "width": 1366,
		    "height": 600
        }
    )
    browser.close()

import os
import requests

print(os.listdir("."))

    
apikey = os.environ["OCR_API_KEY"]

with open("captura.png", "rb") as f:
    r = requests.post(
        "https://api.ocr.space/parse/image",
        files={"filename": f},
        data={
            "apikey": apikey,
            "language": "spa"
        }
    )

print(r.text)
