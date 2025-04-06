# summarizer.py

from typing import List

class Summarizer:
    def __init__(self, llm):
        """
        :param llm: an LLM instance (e.g. ChatGroq) supporting .invoke(prompt) -> AIMessage or str
        """
        self.llm = llm

    def summarize(self, chunks: List[str], question: str = None) -> str:
        context = "\n\n".join(chunks)
        prompt = (
            "Summarize the following lecture content in clear, concise bullet points.\n\n"
            + (f"Focus on answering this question: {question}\n\n" if question else "")
            + "Content:\n"
            + context
            + "\n\nSummary:"
        )
        result = self.llm.invoke(prompt)
        # If the LLM returns an AIMessage (with .content), extract it; otherwise cast to str
        return result.content if hasattr(result, "content") else str(result)

