from PyPDF2 import PdfFileWriter, PdfFileReader
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import os
import numpy as np
import time
import datetime
import glob
import argparse
from mappings import dir_mapping, temp_dir, scan_path, tesseract_path

pytesseract.pytesseract.tesseract_cmd = tesseract_path



parser = argparse.ArgumentParser()
parser.add_argument('--blank', help='use blank pages to parse', action='store_true')
parser.add_argument('--single', help='use single-sided scans', action='store_true')

options = parser.parse_args()
use_blank = options.blank
single_sided = options.single


def split_pdf():
    # tracking pdf sets and parsed docs
    curr_num_docs = 0  # num docs from pdf set

    # helper params
    prev_is_doc = False  # auto-copy back pages of docs
    ended = True  # save last doc even without splitter

    file_path = os.path.join(scan_path, "img*.pdf")

    if len(glob.glob(file_path)) is 0:
        return False, curr_num_docs

    filename = glob.glob(file_path)[0]
    print("Scanning " + filename)

    with open(filename, "rb") as f:
        inputpdf = PdfFileReader(f)
        output = PdfFileWriter()

        i = 0
        while i < inputpdf.numPages:
            pageObj = inputpdf.getPage(i)
            # automatically copy back of a doc page
            if prev_is_doc is True:
                ended = False
                prev_is_doc = False
                output.addPage(pageObj)
            else:
                is_splitter, folder = check_for_break(i, f)
                # copy doc page
                if is_splitter is False:
                    ended = False
                    if single_sided is False:
                        prev_is_doc = True
                    output.addPage(pageObj)
                # found splitter page, don't copy it
                else:
                    ended = True
                    # if single-sided scanning not enabled, skip checking the back of the splitter page
                    if single_sided is False:
                        i += 1

                    curr_num_docs += 1

                    if os.path.exists(dir_mapping[folder]) is not True:
                        os.mkdir(dir_mapping[folder])

                    doc = os.path.join(dir_mapping[folder], "%s.pdf" % curr_num_docs)
                    with open(doc, "wb") as outputStream:
                        output.write(outputStream)
                        # bug in PyPDF2, re-initialize
                        inputpdf = PdfFileReader(f)
                        output = PdfFileWriter()
            i += 1

        if ended is False:
            # place it in generic folder
            if os.path.exists(dir_mapping['blank']) is not True:
                os.mkdir(dir_mapping['blank'])

            curr_num_docs += 1

            doc = os.path.join(dir_mapping['blank'], "%s.pdf" % curr_num_docs)
            with open(doc, "wb") as outputStream:
                output.write(outputStream)

    os.rename(filename, os.path.join(scan_path, "%s_digitized.pdf" % datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')))
    return True, curr_num_docs


def check_for_break(i, filename):
    temp_pdf = os.path.join(temp_dir,"doctodigital_temp.pdf")
    temp_jpeg = os.path.join(temp_dir, "doctodigital_temp.jpeg")

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
    if np.sum(data) < 640000000 or np.sum(data) > 720000000:
        return False, None

    if use_blank:
        return True, "blank"

    # OCR
    text = pytesseract.image_to_string(img)

    loc = ''
    for i in range(0,len(text)):
        loc += text[i]
        if loc.lower() in dir_mapping.keys():
            return True, loc.lower()
    return False, None


def main():
    start_time = time.time()
    scanned, curr_num_docs = split_pdf()
    if scanned:
        print("Scanning took " + str(round(time.time() - start_time, 1)) + " seconds.")
        print(str(curr_num_docs) + " documents filed away.")
    else:
        print("No documents available to scan.")


if __name__ == "__main__":
    main()

