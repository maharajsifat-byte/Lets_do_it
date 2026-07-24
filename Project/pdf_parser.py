import re

class PDFProcessor:
    @staticmethod
    def extract_mcqs(file_path):
        try:
            from pypdf import PdfReader
            reader = PdfReader(file_path)
            full_text = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"

            q_indices = [m.start() for m in re.finditer(r'\bQ\d+\.', full_text)]
            if not q_indices:
                 return []

            questions = []
            q_indices.append(len(full_text))


            