from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import json
import time

# Setup options for WebDriver
options = Options()
options.add_argument('--headless')  # Run in headless mode, optional

# Set up WebDriver
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

# Navigate to the page
driver.get("https://ethereum.org/en/developers/docs/")

# Wait for the necessary elements to load
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#__next > div > div.css-hgrqbb > div.css-1kc3w28 > nav')))

# Find all the menus using the specified selector and click to expand them
menus = driver.find_elements(By.CSS_SELECTOR, '#__next > div > div.css-hgrqbb > div.css-1kc3w28 > nav > div')
for menu in menus:
    menu.click()
    time.sleep(1)  # Wait a bit to ensure the menu has expanded

links = []
link_index = 0  # Initialize a counter for the links

expanded_menus = driver.find_elements(By.CSS_SELECTOR, '#__next > div > div.css-hgrqbb > div.css-1kc3w28 > nav > div > div')
for expanded_menu in expanded_menus:
    menu_links = expanded_menu.find_elements(By.TAG_NAME, 'a')
    for link in menu_links:
        url = link.get_attribute('href')
        _url = url.rstrip('/').split('/')
        last_segment = url.rstrip('/').split('/')[-1].upper()
        title = ''
        for k, v in enumerate(_url, start=6):
            try:
                title = title + '_' + _url[k]
            except:
                break
        title = f"{link_index}{title.upper()}"
        link_data = {
            "url": url,
            "title": title
        }
        links.append(link_data)
        link_index += 1  # Increment the link index

# Save the links to a JSON file
with open('crawled-links.json', 'w') as file:
    json.dump(links, file, indent=4)

# Close the driver
driver.quit()

print('Links have been saved to crawled-links.json')
