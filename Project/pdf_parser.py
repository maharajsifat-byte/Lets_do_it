import re

class PDFProcessor:
    @staticmethod
    def extract_mcqs(file_path):
        try:
            from pypdf import PdfReader
        except Exception:
            return []

        try:
            reader = PdfReader(file_path)
            full_text = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
        except Exception:
            return []

        blocks = re.split(r"(?=\bQ\d+\.)", full_text)
        questions = []
        for block in blocks:
            block = block.strip()
            if not block or not re.match(r"^Q\d+\.", block):
                continue

            lines = [line.strip() for line in block.splitlines() if line.strip()]
            if not lines:
                continue

            question_line = re.sub(r"^Q\d+\.\s*", "", lines[0]).strip()
            option_lines = [line for line in lines[1:] if re.match(r"^[A-D]\)", line)]
            if len(option_lines) < 4:
                continue

            options = option_lines[:4]
            answer = options[0]
            for line in lines[1:]:
                match = re.match(r"^Answer\s*:\s*([A-D]\)\s*.*)$", line, flags=re.IGNORECASE)
                if match:
                    answer = match.group(1).strip()
                    break

            questions.append(
                {
                    "id": len(questions),
                    "question": question_line,
                    "options": options,
                    "answer": answer,
                }
            )

        return questions