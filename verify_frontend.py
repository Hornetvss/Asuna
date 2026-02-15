import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        # Navigate to the frontend served by python http.server
        page.goto("http://localhost:8001/frontend/index.html")

        # Wait for the status text to update from "Checking..."
        # This confirms that the JS has successfully fetched from the backend.
        try:
            page.wait_for_function("document.getElementById('status-text').textContent.indexOf('Checking') === -1", timeout=10000)
        except Exception as e:
            print(f"Timeout waiting for status update: {e}")
            page.screenshot(path="verification_timeout.png")
            browser.close()
            return

        # Wait a bit to ensure the color/emotion is visible and potentially catch a state change
        time.sleep(2)

        # Take a screenshot
        page.screenshot(path="verification.png")
        print("Screenshot taken: verification.png")
        browser.close()

if __name__ == "__main__":
    run()
