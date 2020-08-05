import os
import logging
import csv
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine

# alternate method of accessing file
# base_path = "C://some_folder"
# my_file = os.path.join(base_path + "/" + "test_pdf.pdf")
# Loop through base_path
# csv path - C:\automate\attachment_list\incoming
# pdf path C:\automate\attachment\archive\BULOVA\2020\07
# Loop through csvs - grab filename, look in pdf directory for file to process 
# need to access vendor name
# ----- Build loops -------
# csv_path = C:\automate\attachment_list\incoming
# for vendor in csv_path
# for csv in vendor
# loop through csv - rows and columns - use hard coded index values 
listOfPDFs = []
list_of_msg_id = []
list_of_csv = []
# ---------------------------  Path variables deorecated - will be vendor non-specific -------------------------
# base_path = "./exchangeemail/Bulova"
# base_path = "./exchangeemail/Test"
# directory = os.fsencode(f'{base_path}/temp')
csv_directory = "./attachment_list/incoming"
base_path = "./attachment/archive"
# csv_directory = "./"
# csvFile = 'log.csv'
# ---------------------------   Add CSV Files to List  --------------------------
# for file in os.listdir(csv_directory):
#     filename = os.fsdecode(file)
#     if filename.endswith(".csv"):
#         list_of_csv.append(filename)
# ---------------------------   Convert files to text for each CSV --------------------------
# on each loop, each row of csv file needs to access a file, extract test, write new file
for vendor in os.listdir(csv_directory):
    for csv in vendor:
        with open(f'{csv_directory}/{vendor}/{csv}', 'r') as file:
            reader = csv.reader(file)
            for row in reader: 
                # setup variables to collect from csv    
                pdf_file_name = ''
                email_year = None
                email_month = None
                attachment_list = None
                message_id = None
                Bcc = None
                Cc = None
                date_recieved = None
                email_from = None
                has_attachments = True
                subject = None
                email_to = None
                for index, column in enumerate(row):
                    if index == 0:
                        pdf_file_name = column
                    if index == 1:
                        email_year = column
                    if index == 2:
                        email_month = column
                    if index == 3:
                        attachment_list = column
                    if index == 4:
                        message_id = column
                    if index == 5:
                        Bcc = column
                    if index == 6:
                        Cc = column
                    if index == 7:
                        date_recieved = column
                    if index == 8:
                        email_from = column
                    if index == 9:
                        has_attachments = column
                    if index == 10:
                        subject = column
                    if index == 11:
                        email_to = column
                # for each row, access file to process and process
                # use email month and year to access pdf file - already have vendor name 
                fp = open(f'./{base_path}/{vendor}/{email_year}/{email_month}/{pdf_file_name}', 'rb')
                password = ""
                extracted_text = ""
                message_id = ""
                split_file = pdf_file_name.split(".pdf")[0]
                # for id in list_of_msg_id:
                #     # print(id)
                #     if split_file in id:
                #         message_id = id
                # message_id += "////"
                # print(message_id)
                # document requests objects from pdf
                # parser stores objects from pdf into document

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
                # for each page in pdf, process text into seperate txt file
                for index, page in enumerate(document.get_pages()):
                    interpreter.process_page(page)
                    # The device renders the layout from interpreter
                    layout = device.get_result()
                    # look for LTTextBox LTTextLine in lt_obj list
                    for lt_obj in layout:
                        if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                            extracted_text += lt_obj.get_text()
                    # print (extracted_text.encode("utf-8"))
                    # The outfile should be in binary mode.
                    # Save file as combination of file and page number 
                    file_name = f'{file}_{index}.txt'
                    if os.path.isfile(file_name):
                        expand = 1
                        while True:
                            expand += 1
                            new_file_name = file_name.split(".txt")[0] + str(expand) + ".txt"
                            if os.path.isfile(new_file_name):
                                continue
                            else:
                                file_name = new_file_name
                                break
                    # write extracted text to txt file
                    with open(f'{supplier_path}/Text/{file_name}', "wb") as my_log:
                        my_log.write(message_id.encode("utf-8"))
                        my_log.write(extracted_text.encode("utf-8"))
                # close the pdf file
                fp.close()
