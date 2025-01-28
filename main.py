"""
PDF2mp3s
this converts a PDF to mp3s
,basically PDF to audio book.

to be exact it's PDF -> txt -> mp3
... and we can edit the .txt file if we see something we don't like.
(like numbers at the start of each line)

"""
__author__ = "Justin Garza"
__credits__ = ["Justin Garza"]
__version__ = "0.1"
__maintainer__ = "Justin Garza"
__email__ = "JGarza9788@gmail.com"
__status__ = "Development"


import os,re
#import fitz # to convert the pdf to txt
import pymupdf
import asyncio
import utils.tta as tta 
from utils.logMan import createLogger

class PDF2mp3():
    def __init__(self, pdf2txt = True, txt2mp3=True ):
        self.dir = os.path.dirname(os.path.realpath(__file__))

        self.pdfdir = os.path.join(self.dir, "pdf")
        self.txtdir = os.path.join(self.dir, "txt")
        self.mp3dir = os.path.join(self.dir, "mp3")

        self.pdf2txt = pdf2txt
        self.txt2mp3 = txt2mp3
        self.logger = createLogger(__name__)

        # self.data = {}

    def clean_name(self,filename:str):
        return re.sub('(\(.*\)|.pdf)','',filename).strip()
        
    def convert_pdf2txt(self):
        if self.pdf2txt == False:
            return 
        
        for f in os.listdir(self.pdfdir):
            cname = self.clean_name(f)

            pdf_path = os.path.join(self.pdfdir, f)
            txt_file = os.path.join(self.txtdir, cname + '.txt')
            print('pdf -> txt',pdf_path,'->',txt_file)
            
            text = ""
            pdf = pymupdf.open(pdf_path)
            for page_num in range(0, pdf.page_count):
                page = pdf.load_page(page_num)
                text += page.get_text()

            with (open(txt_file, 'w', encoding='utf-8')) as f:
                f.write(text)


    def convert_txt2mp3(self):
        if self.txt2mp3 == False:
            return 
        for f in os.listdir(self.txtdir):
            txt_path = os.path.join(self.txtdir, f)
            mp3_path = os.path.join(self.mp3dir, f + '.mp3')

            text = ''
            with (open(txt_path, 'r', encoding='utf-8')) as f:
                # f.write(extracted_text_pymupdf)
                text = f.read()

            print('txt -> mp3', txt_path, '->', mp3_path)
            asyncio.run(tta.text_to_audio(text, mp3_path))
        


if __name__ == '__main__':
    p = PDF2mp3()
    p.convert_pdf2txt()
    p.convert_txt2mp3()

