from typing import List

class FAQGenerator:
    def __init__(self, llm):
        self.llm = llm

    def generate_faqs_from_chunks(self, chunks: List[str], max_faqs: int = 14) -> List[dict]:
            faqs = []
            for chunk in chunks:
                if len(faqs) >= max_faqs:
                    break  # ✅ Stop once we hit the desired number
        
                prompt = (
                    "Generate 3-5 FAQs from the following content. "
                    "Each FAQ should include a question and a concise answer.\n\n"
                    f"{chunk}\n\n"
                    "Format:\nQ: ...\nA: ..."
                )
                response = self.llm.invoke(prompt)
                output = response.content if hasattr(response, "content") else str(response)
                new_faqs = self._parse_faq_output(output)
        
                space_left = max_faqs - len(faqs)
                faqs.extend(new_faqs[:space_left])  # ✅ Only add what's allowed
            return faqs
        

    def _parse_faq_output(self, output: str) -> List[dict]:
        lines = output.strip().splitlines()
        faqs = []
        question, answer = None, None
        for line in lines:
            if line.startswith("Q:"):
                if question and answer:
                    faqs.append({"question": question, "answer": answer})
                question = line[2:].strip()
                answer = None
            elif line.startswith("A:"):
                answer = line[2:].strip()
        if question and answer:
            faqs.append({"question": question, "answer": answer})
        return faqs
