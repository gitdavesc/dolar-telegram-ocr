from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1366, "height": 2500})

    page.goto("https://cuantoestaeldolar.pe/")

    page.wait_for_timeout(15000)

page.screenshot(
    path="cambio_online.png",
    clip={
        "x": 0,
        "y": 180,
        "width": 1366,
        "height": 700
    }
)
    browser.close()