for csv in list_of_csv:
    # open csv and loop through its columns
    with open(f'{csv_directory}/{csv}', 'r') as file:
        reader = csv.reader(file)
        for row in reader: 
            list_of_msg_id.append(row[0])
    # extract document path from csv - deprecated
    supplier_path = list_of_msg_id.pop(0)
    # open and loop through directory containing pdfs
    pdf_directory = os.fsencode(supplier_path + "/temp")
    for file in os.listdir(pdf_directory):
        # add all filenames that end in .pdf to a list to loop through 
        filename = os.fsdecode(file)
        if filename.endswith(".pdf"):
            listOfPDFs.append(filename)
    for file in listOfPDFs:
        try:
            # open file and extract message id / text to .txt file 
            fp = open(f'./{supplier_path}/temp/{file}', 'rb')
            password = ""
            extracted_text = ""
            message_id = ""
            split_file = file.split(".pdf")[0]
            for id in list_of_msg_id:
                # print(id)
                if split_file in id:
                    message_id = id
            message_id += "////"
            # print(message_id)
            # document requests objects from pdf
            # parser stores objects from pdf into document

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
            # for each page in pdf, process text into seperate txt file
            for index, page in enumerate(document.get_pages()):
                interpreter.process_page(page)
                # The device renders the layout from interpreter
                layout = device.get_result()
                # look for LTTextBox LTTextLine in lt_obj list
                for lt_obj in layout:
                    if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                        extracted_text += lt_obj.get_text()
                # print (extracted_text.encode("utf-8"))
                # The outfile should be in binary mode.
                # Save file as combination of file and page number 
                file_name = f'{file}_{index}.txt'
                if os.path.isfile(file_name):
                    expand = 1
                    while True:
                        expand += 1
                        new_file_name = file_name.split(".txt")[0] + str(expand) + ".txt"
                        if os.path.isfile(new_file_name):
                            continue
                        else:
                            file_name = new_file_name
                            break
                # write extracted text to txt file
                with open(f'{supplier_path}/Text/{file_name}', "wb") as my_log:
                    my_log.write(message_id.encode("utf-8"))
                    my_log.write(extracted_text.encode("utf-8"))
            # close the pdf file
            fp.close()

            # with open(f'{base_path}/Text/{file}.txt', "wb") as my_log:
            #     my_log.write(extracted_text.encode("utf-8"))
            # with open(f'./{csvFile}', "w") as csv_file:
            #     writer = csv.writer(csv_file, delimiter='\t', lineterminator='\n')
            #     # row = [file + 'success']
            #     writer.writerow(f'{file} success')
                # csv_file.write((f'{file} success').encode("utf-8"))
        except: 
            #write error to log file
            # with open(f'./{csvFile}', "w") as csv_file:
            #     writer = csv.writer(csv_file, delimiter='\t', lineterminator='\n')
            #     # row = [file + 'failed']
            #     # writer.writerow(row)
            #     writer.writerow(f'{file} failed')
            #     # csv_file.write((f'{file} failed').encode("utf-8"))
            print("Error !!")
    print("CSV Processed")
    # os.rename('/Users/billy/d1/xfile.txt', '/Users/billy/d2/xfile.txt')
print("Task Complete")

# fp = open('./incentive/i4.pdf', 'rb')
# password = ""
# extracted_text = ""

# # ---------------------------    PROGRAM   --------------------------

# # document requests objects from pdf
# # parser stores objects from pdf into document

# parser = PDFParser(fp)
# document = PDFDocument()
# parser.set_document(document)
# document.set_parser(parser)
# document.initialize('')

# # Create PDFResourceManager object that stores shared resources such as fonts or images

# rsrcmgr = PDFResourceManager()

# # set parameters for analysis

# laparams = LAParams()
# laparams.char_margin = 1.0
# laparams.word_margin = 1.0

# # Create a PDFDevice object which translates interpreted information into desired format
# # Device needs to be connected to resource manager to store shared resources
# # device = PDFDevice(rsrcmgr)
# # Extract the decive to page aggregator to get LT object elements
# device = PDFPageAggregator(rsrcmgr, laparams=laparams)

# # Create interpreter object to process page content from PDFDocument
# # Interpreter needs to be connected to resource manager for shared resources and device
# interpreter = PDFPageInterpreter(rsrcmgr, device)
# extracted_text = ''

# for page in document.get_pages():
#     interpreter.process_page(page)
#     # The device renders the layout from interpreter
#     layout = device.get_result()
#     #look for LTTextBox LTTextLine in lt_obj list
#     for lt_obj in layout:
#         if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
#             extracted_text += lt_obj.get_text()

# #close the pdf file
# fp.close()

# # print (extracted_text.encode("utf-8"))
# # The outfile should be in binary mode.
# with open('./incentive/i4.txt', "wb") as my_log:
# 	my_log.write(extracted_text.encode("utf-8"))
# print("Done !!")


# # ---------------------------   NOTES     --------------------------

# # directory = 'the/directory/you/want/to/use'

# # for filename in os.listdir(directory):
#     #   if filename.endswith(".txt"):
#     #     f = open(filename)
#     #     lines = f.read()
#     #     print(lines[10])
#     #     continue
#     # else:
#     # continue

# # pull file
# # fp = open('./testpdf2.pdf', 'rb')
# # password = ""
# # extracted_text = ""
