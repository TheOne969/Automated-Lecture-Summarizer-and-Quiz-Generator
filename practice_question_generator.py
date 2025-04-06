import re

def parse_practice_questions(content: str):
    questions = []
    lines = content.strip().splitlines()
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # === Open-ended question detection ===
        if re.match(r"(?i)\*\*?open-ended question\*\*?:?", line):
            question_text = ""
            i += 1
            while i < len(lines):
                next_line = lines[i].strip()
                if next_line == "" or re.match(r"(?i)\*\*?open-ended question\*\*?:?", next_line):
                    i += 1
                    continue
                question_text = next_line
                break
            if question_text:
                questions.append({
                    "type": "open",
                    "question": question_text
                })

        # === Multiple-choice question detection ===
        elif re.match(r"(?i)(q:|\d+\.\s)", line):
            question_text = re.sub(r"(?i)^q:|\d+\.\s*", "", line).strip()
            options = []
            answer = None
            i += 1

            while i < len(lines):
                next_line = lines[i].strip()

                option_match = re.match(r"^[A-Da-d]\)", next_line)
                if option_match:
                    options.append(next_line[2:].strip())

                elif re.match(r"(?i)^correct answer:", next_line):
                    answer = next_line.split(":", 1)[-1].strip()
                    break
                elif next_line == "":
                    i += 1
                    continue
                else:
                    break
                i += 1

            if question_text and options and answer:
                questions.append({
                    "type": "mcq",
                    "question": question_text,
                    "options": options,
                    "answer": answer
                })

        i += 1

    return questions  # ✅ This is the missing part
