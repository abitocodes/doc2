import os
from pdf2image import convert_from_path
from PIL import Image
import numpy as np

# Path of the original PDF file
input_pdf_path = 'merged_document.pdf'
# Path to save the reversed images as a PDF file
output_pdf_path = 'merged_document_reversed.pdf'

# Convert PDF to images (setting DPI to 200 here)
pages = convert_from_path(input_pdf_path, 200)

# Processing the first page to start creating the PDF
first_inverted_image = Image.fromarray(255 - np.array(pages[0]))
first_inverted_image = first_inverted_image.convert('RGB')  # Convert to RGB mode for PDF saving

# Processing the remaining pages
rest_inverted_images = [Image.fromarray(255 - np.array(page)).convert('RGB') for page in pages[1:]]

# Save the first page and append the remaining pages
first_inverted_image.save(output_pdf_path, 'PDF', resolution=100.0, save_all=True, append_images=rest_inverted_images)

print(f"Inverted color PDF saved to {output_pdf_path}")
