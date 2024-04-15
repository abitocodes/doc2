# doc2
Webpage to PDF Conversion Tool

## Description
This project provides a toolset for crawling web pages (specifically from Ethereum Tech Docs as an example, https://ethereum.org/en/developers/docs/), converting them into PDF format, and optionally reversing the colors for print. The process is divided into several steps, each handled by a separate script.

## Prerequisites
Before you begin, ensure you have Python installed on your machine along with the following libraries:
- selenium
- webdriver_manager
- PyPDF2
- img2pdf
- pdf2image
- PIL (Pillow)

## Installation
Clone this repository to your local machine using:
```bash
git clone https://github.com/abitocodes/doc2.git
```

## Usage
To use this tool, perform the following steps in order:
1. **Crawl Links**: Extract all relevant links from a webpage.
   ```bash
   python 1-crawl-links.py
   ```
2. **Crawl Web**: Download and convert the web pages from the crawled links into PDF files. You can modify the parameters `6` and `7` in `process_links_from_json('crawled-links.json', 6, 7)` to specify the range of pages you want to process from the `crawled-links.json`.
   ```bash
   python 2-crawl-web.py
   ```
3. **Merge PDFs**: Combine all the PDF files into one single document.
   ```bash
   python 3-merge-crawled-pdfs.py
   ```
4. **Reverse PDF Color**: Modify the PDF for print by inverting its colors.
   ```bash
   python 4-reverse-pdf-color-for-print.py
   ```

## Output
The scripts will generate PDFs in the 'results' directory and ultimately produce a merged and color-inverted PDF in the project root directory.
