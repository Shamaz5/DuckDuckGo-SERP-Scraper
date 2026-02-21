# DuckDuckGo-SERP-Scraper
A lightweight Python script using Selenium to scrape, analyze, and export DuckDuckGo search result titles to CSV.
# DuckDuckGo SERP Scraper

A lightweight, automated Python script that scrapes Search Engine Results Page (SERP) titles from DuckDuckGo using Selenium. It extracts the top search results for a given keyword, performs a basic text analysis, and exports the data to a CSV file.

## Features

* **Automated Browsing:** Uses Selenium WebDriver to navigate DuckDuckGo.
* **Headless Execution:** Runs in the background without opening a visible browser window (can be toggled in `main.py`).
* **Anti-Bot Mitigation:** Includes custom headers, user-agents, and automation-flag removal to bypass basic bot detection.
* **Text Analysis:** Calculates character count and word count for each title, and displays the top 10 most common words across all results.
* **CSV Export:** Automatically saves the scraped rankings, titles, and lengths into `serp_titles.csv`.
* **Smart Debugging:** Automatically saves a screenshot (`debug_screenshot.png`) and the page source (`debug_page.html`) if no titles are found, helping you easily troubleshoot selector changes.

## Prerequisites

* Python 3.7 or higher
* Google Chrome browser installed on your machine

## Installation

1. **Clone or download the repository:**
   Ensure `main.py` is in your working directory.

2. **Install the required dependencies:**
   Run the following command in your terminal to install Selenium and Webdriver Manager:
   ```bash
   pip install -r requirements.txt
