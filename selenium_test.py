from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run in headless mode
chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration
chrome_options.add_argument('--no-sandbox')  # Disable sandbox for increased performance (on Linux)
chrome_options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems

# Set the path to your ChromeDriver
chrome_driver_path = '/Users/yanzheng/Downloads/chromedriver-mac-x64/chromedriver'  # Update this to the actual path

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)

try:
    # Open the URL
    driver.get('http://gss.customs.gov.cn/clsouter2020/Home/ClassifyYCDSearch')

    # Wait for the page to load fully
    WebDriverWait(driver, 10).until(  # 增加等待时间
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # Retrieve the full page source
    page_source = driver.page_source

    # Print or save the page source as needed
    print(page_source)

finally:
    # Quit the driver
    driver.quit()