from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 1. Setup Headless Options
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# 2. Initialize Driver - DON'T pass a service path
# Selenium will now automatically find the driver for Chrome 146
try:
    driver = webdriver.Chrome(options=options)
    driver.get("https://google.com")
    print(f"Connected to: {driver.title}")
finally:
    if 'driver' in locals():
        driver.quit()
