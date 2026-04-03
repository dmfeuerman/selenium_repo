from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')

service = Service('/usr/local/bin/chromedriver')
driver = webdriver.Chrome(service=service, options=options)

try:
    # --- LOGIN ---
    driver.get('https://t-propensity-rest-api.addapptation.com/login')
    wait = WebDriverWait(driver, 10)

    wait.until(EC.presence_of_element_located((By.ID, 'email'))).send_keys(os.environ['SITE_EMAIL'])
    driver.find_element(By.ID, 'password').send_keys(os.environ['SITE_PASSWORD'])
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click
    time.sleep(3)

    # --- NAVIGATE TO PAGE ---
    driver.get('https://t-propensity-rest-api.addapptation.com/test_page')
    time.sleep(2)

    # --- SUBMIT DATA ---
    message = os.environ.get('INPUT_MESSAGE', 'Hello!')
    wait.until(EC.presence_of_element_located((By.ID, 'user-input'))).send_keys(message)
    driver.find_element(By.ID, 'submitBtn').click()
    time.sleep(3)

    # --- READ RESPONSE ---
    print(driver.find_element(By.ID, 'chat-window').text)

except Exception as e:
    print(f"Error: {e}")
    print(driver.page_source)  # helps debug

finally:
    driver.quit()
