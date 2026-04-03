require 'selenium-webdriver'

options = Selenium::WebDriver::Chrome::Options.new
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')

driver = Selenium::WebDriver.for :chrome, options: options

begin
  # --- LOGIN ---
  driver.get('https://t-propensity-rest-api.addapptation.com/login')
  sleep 2

  driver.find_element(id: 'email').send_keys(ENV['SITE_EMAIL'])
  driver.find_element(id: 'password').send_keys(ENV['SITE_PASSWORD'])
  driver.find_element(css: 'button[type="submit"]').click
  sleep 3

  # --- NAVIGATE TO PAGE ---
  driver.get('https://t-propensity-rest-api.addapptation.com/test_page')
  sleep 2

  # --- SUBMIT DATA ---
  message = ENV['INPUT_MESSAGE'] || 'Default message'
  driver.find_element(id: 'user-input').send_keys(message)
  driver.find_element(id: 'submitBtn').click
  sleep 3

  # --- READ RESPONSE ---
  puts driver.find_element(id: 'chat-window').text

rescue => e
  puts "Error: #{e.message}"
  puts driver.page_source  # helps debug login issues
ensure
  driver.quit
end
