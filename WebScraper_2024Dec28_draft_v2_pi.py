# Peter Idoko
# 2024-12-28
# Program that scrapes a webpage

import os  # So program can create folders
import time  # So three more seconds can be added when webpages load
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration
BASE_URL = "https://prciec-rpccie.parl.gc.ca/EN/PublicRegistries/Pages/PublicRegistryCode.aspx"
OUTPUT_FOLDER = "test_parliament_members_html"
CHROMEDRIVER_PATH = r"C:\Users\Administrator\Downloads\CommonInvestor\chromedriver-win64\chromedriver.exe"  # Ensure correct path
WAIT_TIME = 15  # Increased wait time for slower pages. 

# Setup Selenium WebDriver
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service)
driver.maximize_window()

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Step 1: Navigate to the main page
print("Accessing the main page...")
driver.get(BASE_URL)

try:
    WebDriverWait(driver, WAIT_TIME).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a"))
    )
    print("Main page loaded successfully.")
except Exception as e:
    print("Error loading the main page:", e)
    driver.quit()
    exit()

# Step 2: Extract all member links across pages
print("Extracting member links across all pages...")
member_links = []

while True:  # Loop to navigate through all pages
    try:
        # Wait for the current page to load
        WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a"))
        )

        # Extract links for the current page
        links = driver.find_elements(By.CSS_SELECTOR, "a")
        for link in links:
            href = link.get_attribute("href")
            if href and "Client.aspx#k=" in href:  # Keep the fragment identifier
                if href not in member_links:  # Avoid duplicates
                    member_links.append(href)

        # Check for and click the "Next" button
        next_button = driver.find_element(By.CSS_SELECTOR, "a[title='Move to next page']")  # Adjust selector as needed
        if next_button:
            print("Navigating to the next page...")
            next_button.click()
            time.sleep(3)  # Allow time for the next page to load
        else:
            print("No more pages to navigate.")
            break  # Exit the loop if "Next" button is not found
    except Exception as e:
        print("Error navigating pages:", e)
        break

print(f"Total member links extracted: {len(member_links)}")

# Step 3: Visit Each Link and Save Page as HTML
for idx, member_link in enumerate(member_links, start=1):
    print(f"Processing member {idx}/{len(member_links)}: {member_link}")
    try:
        driver.get(member_link)  # Visit the link with the fragment identifier

        # Wait for the page to fully load
        WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(3)  # Allow additional time for dynamic content

        # Save the rendered page as an HTML file
        html_path = os.path.join(OUTPUT_FOLDER, f"member_{idx}.html")
        with open(html_path, "w", encoding="utf-8") as file:
            file.write(driver.page_source)
        print(f"Saved HTML: {html_path}")

    except Exception as e:
        print(f"Error processing member {idx}: {e}")
        continue

# Cleanup
print("Scraping completed.")
driver.quit()
