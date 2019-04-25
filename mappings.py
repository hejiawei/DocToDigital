import os

tesseract_path = r'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'

temp_dir = "C:/Users/jiawe/Downloads/"
scan_path = "C:/Users/jiawe/Downloads/"
save_path = "C:/Users/jiawe/OneDrive/Desktop/Scans/"

# 'blank' mapping is used when blank pages are used as separators
dir_mapping = {'mortgage statement': os.path.join(save_path, "House Mortgage Statements"),
        'receipts': os.path.join(save_path, "Receipts"),
        'bank statement': os.path.join( save_path, "Bank Statements"),
        'health': os.path.join(save_path, "Health"),
        'car insurance': os.path.join(save_path, "Car Insurance"),
        'blank': os.path.join(save_path, "Collection")}
