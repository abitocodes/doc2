from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import img2pdf
from PyPDF2 import PdfMerger
import time
import os

def web_to_pdf(url, output_file_name):
    # Ensure the results directory exists
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)

    firefox_options = Options()
    firefox_options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)
    
    # Set window size to simulate a mobile device
    driver.set_window_size(630, 891)
    
    try:
        print(f"Loading page: {url}")
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print("Page loaded successfully.")
        
        temp_pdf_files = []
        initial_height = 0
        scroll_unit = driver.get_window_size()["height"]
        print(f"Scroll unit: {scroll_unit}")
        target_height = initial_height + scroll_unit
        last_height = driver.execute_script("return document.body.scrollHeight")
        print("Starting to take screenshots...")
        print(f"Initial height: {target_height}")
        print(f"Last height: {last_height}")
        
        while True:
            # Take a screenshot and save as PDF
            screenshot_png = os.path.join(results_dir, f'temp_screenshot_{len(temp_pdf_files)}.png')
            driver.save_screenshot(screenshot_png)
            print(f"Screenshot saved as {screenshot_png}.")
            
            # Convert PNG to PDF
            temp_pdf = os.path.join(results_dir, f"temp_{len(temp_pdf_files)}.pdf")
            with open(temp_pdf, "wb") as f:
                f.write(img2pdf.convert(screenshot_png))
            temp_pdf_files.append(temp_pdf)
            print(f"Converted {screenshot_png} to {temp_pdf}.")
            
            # Scroll down and check if the bottom of the page is reached
            driver.execute_script(f"window.scrollTo(0, {target_height});")
            time.sleep(2)
            if target_height >= last_height:
                print("Reached the bottom of the page.")
                break
            target_height += scroll_unit
            print(f"Scrolling down to {target_height}...")
        
        # Merge all PDFs into one
        merger = PdfMerger()
        for pdf in temp_pdf_files:
            merger.append(pdf)
        output_file = os.path.join(results_dir, output_file_name)
        merger.write(output_file)
        merger.close()
        print(f"All screenshots merged into {output_file}.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
        # Clean up temp files
        for file in temp_pdf_files:
            os.remove(file)
        print("WebDriver closed and temp files cleaned up.")

web_to_pdf('https://ethereum.org/en/developers/docs/', 'ethereum_docs.pdf')
