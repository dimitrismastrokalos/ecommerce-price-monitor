import asyncio
import csv
from datetime import datetime
from playwright.async_api import async_playwright

async def check_price(url):
    print(f"🔍 Checking product page: {url}")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        try:
            await page.goto(url, timeout=15000, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)
            
            title = await page.title()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            result = {
                "Timestamp": now,
                "Product Title": title.strip(),
                "URL": url
            }
            
            print(f"✅ Extracted: {title.strip()}")
            
            with open("price_log.csv", mode="a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=result.keys())
                if f.tell() == 0:
                    writer.writeheader()
                writer.writerows([result])
                
            print("💾 Saved check to 'price_log.csv'")

        except Exception as e:
            print(f"❌ Error scraping URL: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    test_url = "https://www.amazon.com/dp/B08N5WRWNW"
    asyncio.run(check_price(test_url))