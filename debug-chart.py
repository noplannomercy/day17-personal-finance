from playwright.sync_api import sync_playwright
import time

def debug_chart():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Capture console messages
        console_messages = []
        page.on("console", lambda msg: console_messages.append(f"{msg.type}: {msg.text}"))
        
        print("Navigating to app...")
        page.goto('http://localhost:3005')
        page.wait_for_load_state('networkidle')
        time.sleep(3)
        
        # Check for errors
        print("\n--- Console Messages ---")
        for msg in console_messages:
            if 'error' in msg.lower() or 'warn' in msg.lower():
                print(msg)
        
        # Check monthly trend chart area
        print("\n--- Checking Monthly Trend Chart ---")
        trend_card = page.locator('text=월별 추이').first
        if trend_card.count() > 0:
            print("Found 월별 추이 card")
            # Get the parent card content
            card_content = trend_card.locator('xpath=ancestor::div[contains(@class,"card")]')
            html = card_content.inner_html()
            print(f"Card HTML length: {len(html)}")
            print(f"Contains svg: {'svg' in html.lower()}")
            print(f"Contains recharts: {'recharts' in html.lower()}")
            print(f"Contains 데이터 없음: {'데이터 없음' in html}")
            print(f"Contains animate-pulse: {'animate-pulse' in html}")
        
        # Take a screenshot
        page.screenshot(path='test-screenshots/debug-chart.png', full_page=True)
        print("\nScreenshot saved: test-screenshots/debug-chart.png")
        
        browser.close()

if __name__ == "__main__":
    debug_chart()
