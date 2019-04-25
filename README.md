# DocToDigital

__The purpose of this project:__ \
\
This program solves the problem of digitizing and categorizing multiple paper documents at a time. Instead of manually scanning each document and filing them away, DocToDigital allows for a single pdf of multiple scans which it then partitions to separated pdfs using separator sheets--blank sheets to categorize into a general folder or titled sheets for categorizing into specified folders via OCR. 

__The requirements of this project are listed below:__\
\
Python 3.x\

PyPDF2  - PDF manipulation\
pip install PyPDF2
  
pdf2image - convert pdf for image processing\
  pip install pdf2image
  
pillow - Python Imaging Library (PIL) fork\
  pip install pillow
  
poppler - PDF rendering library used by pdf2image\
  conda install -c conda-forge poppler 
  
numpy - mathematical operations\
  pip install numpy
  
pytesseract - wrapper for Google's Tesseract-OCR Engine\
  pip install pytesseract
  include pytesseract.pytesseract.tesseract_cmd = r'<absolute path to tesseract executable>'

      
__Using DocToDigital__: \
\
For every document you want scanned, a single separator sheet needs to go after. If you leave the last document without a separator sheet, it will go to the default folder. Feed the entire stack into your ADF for single- or double-sided scanning, resulting in a single pdf of all your documents. Specify which folder DocToDigital looks in for the scanned pdf as well as how your separator titles map to directories. When you use the command below, DocToDigital will partition the documents into the specified directories and provide a summary of how many documents were scanned and how long the scanning took.


python DocToDigital.py [separator type flag] [single or double-sided doc flag] \
\
Separator type flag:\
DEFAULT: uses titled sheets as separators and categorizes doc based on mapping of title to a specified folder
--blank: uses blank sheets as separators and categorizes doc to a default folder
\
\
Single or double-sided doc flag:
DEFAULT: checks and keeps two pages at a time
--single: skips every other page when generating individual doc

