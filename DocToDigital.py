from PyPDF2 import PdfFileWriter, PdfFileReader
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import os
import numpy as np
import time
import glob

class DocToDigital:
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
        self.dict = {'balboa arms': "C:/Users/jiawe/OneDrive/Desktop/Scans/Balboa Arms",
                     'balboa arms mortgage': "C:/Users/jiawe/OneDrive/Desktop/Scans/Balboa Arms Mortgage",
                     'receipts': "C:/Users/jiawe/OneDrive/Desktop/Scans/Receipts",
                     'bank statements': "C:/Users/jiawe/OneDrive/Desktop/Scans/Bank Statements",}
        self.temp_dir = "C:/Users/jiawe/Downloads/"
        self.total_num_docs = 0
        self.curr_num_docs = 0
        self.num_scans = 0

    def split_pdf(self):
        path = "C:/Users/jiawe/Downloads/img*.pdf"
        if len(glob.glob(path)) is 0:
            return False
        for filename in glob.glob(path):
            print("Scanning " + filename)
            with open(filename, "rb") as f:
                inputpdf = PdfFileReader(f)
                output = PdfFileWriter()

                i = 0
                print("num pages %i " % inputpdf.numPages)
                while i < inputpdf.numPages:
                    pageObj = inputpdf.getPage(i)

                    result, folder = self.check_for_break(i, filename)
                    if result is False:
                        output.addPage(pageObj)
                    else:
                        i += 1

                        if os.path.exists(self.dict[folder]) is not True:
                            os.mkdir(self.dict[folder])
                        self.total_num_docs += 1
                        self.curr_num_docs += 1
                        doc = os.path.join(self.dict[folder],"%s.pdf" % self.total_num_docs)
                        with open(doc, "wb") as outputStream:
                            output.write(outputStream)
                            inputpdf = PdfFileReader(filename)
                            output = PdfFileWriter()

                    i += 1
            os.rename(filename, "C:/Users/jiawe/Downloads/done_%i.pdf" % self.num_scans)
            self.num_scans += 1
        return True

    def check_for_break(self, i, filename):
        temp_pdf = os.path.join(self.temp_dir,"temp.pdf")
        temp_jpeg = os.path.join(self.temp_dir, "temp.jpeg")

        inputpdf = PdfFileReader(filename)
        output = PdfFileWriter()
        pageObj = inputpdf.getPage(i)
        output.addPage(pageObj)

        with open(temp_pdf, "wb") as outputStream:
            output.write(outputStream)

        pages = convert_from_path(temp_pdf, 500)
        for page in pages:
            page.save(temp_jpeg, 'JPEG')
        img = Image.open(temp_jpeg)
        data = np.asarray(img, dtype='int32')

        if np.sum(data) < 670000000:
            return False, None

        text = pytesseract.image_to_string(img)
        os.remove(temp_pdf)
        os.remove(temp_jpeg)

        loc = ''
        for i in range(0,len(text)):
            loc += text[i]
            if loc in self.dict.keys():
                return True, loc
        return False, None

prog = DocToDigital()
while(True):
    start_time = time.time()
    scanned = prog.split_pdf()
    if scanned:
        print("Scanning took " + str(round(time.time() - start_time, 1)) + " seconds.")
        print(str(prog.curr_num_docs) + " documents filed away.")
        prog.curr_num_docs = 0
    time.sleep(5)

