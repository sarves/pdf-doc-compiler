#by sarves - iamsarves@gmail.com
#version - 20221229
#published under Apache License, Version 2.0 https://www.apache.org/licenses/LICENSE-2.0.txt

import os
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
import PyPDF2
from decimal import *
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
import natsort
import shutil

# Set the directory you want to read from. The final output will be created in the director you point below, and the file name will be <directory name>.pdf
directory = 'All'

#mac creates temp stroage files which cause errors, so removing it.
if os.path.exists(directory + "/"+".DS_Store"):
    os.remove(directory + "/"+".DS_Store")

#remove if three is a file exist already.
if os.path.exists(directory+"/"+directory+"-Paged.pdf"):
    os.remove(directory+"/"+directory+"-Paged.pdf")
    
files_unsorted = os.listdir(directory)
files=sorted(files_unsorted)
for file in files:
    writer = PdfFileWriter()
    # Open the PDF file in read-binary mode
    file_path = os.path.join(directory, file)
    # Split the file name and extension
    filename, ext = os.path.splitext(file)
    #print(filename)
    canvas = Canvas("hello.pdf", pagesize=(8.3*72+30,11.7*72+100))
    canvas.setFillColorRGB(0,0,0)
    canvas.roundRect(500, 850, 100, 30, 4, stroke=1, fill=1)
    canvas.setFillColorRGB(255,255,255)
    canvas.setFont("Helvetica", 15)
    canvas.drawString(510, 860, filename)
    canvas.save()

    with open(file_path, 'rb') as file:
        # Create a PDF object
        pdf = PdfFileReader(file)
        # Iterate through all the pages
        for page in range(pdf.getNumPages()):
            # Get the current page
            current_page = pdf.getPage(page)
            
            # Identify the orientation of the page
            orientation = current_page.get('/Rotate')
            
            # Rotate it if it is in landscape
            if orientation == 90:
                current_page.rotateClockwise(-90)
            elif orientation == 270:
                current_page.rotateClockwise(90)

            # Create a PDF object for the header
            header = PdfFileReader(open('hello.pdf', 'rb'))

            # add a blank space or extend the header to add label
            current_page.mediaBox.upperRight = (current_page.mediaBox.getUpperRight_x()+40, current_page.mediaBox.getUpperRight_y() + 80)
            current_page.mediaBox.lowerLeft = (current_page.mediaBox.getLowerLeft_x()-40, current_page.mediaBox.getLowerLeft_y()-50)
            
            # Merge the header with the current page
            current_page.mergePage(header.getPage(0))

            # Add the modified page back to the PDF
            writer.addPage(current_page)

        isExist = os.path.exists(directory + "-output")
        if not isExist:
            os.makedirs(directory + "-output")

        # Create a new PDF file to write the output
        with open(directory + "-output/" + filename+"-header.pdf", 'wb') as output:
            # Write the modified PDF to the output file
            writer.write(output)
        output.close()


# the following section will merge all the pdfs, sort them according to the file name and add the final file to the original directory.

pdf_merger = PdfFileMerger()
path = directory + "-output"
files_unsorted = os.listdir(path)
files=natsort.natsorted(files_unsorted)
for pdf in files:
    #filename, ext = os.path.splitext(pdf)
    #print(filename)
    if pdf.endswith('.pdf'):
        pdf_merger.append(path + '/' + pdf)
output_pdf = directory+"/"+directory+".pdf"
pdf_merger.write(output_pdf)
pdf_merger.close()

# The following section will add page numbers

# add_numbering_to_pdf(directory+"/"+directory+".pdf", directory+"/"+directory+"-pages.pdf")

counter=1
merged_file=directory+"/"+directory

with open(merged_file+".pdf", 'rb') as file:
        # Create a PDF object
        pdf = PdfFileReader(file)
        # Iterate through all the pages
        for page in range(pdf.getNumPages()):
            # Get the current page
            cur_page = pdf.getPage(page)

            canvas = Canvas("hello.pdf", pagesize=(8.3*72+30,11.7*72+100))
            canvas.setFillColorRGB(0,0,0)
            canvas.roundRect(280, 30, 40, 18, 4, stroke=1, fill=1)
            canvas.setFillColorRGB(255,255,255)
            canvas.setFont("Helvetica", 15)
            canvas.drawString(285, 35, str(counter))
            counter=counter+1
            canvas.save()
    
            # Create a PDF object for the header
            footer = PdfFileReader(open('hello.pdf', 'rb'))
             
            # Merge the header with the current page
            cur_page.mergePage(footer.getPage(0))

            # Add the modified page back to the PDF
            writer.addPage(cur_page)

        # Create a new PDF file to write the output
        with open(merged_file+"-Paged.pdf", 'wb') as output:
            # Write the modified PDF to the output file
            writer.write(output)
        output.close()

#Remove output directory which is created during the compilation.
shutil.rmtree(directory + "-output")
#remove if three is a file exist already.
if os.path.exists(directory+"/"+directory+".pdf"):
    os.remove(directory+"/"+directory+".pdf")
