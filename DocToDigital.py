from PyPDF2 import PdfFileWriter, PdfFileReader
import textract

class DocToDigital:
    def __init__(self):
        self.x = 0

    def split_pdf(self):
        inputpdf = PdfFileReader(open("C:/Users/jiawe/Downloads/test.pdf", "rb"))
        output = PdfFileWriter()

        for i in range(inputpdf.numPages):
            inputpdf = PdfFileReader(open("C:/Users/jiawe/Downloads/test.pdf", "rb"))
            pageObj = inputpdf.getPage(i)

            result = self.check_for_break(pageObj)
            if result is False:
                output.addPage(inputpdf.getPage(i))
            else:
                with open("C:/Users/jiawe/Downloads/document-page%s.pdf" % i, "wb") as outputStream:
                    output.write(outputStream)
                    output = PdfFileWriter()

    def check_for_break(self, pageObj):
        output = PdfFileWriter()
        output.addPage(pageObj)
        with open("C:/Users/jiawe/Downloads/temp.pdf", "wb") as outputStream:
            output.write(outputStream)

        text = textract.process("C:/Users/jiawe/Downloads/temp.pdf", method='tesseract', language='end')
        print(text)
        return True


tester = DocToDigital()
tester.split_pdf()