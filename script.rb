require 'selenium-webdriver'

options = Selenium::WebDriver::Chrome::Options.new
options.binary = '/usr/bin/chromium-browser'   # ← this is the key fix
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')

service = Selenium::WebDriver::Chrome::Service.new(path: '/usr/bin/chromedriver')

driver = Selenium::WebDriver.for :chrome, service: service, options: options

begin
  driver.get('https://t-propensity-rest-api.addapptation.com/test_page')
  sleep 2

  driver.find_element(id: 'user-input').send_keys(ENV['INPUT_MESSAGE'] || 'Hello!')
  driver.find_element(id: 'submitBtn').click
  sleep 3

  puts driver.find_element(id: 'chat-window').text

rescue => e
  puts "Error: #{e.message}"
ensure
  driver.quit
end
