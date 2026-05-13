import PyPDF2

def read_pdf(file_path, out_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
        with open(out_path, 'w', encoding='utf-8') as out_file:
            out_file.write(text)

read_pdf(r"c:\Users\mohan\Desktop\Guardan AI\GuardianAI_Data_Sources_and_Model_Architecture.pdf", r"c:\Users\mohan\Desktop\Guardan AI\pdf_output.txt")
read_pdf(r"c:\Users\mohan\Desktop\Guardan AI\GuardianAI_Fraud_Scam_Chatbot_Development_Process.pdf", r"c:\Users\mohan\Desktop\Guardan AI\pdf_output2.txt")
