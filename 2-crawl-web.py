import json
import os
import img2pdf
from PyPDF2 import PdfMerger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager

def remove_unwanted_elements(driver):
    driver.execute_script("""
        document.querySelectorAll('header, footer, nav, aside, div.css-134kjkj, div.css-1p9e00f, div.css-7zfpgm, div.css-13i3mb1, .sidebar, .header').forEach(function(element) {
            element.parentNode.removeChild(element);
        });
    """)

def web_to_pdf(url, title):
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)
    driver.set_window_size(630, 891)

    try:
        print(f"Loading page: {url}")
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print("Page loaded successfully.")
        remove_unwanted_elements(driver)
        
        temp_pdf_files = []
        temp_image_files = []
        initial_height = 0
        scroll_unit = driver.get_window_size()["height"] - 120
        target_height = initial_height + scroll_unit
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while True:
            screenshot_png = os.path.join(results_dir, f'temp_screenshot_{len(temp_image_files)}.png')
            driver.save_screenshot(screenshot_png)
            temp_image_files.append(screenshot_png)

            temp_pdf = os.path.join(results_dir, f"temp_{len(temp_pdf_files)}.pdf")
            with open(temp_pdf, "wb") as f:
                f.write(img2pdf.convert(screenshot_png))
            temp_pdf_files.append(temp_pdf)
            
            if target_height >= last_height:
                break
            target_height += scroll_unit
        
        merger = PdfMerger()
        for pdf in temp_pdf_files:
            merger.append(pdf)
        output_file = os.path.join(results_dir, title + ".pdf")
        merger.write(output_file)
        merger.close()
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
        for file in temp_pdf_files + temp_image_files:
            os.remove(file)

def process_links_from_json(json_file_path, start_index, end_index):
    with open(json_file_path, 'r') as json_file:
        links = json.load(json_file)[start_index:end_index+1]
        for link in links:
            web_to_pdf(link["url"], link["title"])

process_links_from_json('crawled-links.json', 6, 7)
