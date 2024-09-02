import subprocess
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

# File paths
input_file = 'loom-videos.txt'
processed_file = 'loom-videos-processed.txt'

# Chrome paths
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
user_data_dir = os.path.expanduser('~') + r"\AppData\Local\Google\Chrome\User Data"

print(f"Chrome path: {chrome_path}")
print(f"User data directory: {user_data_dir}")

# Launch Chrome with remote debugging port
cmd = f'"{chrome_path}" --remote-debugging-port=9222 --user-data-dir="{user_data_dir}"'
print(f"Launching Chrome with command: {cmd}")
subprocess.Popen(cmd, shell=True)

print("Waiting for Chrome to launch...")
time.sleep(5)  # Give Chrome some time to start

print("Chrome has been launched. Please log in to Loom manually if needed.")
input("Press Enter when you're logged in and ready to proceed...")

# Set up Chrome options for Selenium
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# Initialize the WebDriver
print("Connecting to Chrome...")
driver = webdriver.Chrome(options=chrome_options)

print("Connected to Chrome. Verifying connection...")
try:
    print(f"Current URL: {driver.current_url}")
    print(f"Page title: {driver.title}")
except Exception as e:
    print(f"Error verifying connection: {str(e)}")
    exit(1)

try:
    # Navigate to Loom
    print("Navigating to Loom...")
    driver.get("https://www.loom.com")
    time.sleep(5)
    print(f"Current URL after navigation: {driver.current_url}")
    print(f"Page title after navigation: {driver.title}")

    # Now proceed with the Loom video processing
    video_ids = [line.strip() for line in open(input_file, 'r') if line.strip()]
    
    for video_id in video_ids:
        try:
            url = f"https://www.loom.com/share/{video_id}"
            print(f"\nOpening URL: {url}")
            driver.get(url)
            
            print("Waiting for page to load...")
            time.sleep(10)
            
            print("Current page title:", driver.title)
            
            print("Looking for 'More actions' button...")
            more_actions_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "toggleActions"))
            )
            print("'More actions' button found. Clicking...")
            driver.execute_script("arguments[0].scrollIntoView();", more_actions_button)
            more_actions_button.click()
            
            time.sleep(2)
            
            print("Looking for 'Download captions' option...")
            download_captions_option = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Download captions')]"))
            )
            print("'Download captions' option found. Clicking...")
            driver.execute_script("arguments[0].scrollIntoView();", download_captions_option)
            download_captions_option.click()
            
            print("Waiting for download to start...")
            time.sleep(5)
            
            print(f"Processed video: {video_id}")
            with open(processed_file, 'a') as f:
                f.write(f"{video_id}\n")
            with open(input_file, 'r') as f:
                lines = f.readlines()
            with open(input_file, 'w') as f:
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
    input("Press Enter to close the browser...")
    try:
        driver.quit()
    except WebDriverException:
        print("WebDriver was already closed.")
    except Exception as e:
        print(f"Error while closing the browser: {str(e)}")

print("Script completed. You can now close the Chrome window manually.")