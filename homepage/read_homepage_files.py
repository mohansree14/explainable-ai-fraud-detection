import os
import PyPDF2

def read_pdfs(folder_path, output_file):
    with open(output_file, 'w', encoding='utf-8') as out_f:
        for filename in os.listdir(folder_path):
            if filename.lower().endswith('.pdf'):
                file_path = os.path.join(folder_path, filename)
                try:
                    with open(file_path, 'rb') as f:
                        reader = PyPDF2.PdfReader(f)
                        text = ''
                        for page in reader.pages:
                            extracted = page.extract_text()
                            if extracted:
                                text += extracted + '\n'
                        out_f.write(f"--- File: {filename} ---\n")
                        out_f.write(text + "\n\n")
                except Exception as e:
                    out_f.write(f"--- File: {filename} (Error reading: {e}) ---\n\n")

if __name__ == '__main__':
    folder = r"c:\Users\mohan\Desktop\Guardan AI\homepage\Home page changes"
    out_file = r"c:\Users\mohan\Desktop\Guardan AI\homepage_content_extracted.txt"
    read_pdfs(folder, out_file)
    print(f"Extraction complete. Results saved to {out_file}")
