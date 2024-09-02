from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
import os
import tempfile

# File paths
input_file = "loom-videos.txt"
processed_file = "loom-videos-processed.txt"

# Create a temporary directory for the Chrome user data
temp_dir = tempfile.mkdtemp()
print(f"Using temporary directory for Chrome profile: {temp_dir}")

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument(f"user-data-dir={temp_dir}")
chrome_options.add_argument("--no-first-run")
chrome_options.add_argument("--no-default-browser-check")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

# Set up ChromeDriver service
service = Service()

# Initialize the WebDriver
driver = None

try:
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(30)

    # Navigate to Loom login page
    print("Navigating to Loom login page...")
    driver.get("https://www.loom.com/login")
    time.sleep(5)

    print("Please log in to your Loom account manually in the opened browser.")
    input("Press Enter when you have successfully logged in...")

    # Now proceed with the Loom video processing
    video_ids = [line.strip() for line in open(input_file, "r") if line.strip()]

    for video_id in video_ids:
        try:
            url = f"https://www.loom.com/share/{video_id}"
            print(f"\nOpening URL: {url}")
            driver.get(url)

            print("Waiting for page to load...")
            time.sleep(5)

            print("Current page title:", driver.title)

            print("Looking for 'More actions' button...")
            more_actions_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "toggleActions"))
            )
            print("'More actions' button found. Clicking...")
            driver.execute_script("arguments[0].scrollIntoView();", more_actions_button)
            more_actions_button.click()

            print("Looking for 'Download captions' option...")
            download_captions_option = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "downshift-0-item-4"))
            )
            print("'Download captions' option found. Clicking...")
            # driver.execute_script(
            #     "arguments[0].scrollIntoView();", download_captions_option
            # )
            download_captions_option.click()

            print("Waiting for download to start...")
            time.sleep(5)

            print(f"Processed video: {video_id}")
            with open(processed_file, "a") as f:
                f.write(f"{video_id}\n")
            with open(input_file, "r") as f:
                lines = f.readlines()
            with open(input_file, "w") as f:
                f.writelines(line for line in lines if line.strip() != video_id)

        except TimeoutException:
            print(f"Timeout occurred while processing video {video_id}")
        except Exception as e:
            print(f"Error processing video {video_id}: {str(e)}")

        print("Waiting before next video...")
        time.sleep(5)

except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    if driver:
        input("Press Enter to close the browser...")
        try:
            driver.quit()
        except WebDriverException:
            print("WebDriver was already closed.")
        except Exception as e:
            print(f"Error while closing the browser: {str(e)}")

    # Clean up the temporary directory
    import shutil

    shutil.rmtree(temp_dir, ignore_errors=True)
    print(f"Removed temporary Chrome profile directory: {temp_dir}")
