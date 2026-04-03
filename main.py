from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')

# FIX: Removed the Service('/usr/local/bin/chromedriver') to let Selenium Manager handle version 146
driver = webdriver.Chrome(options=options)

try:
    # --- LOGIN ---
    driver.get('https://t-propensity-rest-api.addapptation.com/login')
    wait = WebDriverWait(driver, 15)

    # Use .get() for env vars to avoid KeyError if they aren't set
    email = os.environ.get('SITE_EMAIL')
    password = os.environ.get('SITE_PASSWORD')

    wait.until(EC.presence_of_element_located((By.ID, 'email'))).send_keys(email)
    driver.find_element(By.ID, 'password').send_keys(password)
    
    # FIX: Added parentheses to .click()
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    time.sleep(5) # Give the dashboard time to load

    # --- NAVIGATE TO PAGE ---
    driver.get('https://t-propensity-rest-api.addapptation.com/test_page')
    
    # --- SUBMIT DATA ---
    message = os.environ.get('INPUT_MESSAGE', 'Hello from GitHub Actions!')
    
    # Wait for the specific input box to be interactable
    input_box = wait.until(EC.element_to_be_clickable((By.ID, 'user-input')))
    input_box.send_keys(message)
    
    driver.find_element(By.ID, 'submitBtn').click()
    time.sleep(5)

    # --- READ RESPONSE ---
    # Scrape the specific result
    response_window = driver.find_element(By.ID, 'chat-window')
    print(f"AI Response Output:\n{response_window.text}")

except Exception as e:
    print(f"Error encountered: {e}")
    # Optional: print(driver.page_source) 

finally:
    driver.quit()
