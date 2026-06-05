from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1366, "height": 2500})

    page.goto("https://cuantoestaeldolar.pe/")

    page.wait_for_timeout(15000)

    page.screenshot(path="captura.png", full_page=True)

    browser.close()

import os

print(os.listdir("."))
    
import requests

with open("captura.png", "rb") as f:
    r = requests.post(
        "https://api.ocr.space/parse/image",
        files={"filename": f},
        data={
            "apikey": "K85573583588957",
            "language": "spa"
        }
    )

print(r.text)
