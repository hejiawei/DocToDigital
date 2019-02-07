from PyPDF2 import PdfFileWriter, PdfFileReader
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import os
import numpy as np
import time
import glob
import argparse

class DocToDigital:
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'

        self.dict = {'balboa arms': "C:/Users/jiawe/OneDrive/Desktop/Scans/5404 Balboa Arms",
                     'balboa arms mortgage': "C:/Users/jiawe/OneDrive/Desktop/Scans/Balboa Arms Mortgage",
                     'receipts': "C:/Users/jiawe/OneDrive/Desktop/Scans/Receipts",
                     'bank statement': "C:/Users/jiawe/OneDrive/Desktop/Scans/Bank Statements",
                     'nobel dr': "C:/Users/jiawe/OneDrive/Desktop/Scans/4435 Nobel Dr",
                     'car insurance': "C:/Users/jiawe/OneDrive/Desktop/Scans/Car Insurance",
                     'blank' : "C:/Users/jiawe/OneDrive/Desktop/Scans/Collection"}

        self.temp_dir = "C:/Users/jiawe/Downloads/"
        self.scan_path = "C:/Users/jiawe/Downloads/"

        # tracking pdf sets and parsed docs
        self.total_num_docs = 0 # # total num docs in one run
        self.curr_num_docs = 0  # num docs from pdf set
        self.num_scans = 0  # pdf set of scans

        # helper params
        self.prev_is_doc = False    # auto-copy back pages of docs
        self.use_blank = False  # blank splitter mode
        self.single_sided = False   # single-sided doc mode
        self.ended = True   # save last doc even without splitter

        parser = argparse.ArgumentParser()
        parser.add_argument('--blank', help='use blank pages to parse', action='store_true')
        parser.add_argument('--single', help='use single-sided scans', action='store_true')

        options = parser.parse_args()
        self.use_blank = options.blank
        self.single_sided = options.single

    def split_pdf(self):
        file_path = os.path.join(self.scan_path, "img*.pdf")

        if len(glob.glob(file_path)) is 0:
            return False

        filename = glob.glob(file_path)[0]
        print("Scanning " + filename)

        with open(filename, "rb") as f:
            inputpdf = PdfFileReader(f)
            output = PdfFileWriter()

            i = 0
            while i < inputpdf.numPages:
                pageObj = inputpdf.getPage(i)

                # automatically copy back of a doc page
                if self.prev_is_doc is True:
                    self.ended = False
                    self.prev_is_doc = False
                    output.addPage(pageObj)
                else:
                    is_splitter, folder = self.check_for_break(i, f)

                    # copy doc page
                    if is_splitter is False:
                        self.ended = False
                        if self.single_sided is False:
                            self.prev_is_doc = True
                        output.addPage(pageObj)
                    # found splitter page, don't copy it
                    else:
                        self.ended = True
                        # if single-sided scanning not enabled, skip checking the back of the splitter page
                        if self.single_sided is False:
                            i += 1

                        self.total_num_docs += 1
                        self.curr_num_docs += 1

                        if os.path.exists(self.dict[folder]) is not True:
                            os.mkdir(self.dict[folder])

                        doc = os.path.join(self.dict[folder],"%s.pdf" % self.total_num_docs)
                        with open(doc, "wb") as outputStream:
                            output.write(outputStream)
                            # bug in PyPDF2, re-initialize
                            inputpdf = PdfFileReader(f)
                            output = PdfFileWriter()
                i += 1

        if self.ended is False:
            # place it in generic folder
            if os.path.exists(self.dict['blank']) is not True:
                os.mkdir(self.dict['blank'])

            self.total_num_docs += 1
            self.curr_num_docs += 1

            doc = os.path.join(self.dict['blank'], "%s.pdf" % self.total_num_docs)
            with open(doc, "wb") as outputStream:
                output.write(outputStream)

        os.rename(filename, os.path.join(self.scan_path, "done_%i.pdf" % self.num_scans))
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

        pages = convert_from_path(temp_pdf, 500)    # convert to img
        pages[0].save(temp_jpeg, 'JPEG')    # save as jpeg
        img = Image.open(temp_jpeg)
        data = np.asarray(img, dtype='int32')

        os.remove(temp_pdf)
        os.remove(temp_jpeg)

        # likely a doc page
        if np.sum(data) < 640000000:
            return False, None

        if self.use_blank:
            return True, "blank"

        # OCR
        text = pytesseract.image_to_string(img)

        loc = ''
        for i in range(0,len(text)):
            loc += text[i]
            if loc.lower() in self.dict.keys():
                return True, loc.lower()
        return False, None


prog = DocToDigital()
while True:
    start_time = time.time()
    scanned = prog.split_pdf()
    if scanned:
        print("Scanning took " + str(round(time.time() - start_time, 1)) + " seconds.")
        print(str(prog.curr_num_docs) + " documents filed away.")
        prog.curr_num_docs = 0
    else:
        time.sleep(5)

