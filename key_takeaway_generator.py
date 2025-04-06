# key_takeaway_generator.py

class KeyTakeawayGenerator:
    def __init__(self, llm):
        """
        :param llm: an LLM instance (e.g. ChatGroq) supporting .invoke(prompt) -> AIMessage or str
        """
        self.llm = llm

    def generate_takeaways(self, chunks: list[str]) -> str:
        text = "\n".join(chunks)
        prompt = (
            "Given the following lecture content:\n\n"
            f"{text}\n\n"
            "Generate 5–7 key takeaways that summarize the most important points. "
            "Keep them concise and informative, and use bullet points."
        )
        result = self.llm.invoke(prompt)
        # Extract the actual text
        return result.content if hasattr(result, "content") else str(result)
