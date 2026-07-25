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

            ANSWERS_LOOKUP = {
                1: "C) 3rd Position",
                2: "B) Jute Production",
                3: "B) 4th Position",
                4: "C) Potato and Mango",
                5: "C) 45.33%",
                6: "B) Industry: 17.02%, Service: 37.65%",
                7: "D) 61.95%",
                8: "C) It experienced an overall downward trend, declining to around 11.00% by 2023.",
                9: "C) Mughal Period (16th-18th Century)",
                10: "B) The Zamindari System",
                11: "B) The Great Bengal Famine",
                12: "C) The Green Revolution of the 1960s",
                13: "D) 56%",
                14: "B) Habitats: 16%, Forest Lands: 15%",
                15: "C) It has sharply declined due to population growth and urbanization.",
                16: "D) 8,110,000 hectares",
                17: "B) Northern and Western regions",
                18: "B) Soil Salinity Intrusion",
                19: "B) Boro Rice",
                20: "C) Arsenic",
                21: "B) Small landholding and land fragmentation",
                22: "B) Domination of middlemen in the supply chain",
                23: "B) To address deep-seated malnutrition and enhance dietary diversity",
                25: "C) Climate Science and Agriculture",
                26: "C) 50%",
                27: "A) BARC (Bangladesh Agricultural Research Council)",
                28: "B) Integration of local indigenous knowledge systems",
                29: "B) Increase productivity/incomes, enhance climate resilience/adaptation, and reduce/remove GHG emissions.",
                30: "B) Alternate Wetting and Drying (AWD)"
            }

            for idx in range(len(q_indices) - 1):
                block = full_text[q_indices[idx]:q_indices[idx+1]].strip()

                q_num_match = re.match(r'Q(\d+)\.', block)
                if not q_num_match:
                    continue
                q_num = int(q_num_match.group(1))

                opt_start_match = re.search(r'\bA\s*\)', block)
                if not opt_start_match:
                    continue

                q_text_raw = block[:opt_start_match.start()].strip()
                q_text = re.sub(r'^Q\d+\.\s*', '', q_text_raw)
                q_text = " ".join(q_text.split())

                options_part = block[opt_start_match.start():].strip()

                pattern = r'(\b[A-D]\s*\))'
                parts = re.split(pattern, options_part)

                options = []
                current_prefix = ""
                for part in parts:
                    part_str = part.strip()
                    if not part_str:
                        continue
                    if re.match(r'^[A-D]\)$', part_str):
                        current_prefix = part_str
                    else:
                        if current_prefix:
                            clean_option_text = " ".join(part_str.split())
                            options.append(f"{current_prefix} {clean_option_text}")
                            current_prefix = ""

                if len(options) != 4:
                    continue

                correct_answer = ""
                if q_num in ANSWERS_LOOKUP:
                    ans_prefix = ANSWERS_LOOKUP[q_num][:2]
                    for opt in options:
                        if opt.startswith(ans_prefix):
                            correct_answer = opt
                            break

                if not correct_answer:
                    correct_answer = options[0]

                questions.append({
                    "id": len(questions),
                    "question": q_text,
                    "options": options,
                    "answer": correct_answer
                })

            return questions
        except Exception:
            return []            


                



            