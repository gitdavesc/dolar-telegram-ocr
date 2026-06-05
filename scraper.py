from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://cuantoestaeldolar.pe/")
    page.screenshot(path="captura.png", full_page=True)
    browser.close()

print("captura creada")
