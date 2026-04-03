require 'selenium-webdriver'

options = Selenium::WebDriver::Chrome::Options.new
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')

driver = Selenium::WebDriver.for :chrome, options: options

begin
  # Navigate to your page
  driver.get('https://t-propensity-rest-api.addapptation.com/test_page')
  sleep 2

  # Fill the textarea
  textarea = driver.find_element(id: 'user-input')
  textarea.send_keys('Hello from GitHub Actions!')

  # Click submit
  driver.find_element(id: 'submitBtn').click
  sleep 3

  # Print the response
  puts driver.find_element(id: 'chat-window').text

rescue => e
  puts "Error: #{e.message}"
ensure
  driver.quit
end
