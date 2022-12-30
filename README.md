# PDF Document Compiler

The PDF file compiler is a script designed to compile promotion applications in the Sri Lankan University system. In order to use it, you must have 
- Python 3.0 installed 
and have the following Python libraries installed via pip: 

  - PyPDF2
  - reportlab
  - natsort
  - shutil.

This script offers several useful features: 
- it can add a label featuring your file name to the top right of each page
- add page numbers to the bottom of each page
- orient landscape pages to portrait
- automatically add spaces to the top and bottom of each page to make room for the label and page numbers.

To use this script:
- Create a directory and place all the PDF documents that you want to label in it. Make sure that the documents are sized to A4.
- Place the script in the same location as the directory with the PDFs.
- In line 15 of the script (compiler.py), specify the name of the directory containing the PDFs.
- Run the script.
- A pdf with the <directory-name>-paged.pdf will be created in the directory you specified in line 15.

Please note that this software is provided "as is" and comes with no warranty of any kind, express or implied. The authors and copyright holders shall not be held liable for any claims, damages, or other liabilities arising from or in connection with the use of this software.
