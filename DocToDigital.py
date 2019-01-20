from PyPDF2 import PdfFileWriter, PdfFileReader
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import os
import numpy as np
import time

class DocToDigital:
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
        self.dict = {'Bank Statement': "C:/Users/jiawe/Downloads/Bank",
                     'Car Payment': "C:/Users/jiawe/Downloads/Car"}
        self.temp_dir = "C:/Users/jiawe/Downloads/"
        self.num_docs = 0
    def split_pdf(self):
        inputpdf = PdfFileReader(open("C:/Users/jiawe/Downloads/test.pdf", "rb"))
        output = PdfFileWriter()

        for i in range(inputpdf.numPages):
            pageObj = inputpdf.getPage(i)

            result, folder = self.check_for_break(i)
            if result is False:
                output.addPage(pageObj)
            else:
                if os.path.exists(self.dict[folder]) is not True:
                    os.mkdir(self.dict[folder])
                self.num_docs += 1
                doc = os.path.join(self.dict[folder],"%s.pdf" % self.num_docs)
                with open(doc, "wb") as outputStream:
                    output.write(outputStream)
                    inputpdf = PdfFileReader(open("C:/Users/jiawe/Downloads/test.pdf", "rb"))
                    output = PdfFileWriter()

    def check_for_break(self, i):
        temp_pdf = os.path.join(self.temp_dir,"temp.pdf")
        temp_jpeg = os.path.join(self.temp_dir, "temp.jpeg")

        inputpdf = PdfFileReader(open("C:/Users/jiawe/Downloads/test.pdf", "rb"))
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

        if np.sum(data) < 690000000:
            return False, None

        text = pytesseract.image_to_string(img)
        os.remove(temp_pdf)
        os.remove(temp_jpeg)
        loc = ''

        for i in range(0,len(text)-1):
            loc += text[i]

        if loc in self.dict.keys():
            return True, loc
        return False, None

prog = DocToDigital()
start_time = time.time()
prog.split_pdf()

print("Scanning took " + str(round(time.time() - start_time,1)) + " seconds.")
print(str(prog.num_docs) + " documents filed away.")