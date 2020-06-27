import os
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine

# pull file
# base_path = "C://some_folder"
# my_file = os.path.join(base_path + "/" + "test_pdf.pdf")
# log_file = os.path.join(base_path + "/" + "pdf_log.txt")
fp = open('./aoda.pdf', 'rb')


# log_file = 

password = ""
extracted_text = ""

# parser stores objects from pdf
# document requests objects from pdf
parser = PDFParser(fp)
document = PDFDocument()
parser.set_document(document)
document.set_parser(parser)
document.initialize('')

# Create PDFResourceManager object that stores shared resources such as fonts or images
rsrcmgr = PDFResourceManager()

# set parameters for analysis
laparams = LAParams()
laparams.char_margin = 1.0
laparams.word_margin = 1.0

# Create a PDFDevice object which translates interpreted information into desired format
# Device needs to be connected to resource manager to store shared resources
# device = PDFDevice(rsrcmgr)
# Extract the decive to page aggregator to get LT object elements
device = PDFPageAggregator(rsrcmgr, laparams=laparams)

# Create interpreter object to process page content from PDFDocument
# Interpreter needs to be connected to resource manager for shared resources and device 
interpreter = PDFPageInterpreter(rsrcmgr, device)
extracted_text = ''

for page in document.get_pages():
    interpreter.process_page(page)
    # The device renders the layout from interpreter
    layout = device.get_result()
    #look for LTTextBox LTTextLine in lt_obj list
    for lt_obj in layout:
        if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
            extracted_text += lt_obj.get_text()

#close the pdf file
fp.close()

# print (extracted_text.encode("utf-8"))
			
with open('./write.txt', "wb") as my_log:
	my_log.write(extracted_text.encode("utf-8"))
print("Done !!")
