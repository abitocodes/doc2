import os
import re
from PyPDF2 import PdfMerger

# Directory path where PDF files are stored
pdf_dir = './results'

# Load all PDF files in the directory
pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]

# Extract and convert the numeric part from the file names to integers for sorting
sorted_files = sorted(pdf_files, key=lambda x: int(re.search(r'\d+', x).group()))

# Create a PDF merger object
merger = PdfMerger()

# Append sorted files one by one
for pdf in sorted_files:
    merger.append(os.path.join(pdf_dir, pdf))

# Merge all files into one and save the result
output_pdf_path = os.path.join('merged_document.pdf')
merger.write(output_pdf_path)
merger.close()

print(f"All PDFs merged into {output_pdf_path}")
