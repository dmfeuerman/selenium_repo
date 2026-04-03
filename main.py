import os
import json
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURATION ---
DATA_TABLE = {
    "campaign": {
        "link": "https://dashboard.propensity.com/experiences",
        "container_id": "campaigns-table_wrapper",
        "toggle_css": ".cohort-toggle"
    },
    "audience": {
        "link": "https://dashboard.propensity.com/audiences",
        "container_id": "audiences-table_wrapper",
        "toggle_css": ".cohort-toggle"
    }
}

# --- HTML CLEANING LOGIC ---
def clean_html_keep_all_data(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    
    # 1. Remove non-content tags
    for tag in soup(['script', 'style', 'svg', 'path', 'button', 'noscript', 'canvas']):
        tag.decompose()
    
    # 2. Strip attributes except 'href' and 'data-id'
    for tag in soup.find_all(True):
        attrs = dict(tag.attrs)
        for attr in attrs:
            if attr not in ['href', 'data-id']:
                del tag[attr]
                
    # 3. Minify and return string
    return " ".join(soup.get_text(separator=" ").split())

# --- OPENAI API CALL ---
def call_openai(system_prompt, user_content):
    api_key = os.environ.get('OPENAI_API_KEY')
    url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    body = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.1
    }

    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        content = response.json()['choices'][0]['message']['content']
        return json.loads(content)
    else:
        raise Exception(f"OpenAI Error: {response.text}")

def login_to_propensity(driver):
    driver.get("https://auth.propensity.com/sign_in")
    wait = WebDriverWait(driver, 15)
    
    # Login fields (Using .get for safety)
    email_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    email_field.send_keys("dylan@propensity.com")
    driver.find_element(By.NAME, "password").send_keys("Foobar123/")
    driver.find_element(By.ID, "g__submit_btn").click()

# --- MAIN EXECUTION ---
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)
current_config = DATA_TABLE["campaign"]

try:
    # 1. Login
    print("Logging in...")
    login_to_propensity(driver)
    
    # 2. Navigate
    print(f"Navigating to {current_config['link']}...")
    driver.get(current_config['link'])
    wait = WebDriverWait(driver, 15)
    
    # 3. EXPAND ALL SUB-ITEMS
    print("Expanding all sub-items...")
    '''
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, current_config['toggle_css'])))
    
    toggles = driver.find_elements(By.CSS_SELECTOR, current_config['toggle_css'])
    for toggle in toggles:
        try:
            # Scroll to element to ensure it's clickable
            driver.execute_script("arguments[0].scrollIntoView();", toggle)
            toggle.click()
            time.sleep(0.3) 
        except Exception:
            continue # Skip if intercepted or already open

    # 4. Extract Data
    print("Extracting table content...")
    '''
    table_element = driver.find_element(By.ID, current_config['container_id'])
    print(table_element.text)
    raw_html = table_element.get_attribute('outerHTML')
    
    # Clean HTML (Instead of Markdown, GPT-4o-mini is great at parsing cleaned HTML)
    cleaned_data = clean_html_keep_all_data(raw_html)

    # 5. OpenAI Call
    print("Sending data to OpenAI...")
    system_prompt = (
        "Extract all campaigns and their nested sub-items from this data. "
        "Return a JSON object where the 'campaigns' key contains an array of objects. "
        "Each object must include name, status, and an array called 'sub_items'."
    )
    
    result = {}#call_openai(system_prompt, cleaned_data)

    with open("campaigns_data.json", "w") as f:
        json.dump(result, f, indent=4)
        
    print("Done! Saved to campaigns_data.json")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
