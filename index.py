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
import json

def remove_unwanted_elements(driver):
    driver.execute_script("""
        document.querySelectorAll('header, footer, nav, aside, div.css-134kjkj, div.css-1p9e00f, div.css-7zfpgm, div.css-13i3mb1, .sidebar, .header').forEach(function(element) {
            element.parentNode.removeChild(element);
        });
    """)

def format_title_segment(segment):
    # 각 세그먼트를 대문자로 시작하도록 변환합니다. 예: "nodes-and-clients" -> "Nodes-And-Clients"
    return '-'.join(word.capitalize() for word in segment.split('-'))

def get_document_title_from_url(url):
    # URL을 파싱하여 "docs" 이후의 경로를 추출합니다.
    parts = url.split('/developers/docs/')[1:]
    if not parts:
        # "docs" 이후의 경로가 없는 경우 기본값 반환
        return "Document"

    # 경로를 '_'로 연결하고, 각 세그먼트를 적절히 형식화합니다.
    title_parts = [format_title_segment(part) for part in parts[0].split('/') if part]
    return '_'.join(title_parts).upper() + ".pdf"

def web_to_pdf(url):
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
        
        document_title = get_document_title(driver)
        
        temp_pdf_files = []
        initial_height = 0
        scroll_unit = driver.get_window_size()["height"] - 120
        print(f"Scroll unit: {scroll_unit}")
        target_height = initial_height + scroll_unit
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while True:
            screenshot_png = os.path.join(results_dir, f'temp_screenshot_{len(temp_pdf_files)}.png')
            driver.save_screenshot(screenshot_png)
            
            temp_pdf = os.path.join(results_dir, f"temp_{len(temp_pdf_files)}.pdf")
            with open(temp_pdf, "wb") as f:
                f.write(img2pdf.convert(screenshot_png))
            temp_pdf_files.append(temp_pdf)
            
            driver.execute_script(f"window.scrollTo(0, {target_height});")
            # time.sleep(2)
            if target_height >= last_height:
                break
            target_height += scroll_unit
        
        merger = PdfMerger()
        for pdf in temp_pdf_files:
            merger.append(pdf)
        output_file = os.path.join(results_dir, f"{document_title}.pdf")
        merger.write(output_file)
        merger.close()
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
        for file in temp_pdf_files:
            os.remove(file)

def process_links_from_json(json_file_path, last_successful_url):
    with open(json_file_path, 'r') as json_file:
        links = json.load(json_file)
        # last_successful_url 이후의 링크들만 처리하도록 인덱스를 찾습니다.
        if last_successful_url in links:
            start_index = links.index(last_successful_url) + 1
        else:
            # last_successful_url이 리스트에 없으면 처음부터 시작
            start_index = 0

        for url in links[start_index:]:
            web_to_pdf(url)

# 마지막으로 성공한 URL을 이 함수의 인자로 전달합니다.
# 예를 들어, 마지막 성공한 링크가 'https://ethereum.org/en/developers/docs/data-and-analytics/' 이었다면:
process_links_from_json('crawled-links.json', 'https://ethereum.org/en/developers/docs/data-and-analytics/')

