import PyPDF2

def extract_text_from_pdf(file_path):
    pdf_file = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    pdf_file.close()
    return text

file_path = '/Users/selinceydeli/Desktop/sabancı/OPIM407/Individual Assignment-3/16701573.pdf'  # replace with your file path
text = extract_text_from_pdf(file_path)
print(text)
