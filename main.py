from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from collections import Counter
import re
import csv
import time

# Toggle this if you want to SEE the browser
HEADLESS = True


def create_driver():
    options = Options()

    if HEADLESS:
        options.add_argument("--headless=new")

    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    try:
        # If webdriver-manager is installed, this works automatically
        from webdriver_manager.chrome import ChromeDriverManager
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    except Exception:
        # Fallback: assumes chromedriver is already in PATH
        driver = webdriver.Chrome(options=options)

    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    return driver


def scrape_duckduckgo_selenium(keyword):
    driver = create_driver()
    wait = WebDriverWait(driver, 10)

    try:
        search_url = f"https://duckduckgo.com/?q={keyword.replace(' ', '+')}"
        print(f"\n🌐 Navigating to: {search_url}")

        driver.get(search_url)

        # Wait for results container instead of sleeping
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))

        selectors = [
            "a[data-testid='result-title-a']",
            ".result__a",
            "h2 a",
        ]

        titles_elements = []
        used_selector = None

        for selector in selectors:
            try:
                titles_elements = wait.until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
                )
                if titles_elements:
                    used_selector = selector
                    print(f"✓ Using selector: {selector}")
                    break
            except TimeoutException:
                continue

        if not titles_elements:
            print("❌ No titles found.")

            with open("debug_page.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)

            driver.save_screenshot("debug_screenshot.png")

            print("📄 Saved debug_page.html")
            print("📸 Saved debug_screenshot.png")

            return None

        titles = []

        for elem in titles_elements[:10]:
            try:
                text = elem.text.strip()
                if len(text) > 5:
                    titles.append(text)
            except Exception:
                continue

        if not titles:
            print("❌ Titles detected but extraction failed.")
            return None

        print(f"✓ Extracted {len(titles)} titles\n")
        return titles

    except Exception as e:
        print(f"❌ Scraping error: {e}")
        return None

    finally:
        driver.quit()


def analyze_and_display(titles):
    if not titles:
        return

    print("=" * 60)
    print("TOP SERP TITLES")
    print("=" * 60)

    all_words = []

    for i, title in enumerate(titles, 1):
        words = re.findall(r"\b\w+\b", title)
        word_count = len(words)
        char_length = len(title)

        print(f"\n{i}. {title}")
        print(f"   Length: {char_length} chars | Words: {word_count}")

        all_words.extend([w.lower() for w in words])

    common_words = Counter(all_words).most_common(10)

    print("\n" + "=" * 60)
    print("MOST COMMON WORDS")
    print("=" * 60)

    for word, count in common_words:
        print(f"{word:<12} : {count}")

    print("=" * 60)


def export_to_csv(titles, filename="serp_titles.csv"):
    if not titles:
        print("❌ No data to export.")
        return

    try:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Rank", "Title", "Length", "Word Count"])

            for i, title in enumerate(titles, 1):
                word_count = len(re.findall(r"\b\w+\b", title))
                writer.writerow([i, title, len(title), word_count])

        print(f"\n✓ Exported to {filename}")

    except Exception as e:
        print(f"❌ CSV export error: {e}")


def main():
    print("🚀 SERP Scraper Started")

    keyword = input("\nEnter keyword: ").strip()

    if not keyword:
        print("❌ Keyword cannot be empty.")
        return

    print(f"\n🔍 Searching DuckDuckGo for: '{keyword}'")

    titles = scrape_duckduckgo_selenium(keyword)

    if titles:
        analyze_and_display(titles)
        export_to_csv(titles)
    else:
        print("\n❌ Failed to retrieve results.")
        print("Check debug_page.html / debug_screenshot.png")


if __name__ == "__main__":
    main()